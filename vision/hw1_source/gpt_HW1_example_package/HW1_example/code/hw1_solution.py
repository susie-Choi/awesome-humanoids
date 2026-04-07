
import os
import random
import numpy as np
import cv2

# -----------------------------
# Utility
# -----------------------------
def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def save_image(path, image):
    cv2.imwrite(path, image)

def mse(img1, img2):
    diff = img1.astype(np.float64) - img2.astype(np.float64)
    return np.mean(diff ** 2)

def psnr(img1, img2):
    err = mse(img1, img2)
    if err == 0:
        return float("inf")
    return 10 * np.log10((255 ** 2) / err)

def to_uint8_abs(image):
    return cv2.convertScaleAbs(image)

# -----------------------------
# Problem #1 Image Transformations
# -----------------------------
def translate(image, x, y):
    h, w = image.shape[:2]
    translation_matrix = np.float32([
        [1, 0, x],
        [0, 1, y]
    ])
    transformed_image = cv2.warpAffine(image, translation_matrix, (w, h))
    return transformed_image

def rotate(image, angle):
    h, w = image.shape[:2]
    center = (w / 2, h / 2)
    transform_matrix = cv2.getRotationMatrix2D(center, angle, 1.0).astype(np.float32)
    transformed_image = cv2.warpAffine(image, transform_matrix, (w, h))
    return transformed_image

def AffineTransformation(image, source_match_point, target_match_point):
    h, w = image.shape[:2]
    source_match_point = np.float32(source_match_point)
    target_match_point = np.float32(target_match_point)
    transform_matrix = cv2.getAffineTransform(source_match_point, target_match_point).astype(np.float32)
    transformed_image = cv2.warpAffine(image, transform_matrix, (w, h))
    return transformed_image

def PerspectiveTransformation(image, source_match_point, target_match_point):
    h, w = image.shape[:2]
    source_match_point = np.float32(source_match_point)
    target_match_point = np.float32(target_match_point)
    transform_matrix = cv2.getPerspectiveTransform(source_match_point, target_match_point).astype(np.float32)
    transformed_image = cv2.warpPerspective(image, transform_matrix, (w, h))
    return transformed_image

# -----------------------------
# Problem #2 Filters
# -----------------------------
def Gaussian_filter(image, ksize=(5, 5), sigma=1.2):
    result = cv2.GaussianBlur(image, ksize, sigmaX=sigma, sigmaY=sigma)
    return result

def Sobel(image, ksize=3):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
    magnitude = cv2.magnitude(sobel_x, sobel_y)
    result = cv2.convertScaleAbs(magnitude)
    return result

def Laplacian(image, ksize=3):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lap = cv2.Laplacian(gray, cv2.CV_64F, ksize=ksize)
    result = cv2.convertScaleAbs(lap)
    return result

######## Don't modify this function ####################
def add_salt_pepper_noise(image, prob):
    # You can use prob argument as the probability of noise at each pixel
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

def median_blur(image, ksize=5):
    result = cv2.medianBlur(image, ksize)
    return result

# -----------------------------
# Problem #3 Image Pyramids
# -----------------------------
def gaussian_pyramid(image, levels=3):
    pyramid = [image]
    current = image
    for _ in range(levels):
        current = cv2.pyrDown(current)
        pyramid.append(current)
    return pyramid

def laplacian_pyramid(image, levels=3):
    g_pyr = [image.astype(np.float32)]
    current = image.astype(np.float32)
    for _ in range(levels):
        current = cv2.pyrDown(current)
        g_pyr.append(current)

    l_pyr = []
    for i in range(levels):
        size = (g_pyr[i].shape[1], g_pyr[i].shape[0])
        up = cv2.pyrUp(g_pyr[i + 1], dstsize=size)
        lap = g_pyr[i] - up
        l_pyr.append(lap)
    l_pyr.append(g_pyr[-1])  # smallest gaussian level
    return g_pyr, l_pyr

def restore_from_laplacian(laplacian_pyr):
    current = laplacian_pyr[-1].copy()
    for i in range(len(laplacian_pyr) - 2, -1, -1):
        size = (laplacian_pyr[i].shape[1], laplacian_pyr[i].shape[0])
        current = cv2.pyrUp(current, dstsize=size)
        current = current + laplacian_pyr[i]
    return np.clip(current, 0, 255).astype(np.uint8)

