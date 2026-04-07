import os
import random
import numpy as np
import cv2

# ──────────────────────────────
# Utility
# ──────────────────────────────
def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def save(path, img):
    cv2.imwrite(path, img)

def mse(a, b):
    return np.mean((a.astype(np.float64) - b.astype(np.float64)) ** 2)

def psnr(a, b):
    m = mse(a, b)
    return float("inf") if m == 0 else 10 * np.log10(255**2 / m)

# ──────────────────────────────
# Problem #1  Image Transformations
# ──────────────────────────────
def translate(image, x, y):
    h, w = image.shape[:2]
    translation_matrix = np.float32([[1, 0, x],
                                     [0, 1, y]])
    transformed_image = cv2.warpAffine(image, translation_matrix, (w, h))
    return transformed_image

def rotate(image, angle):
    h, w = image.shape[:2]
    center = (w / 2.0, h / 2.0)
    transform_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    transformed_image = cv2.warpAffine(image, transform_matrix, (w, h))
    return transformed_image

def AffineTransformation(image, source_match_point, target_match_point):
    h, w = image.shape[:2]
    src = np.float32(source_match_point)
    dst = np.float32(target_match_point)
    transform_matrix = cv2.getAffineTransform(src, dst)
    transformed_image = cv2.warpAffine(image, transform_matrix, (w, h))
    return transformed_image

def PerspectiveTransformation(image, source_match_point, target_match_point):
    h, w = image.shape[:2]
    src = np.float32(source_match_point)
    dst = np.float32(target_match_point)
    transform_matrix = cv2.getPerspectiveTransform(src, dst)
    transformed_image = cv2.warpPerspective(image, transform_matrix, (w, h))
    return transformed_image


# ──────────────────────────────
# Problem #2  Linear Filters
# ──────────────────────────────

# 2-1
def Gaussian_filter(image, ksize=(7, 7), sigma=1.5):
    result = cv2.GaussianBlur(image, ksize, sigmaX=sigma, sigmaY=sigma)
    return result

def Sobel(image, ksize=3):
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sx = cv2.Sobel(image_gray, cv2.CV_64F, 1, 0, ksize=ksize)
    sy = cv2.Sobel(image_gray, cv2.CV_64F, 0, 1, ksize=ksize)
    mag = np.sqrt(sx**2 + sy**2)
    result = np.clip(mag, 0, 255).astype(np.uint8)
    return result

def Laplacian(image, ksize=3):
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lap = cv2.Laplacian(image_gray, cv2.CV_64F, ksize=ksize)
    result = cv2.convertScaleAbs(lap)
    return result

# 2-2
######## Don't modify this function ####################
def add_salt_pepper_noise(image, prob):
    result = np.zeros(image.shape, dtype=np.uint8)
    th = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rand = random.random()
            if rand < prob:
                result[i][j] = 0
            elif rand > th:
                result[i][j] = 255
            else:
                result[i][j] = image[i][j]
    return result
#########################################################

# 2-3
def median_blur(image, ksize=5):
    result = cv2.medianBlur(image, ksize)
    return result


# ──────────────────────────────
# Problem #3  Image Pyramids
# ──────────────────────────────

def build_gaussian_pyramid(image, levels=4):
    """Gaussian pyramid: 원본 포함 levels+1 장 반환."""
    pyr = [image.copy()]
    cur = image.copy()
    for _ in range(levels):
        cur = cv2.pyrDown(cur)
        pyr.append(cur)
    return pyr

def build_laplacian_pyramid(image, levels=4):
    """Laplacian pyramid 생성. float32 기반으로 복원 오차 최소화."""
    gpyr = [image.astype(np.float32)]
    cur = image.astype(np.float32)
    for _ in range(levels):
        cur = cv2.pyrDown(cur)
        gpyr.append(cur)

    lpyr = []
    for i in range(levels):
        sz = (gpyr[i].shape[1], gpyr[i].shape[0])
        expanded = cv2.pyrUp(gpyr[i + 1], dstsize=sz)
        lpyr.append(gpyr[i] - expanded)
    lpyr.append(gpyr[-1])          # 가장 작은 Gaussian level
    return gpyr, lpyr

def restore_from_laplacian(lpyr):
    """Laplacian pyramid으로부터 원본 복원."""
    cur = lpyr[-1].copy()
    for i in range(len(lpyr) - 2, -1, -1):
        sz = (lpyr[i].shape[1], lpyr[i].shape[0])
        cur = cv2.pyrUp(cur, dstsize=sz) + lpyr[i]
    return np.clip(cur, 0, 255).astype(np.uint8)


# ──────────────────────────────
# Problem #4  Median Blur (직접 구현)
# ──────────────────────────────
def my_median_blur(image, size):
    """numpy.sort 기반 median filter. 패딩은 edge 모드 사용."""
    if size % 2 == 0:
        raise ValueError("size는 홀수여야 합니다.")

    pad = size // 2

    if image.ndim == 2:  # grayscale
        padded = np.pad(image, ((pad, pad), (pad, pad)), mode='edge')
        result = np.zeros_like(image)
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                window = padded[i:i + size, j:j + size].flatten()
                window.sort()
                result[i, j] = window[len(window) // 2]
    else:  # color (BGR)
        padded = np.pad(image, ((pad, pad), (pad, pad), (0, 0)), mode='edge')
        result = np.zeros_like(image)
        for c in range(image.shape[2]):
            for i in range(image.shape[0]):
                for j in range(image.shape[1]):
                    window = padded[i:i + size, j:j + size, c].flatten()
                    window.sort()
                    result[i, j, c] = window[len(window) // 2]

    return result.astype(np.uint8)

# ══════════════════════════════
# Main – 전체 실행 및 결과 저장
# ══════════════════════════════
def main():
    random.seed(42)
    np.random.seed(42)

    img = cv2.imread("lenna.png")
    if img is None:
        raise FileNotFoundError("lenna.png를 찾을 수 없습니다.")
    h, w = img.shape[:2]

    for d in ["results/p1", "results/p2", "results/p3", "results/p4"]:
        ensure_dir(d)

    # ── Problem 1 ──────────────────────────────
    save("results/p1/original.png", img)

    translated = translate(img, 50, 30)
    save("results/p1/translated.png", translated)

    rotated = rotate(img, 45)
    save("results/p1/rotated.png", rotated)

    src_af = np.float32([[50, 50], [200, 50], [50, 200]])
    dst_af = np.float32([[10, 100], [200, 50], [100, 250]])
    affine_img = AffineTransformation(img, src_af, dst_af)
    save("results/p1/affine.png", affine_img)

    src_ps = np.float32([[56, 65], [368, 52], [28, 387], [389, 390]])
    dst_ps = np.float32([[0, 0], [w - 1, 0], [0, h - 1], [w - 1, h - 1]])
    persp_img = PerspectiveTransformation(img, src_ps, dst_ps)
    save("results/p1/perspective.png", persp_img)

    # ── Problem 2 ──────────────────────────────
    save("results/p2/original.png", img)

    gauss_img = Gaussian_filter(img)
    save("results/p2/gaussian_7x7.png", gauss_img)

    sobel_img = Sobel(img)
    save("results/p2/sobel.png", sobel_img)

    lap_img = Laplacian(img)
    save("results/p2/laplacian.png", lap_img)

    # 2-2  Salt & Pepper + Gaussian
    noise_prob = 0.05
    noisy = add_salt_pepper_noise(img, noise_prob)
    save("results/p2/noisy_sp005.png", noisy)

    noisy_gauss = Gaussian_filter(noisy)
    save("results/p2/noisy_gaussian.png", noisy_gauss)

    # Sobel / Laplacian on noisy
    noisy_sobel = Sobel(noisy)
    noisy_lap = Laplacian(noisy)
    save("results/p2/noisy_sobel.png", noisy_sobel)
    save("results/p2/noisy_laplacian.png", noisy_lap)

    # 2-3  Median filter on noisy
    noisy_med3 = median_blur(noisy, 3)
    noisy_med5 = median_blur(noisy, 5)
    noisy_med7 = median_blur(noisy, 7)
    save("results/p2/noisy_median_3.png", noisy_med3)
    save("results/p2/noisy_median_5.png", noisy_med5)
    save("results/p2/noisy_median_7.png", noisy_med7)

    # ── Problem 3 ──────────────────────────────
    # 3-1  resize interpolation 비교
    down_sz = (w // 2, h // 2)
    up_sz   = (w * 2, h * 2)

    interps_down = [
        ("nearest",  cv2.INTER_NEAREST),
        ("linear",   cv2.INTER_LINEAR),
        ("area",     cv2.INTER_AREA),
    ]
    interps_up = [
        ("nearest",  cv2.INTER_NEAREST),
        ("linear",   cv2.INTER_LINEAR),
        ("cubic",    cv2.INTER_CUBIC),
    ]
    for name, flag in interps_down:
        save(f"results/p3/down_{name}.png", cv2.resize(img, down_sz, interpolation=flag))
    for name, flag in interps_up:
        save(f"results/p3/up_{name}.png", cv2.resize(img, up_sz, interpolation=flag))

    # 3-2  Gaussian Pyramid
    levels = 4
    gpyr = build_gaussian_pyramid(img, levels)
    for i, g in enumerate(gpyr):
        save(f"results/p3/gpyr_level{i}.png", g)

    # pyrUp 예시
    for i in range(1, len(gpyr)):
        up = cv2.pyrUp(gpyr[i], dstsize=(gpyr[i-1].shape[1], gpyr[i-1].shape[0]))
        save(f"results/p3/gpyr_up_from_level{i}.png", up)

    # 3-3  Laplacian Pyramid + 복원
    gpyr_f, lpyr = build_laplacian_pyramid(img, levels)
    for i, l in enumerate(lpyr):
        if i < len(lpyr) - 1:
            vis = np.clip(l + 128, 0, 255).astype(np.uint8)
        else:
            vis = np.clip(l, 0, 255).astype(np.uint8)
        save(f"results/p3/lpyr_level{i}.png", vis)

    restored = restore_from_laplacian(lpyr)
    save("results/p3/restored.png", restored)
    diff = cv2.absdiff(img, restored)
    save("results/p3/restore_diff.png", diff)

    # ── Problem 4 ──────────────────────────────
    cv_med = cv2.medianBlur(noisy, 5)
    my_med = my_median_blur(noisy, 5)
    med_diff = cv2.absdiff(cv_med, my_med)

    save("results/p4/cv2_median5.png", cv_med)
    save("results/p4/my_median5.png", my_med)
    save("results/p4/median_diff.png", med_diff)

    # ── 수치 요약 ──────────────────────────────
    lines = []
    lines.append("=== Problem 2: Noise & Filter 비교 ===")
    lines.append(f"  MSE(orig, noisy)          = {mse(img, noisy):.4f}")
    lines.append(f"  PSNR(orig, noisy)         = {psnr(img, noisy):.4f} dB")
    lines.append(f"  MSE(orig, noisy+gauss)    = {mse(img, noisy_gauss):.4f}")
    lines.append(f"  PSNR(orig, noisy+gauss)   = {psnr(img, noisy_gauss):.4f} dB")
    lines.append(f"  MSE(orig, noisy+med3)     = {mse(img, noisy_med3):.4f}")
    lines.append(f"  PSNR(orig, noisy+med3)    = {psnr(img, noisy_med3):.4f} dB")
    lines.append(f"  MSE(orig, noisy+med5)     = {mse(img, noisy_med5):.4f}")
    lines.append(f"  PSNR(orig, noisy+med5)    = {psnr(img, noisy_med5):.4f} dB")
    lines.append(f"  MSE(orig, noisy+med7)     = {mse(img, noisy_med7):.4f}")
    lines.append(f"  PSNR(orig, noisy+med7)    = {psnr(img, noisy_med7):.4f} dB")
    lines.append("")
    lines.append("=== Problem 3: Pyramid ===")
    for i, g in enumerate(gpyr):
        lines.append(f"  Gaussian level {i}: {g.shape}")
    lines.append(f"  Restored MSE  = {mse(img, restored):.8f}")
    lines.append(f"  Restored PSNR = {psnr(img, restored):.4f} dB")
    lines.append("")
    lines.append("=== Problem 4: my_median vs cv2.medianBlur ===")
    lines.append(f"  MSE  = {mse(cv_med, my_med):.8f}")
    lines.append(f"  PSNR = {psnr(cv_med, my_med):.4f} dB")

    summary = "\n".join(lines)
    print(summary)
    with open("results/summary.txt", "w", encoding="utf-8") as f:
        f.write(summary + "\n")

    print("\n모든 결과가 results/ 폴더에 저장되었습니다.")


if __name__ == "__main__":
    main()