# -----------------------------
# Problem #4 Median Blur (Numpy)
# -----------------------------
def my_median_blur(image, size):
    if size % 2 == 0:
        raise ValueError("Median filter size must be odd.")
    if image.ndim not in (2, 3):
        raise ValueError("Input image must be grayscale or color.")

    pad = size // 2

    if image.ndim == 2:
        padded = np.pad(image, ((pad, pad), (pad, pad)), mode='edge')
        result = np.zeros_like(image)
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                window = padded[i:i + size, j:j + size]
                result[i, j] = np.median(window)
    else:
        padded = np.pad(image, ((pad, pad), (pad, pad), (0, 0)), mode='edge')
        result = np.zeros_like(image)
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                for c in range(image.shape[2]):
                    window = padded[i:i + size, j:j + size, c]
                    result[i, j, c] = np.median(window)

    return result.astype(np.uint8)

def main():
    random.seed(42)
    np.random.seed(42)

    input_path = "lenna.png"
    if not os.path.exists(input_path):
        raise FileNotFoundError("lenna.png not found. Place this script in the same folder as lenna.png or change input_path.")

    image = cv2.imread(input_path)
    if image is None:
        raise ValueError("Failed to load lenna.png")

    ensure_dir("results")
    ensure_dir("results/problem1")
    ensure_dir("results/problem2")
    ensure_dir("results/problem3")
    ensure_dir("results/problem4")

    # -------------------------
    # Problem 1
    # -------------------------
    translated = translate(image, 60, 40)
    rotated = rotate(image, 30)

    h, w = image.shape[:2]
    src_affine = np.float32([[50, 50], [200, 50], [50, 200]])
    dst_affine = np.float32([[30, 80], [220, 30], [80, 220]])
    affine_img = AffineTransformation(image, src_affine, dst_affine)

    src_persp = np.float32([[40, 40], [w - 40, 40], [40, h - 40], [w - 40, h - 40]])
    dst_persp = np.float32([[0, 30], [w - 60, 0], [50, h - 20], [w - 1, h - 60]])
    perspective_img = PerspectiveTransformation(image, src_persp, dst_persp)

    save_image("results/problem1/original.png", image)
    save_image("results/problem1/translated.png", translated)
    save_image("results/problem1/rotated.png", rotated)
    save_image("results/problem1/affine.png", affine_img)
    save_image("results/problem1/perspective.png", perspective_img)

    # -------------------------
    # Problem 2
    # -------------------------
    gaussian_img = Gaussian_filter(image, (5, 5), 1.2)
    sobel_img = Sobel(image, 3)
    laplacian_img = Laplacian(image, 3)

    prob = 0.1
    noisy = add_salt_pepper_noise(image, prob)
    noisy_gaussian = Gaussian_filter(noisy, (5, 5), 1.2)
    noisy_median = median_blur(noisy, 5)
    noisy_sobel = Sobel(noisy, 3)
    noisy_laplacian = Laplacian(noisy, 3)

    save_image("results/problem2/original.png", image)
    save_image("results/problem2/gaussian.png", gaussian_img)
    save_image("results/problem2/sobel.png", sobel_img)
    save_image("results/problem2/laplacian.png", laplacian_img)
    save_image("results/problem2/noisy_prob_0.1.png", noisy)
    save_image("results/problem2/noisy_gaussian.png", noisy_gaussian)
    save_image("results/problem2/noisy_median.png", noisy_median)
    save_image("results/problem2/noisy_sobel.png", noisy_sobel)
    save_image("results/problem2/noisy_laplacian.png", noisy_laplacian)

    # -------------------------
    # Problem 3-1 resize/interpolation
    # -------------------------
    down_size = (w // 2, h // 2)
    up_size = (w * 2, h * 2)

    down_result_01 = cv2.resize(image, down_size, interpolation=cv2.INTER_NEAREST)
    down_result_02 = cv2.resize(image, down_size, interpolation=cv2.INTER_LINEAR)
    down_result_03 = cv2.resize(image, down_size, interpolation=cv2.INTER_CUBIC)

    up_result_01 = cv2.resize(image, up_size, interpolation=cv2.INTER_NEAREST)
    up_result_02 = cv2.resize(image, up_size, interpolation=cv2.INTER_LINEAR)
    up_result_03 = cv2.resize(image, up_size, interpolation=cv2.INTER_CUBIC)

    save_image("results/problem3/down_nearest.png", down_result_01)
    save_image("results/problem3/down_linear.png", down_result_02)
    save_image("results/problem3/down_cubic.png", down_result_03)
    save_image("results/problem3/up_nearest.png", up_result_01)
    save_image("results/problem3/up_linear.png", up_result_02)
    save_image("results/problem3/up_cubic.png", up_result_03)

    # Problem 3-2 Gaussian Pyramid
    g_pyr = gaussian_pyramid(image, levels=3)
    for idx, img in enumerate(g_pyr):
        save_image(f"results/problem3/gaussian_pyramid_level_{idx}.png", img)

    # pyrUp examples
    g_up_1 = cv2.pyrUp(g_pyr[1], dstsize=(g_pyr[0].shape[1], g_pyr[0].shape[0]))
    g_up_2 = cv2.pyrUp(g_pyr[2], dstsize=(g_pyr[1].shape[1], g_pyr[1].shape[0]))
    g_up_3 = cv2.pyrUp(g_pyr[3], dstsize=(g_pyr[2].shape[1], g_pyr[2].shape[0]))
    save_image("results/problem3/gaussian_up_1.png", g_up_1)
    save_image("results/problem3/gaussian_up_2.png", g_up_2)
    save_image("results/problem3/gaussian_up_3.png", g_up_3)

    # Problem 3-3 Laplacian Pyramid and restoration
    gaussian_pyr, laplacian_pyr = laplacian_pyramid(image, levels=3)
    for idx, img in enumerate(laplacian_pyr):
        if idx == len(laplacian_pyr) - 1:
            view = np.clip(img, 0, 255).astype(np.uint8)
        else:
            view = np.clip(img + 128, 0, 255).astype(np.uint8)
        save_image(f"results/problem3/laplacian_pyramid_level_{idx}.png", view)

    restored_image = restore_from_laplacian(laplacian_pyr)
    save_image("results/problem3/restored_from_laplacian.png", restored_image)
    diff_image = cv2.absdiff(image, restored_image)
    save_image("results/problem3/restored_absdiff.png", diff_image)

    # -------------------------
    # Problem 4
    # -------------------------
    cv_median = cv2.medianBlur(noisy, 5)
    my_median = my_median_blur(noisy, 5)
    median_diff = cv2.absdiff(cv_median, my_median)

    save_image("results/problem4/cv2_median.png", cv_median)
    save_image("results/problem4/my_median.png", my_median)
    save_image("results/problem4/median_absdiff.png", median_diff)

    # -------------------------
    # Numeric summary
    # -------------------------
    with open("results/summary.txt", "w", encoding="utf-8") as f:
        f.write("[Problem 2]\n")
        f.write(f"MSE(original, noisy): {mse(image, noisy):.4f}\n")
        f.write(f"PSNR(original, noisy): {psnr(image, noisy):.4f}\n")
        f.write(f"MSE(original, noisy_gaussian): {mse(image, noisy_gaussian):.4f}\n")
        f.write(f"PSNR(original, noisy_gaussian): {psnr(image, noisy_gaussian):.4f}\n")
        f.write(f"MSE(original, noisy_median): {mse(image, noisy_median):.4f}\n")
        f.write(f"PSNR(original, noisy_median): {psnr(image, noisy_median):.4f}\n\n")

        f.write("[Problem 3]\n")
        for idx, img in enumerate(g_pyr):
            f.write(f"Gaussian pyramid level {idx}: shape={img.shape}\n")
        f.write(f"Restored image MSE: {mse(image, restored_image):.8f}\n")
        f.write(f"Restored image PSNR: {psnr(image, restored_image):.8f}\n\n")

        f.write("[Problem 4]\n")
        f.write(f"MSE(cv2_median, my_median): {mse(cv_median, my_median):.8f}\n")
        f.write(f"PSNR(cv2_median, my_median): {psnr(cv_median, my_median):.8f}\n")

if __name__ == "__main__":
    main()
