import os
import numpy as np
import cv2
import random

'''
Problem #1 Image Transformations
'''

# 1-1
def translate(image, x, y):
    h, w = image.shape[:2]
    translation_matrix = np.float32([[1, 0, x],[0, 1, y]])
    transformed_image = cv2.warpAffine(image, translation_matrix, (w, h))
    return transformed_image

def rotate(image, angle):
    h, w = image.shape[:2]
    center = (w / 2, h / 2)
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


'''
Problem #2 Linear Filters
'''

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


# 2-3
def median_blur(image, ksize=5):
    result = cv2.medianBlur(image, ksize)
    return result


'''
Problem #3 Image Pyramids
'''

# 3-2 Gaussian Pyramid
def build_gaussian_pyramid(image, levels=4):
    pyr = [image.copy()]
    tmp = image.copy()
    for _ in range(levels):
        tmp = cv2.pyrDown(tmp)
        pyr.append(tmp)
    return pyr

# 3-3 Laplacian Pyramid
def build_laplacian_pyramid(image, levels=4):
    gpyr = [image.astype(np.float32)]
    tmp = image.astype(np.float32)
    for _ in range(levels):
        tmp = cv2.pyrDown(tmp)
        gpyr.append(tmp)

    lpyr = []
    for i in range(levels):
        sz = (gpyr[i].shape[1], gpyr[i].shape[0])
        up = cv2.pyrUp(gpyr[i+1], dstsize=sz)
        lpyr.append(gpyr[i] - up)
    lpyr.append(gpyr[-1])
    return gpyr, lpyr

def restore_from_laplacian(lpyr):
    cur = lpyr[-1].copy()
    for i in range(len(lpyr) - 2, -1, -1):
        sz = (lpyr[i].shape[1], lpyr[i].shape[0])
        cur = cv2.pyrUp(cur, dstsize=sz) + lpyr[i]
    return np.clip(cur, 0, 255).astype(np.uint8)


'''
Problem #4 Median Blur
'''
def my_median_blur(image, size):
    # numpy.sort로 median 직접 구현
    # 패딩 없이 필요 영역만 처리, 경계쪽은 원본 값 유지하기
    half = size // 2
    result = image.copy()

    if image.ndim == 2:
        for i in range(half, image.shape[0] - half):
            for j in range(half, image.shape[1] - half):
                window = image[i-half:i+half+1, j-half:j+half+1].flatten()
                window.sort()
                result[i, j] = window[len(window) // 2]
    else:
        for c in range(image.shape[2]):
            for i in range(half, image.shape[0] - half):
                for j in range(half, image.shape[1] - half):
                    window = image[i-half:i+half+1, j-half:j+half+1, c].flatten()
                    window.sort()
                    result[i, j, c] = window[len(window) // 2]

    return result.astype(np.uint8)


if __name__ == "__main__":
    random.seed(2025712918)
    np.random.seed(2025712918)

    img = cv2.imread("lenna.png")
    assert img is not None, "lenna.png 파일 없음"
    h, w = img.shape[:2]

    for d in ["results/p1", "results/p2", "results/p3", "results/p4"]:
        os.makedirs(d, exist_ok=True)

    # Problem 1
    translated = translate(img, 50, 30)
    rotated = rotate(img, 45)

    src_af = np.float32([[50, 50], [200, 50], [50, 200]])
    dst_af = np.float32([[10, 100], [200, 50], [100, 250]])
    affine_img = AffineTransformation(img, src_af, dst_af)

    src_ps = np.float32([[56, 65], [368, 52], [28, 387], [389, 390]])
    dst_ps = np.float32([[0, 0], [w-1, 0], [0, h-1], [w-1, h-1]])
    persp_img = PerspectiveTransformation(img, src_ps, dst_ps)

    cv2.imwrite("results/p1/original.png", img)
    cv2.imwrite("results/p1/translated.png", translated)
    cv2.imwrite("results/p1/rotated.png", rotated)
    cv2.imwrite("results/p1/affine.png", affine_img)
    cv2.imwrite("results/p1/perspective.png", persp_img)

    # Problem 2
    gauss_img = Gaussian_filter(img)
    sobel_img = Sobel(img)
    lap_img = Laplacian(img)

    cv2.imwrite("results/p2/gaussian.png", gauss_img)
    cv2.imwrite("results/p2/sobel.png", sobel_img)
    cv2.imwrite("results/p2/laplacian.png", lap_img)

    # salt & pepper noise
    noisy = add_salt_pepper_noise(img, 0.1)
    cv2.imwrite("results/p2/noisy_sp.png", noisy)

    # 노이즈 이미지에 Gaussian 필터 적용
    noisy_gauss = Gaussian_filter(noisy)
    cv2.imwrite("results/p2/noisy_gaussian.png", noisy_gauss)

    # median blur 다양한 커널 크기 적용
    noisy_med3 = median_blur(noisy, 3)
    noisy_med5 = median_blur(noisy, 5)
    noisy_med7 = median_blur(noisy, 7)
    cv2.imwrite("results/p2/noisy_median3.png", noisy_med3)
    cv2.imwrite("results/p2/noisy_median5.png", noisy_med5)
    cv2.imwrite("results/p2/noisy_median7.png", noisy_med7)

    # Problem 3
    # 3-1 resize interpolation
    down_sz = (w // 2, h // 2)
    up_sz = (w * 2, h * 2)

    down_result_01 = cv2.resize(img, down_sz, interpolation=cv2.INTER_NEAREST)
    down_result_02 = cv2.resize(img, down_sz, interpolation=cv2.INTER_LINEAR)
    down_result_03 = cv2.resize(img, down_sz, interpolation=cv2.INTER_AREA)
    cv2.imwrite("results/p3/down_nearest.png", down_result_01)
    cv2.imwrite("results/p3/down_linear.png", down_result_02)
    cv2.imwrite("results/p3/down_area.png", down_result_03)

    up_result_01 = cv2.resize(img, up_sz, interpolation=cv2.INTER_NEAREST)
    up_result_02 = cv2.resize(img, up_sz, interpolation=cv2.INTER_LINEAR)
    up_result_03 = cv2.resize(img, up_sz, interpolation=cv2.INTER_CUBIC)
    cv2.imwrite("results/p3/up_nearest.png", up_result_01)
    cv2.imwrite("results/p3/up_linear.png", up_result_02)
    cv2.imwrite("results/p3/up_cubic.png", up_result_03)

    # 3-2 Gaussian Pyramid
    levels = 4
    gpyr = build_gaussian_pyramid(img, levels)
    for i, g in enumerate(gpyr):
        cv2.imwrite(f"results/p3/gpyr_level{i}.png", g)

    # pyrUp
    Gaussian_up_01 = cv2.pyrUp(gpyr[1], dstsize=(gpyr[0].shape[1], gpyr[0].shape[0]))
    Gaussian_up_02 = cv2.pyrUp(gpyr[2], dstsize=(gpyr[1].shape[1], gpyr[1].shape[0]))
    Gaussian_up_03 = cv2.pyrUp(gpyr[3], dstsize=(gpyr[2].shape[1], gpyr[2].shape[0]))
    cv2.imwrite("results/p3/gpyr_up_from1.png", Gaussian_up_01)
    cv2.imwrite("results/p3/gpyr_up_from2.png", Gaussian_up_02)
    cv2.imwrite("results/p3/gpyr_up_from3.png", Gaussian_up_03)

    # 3-3 Laplacian Pyramid + 복원
    gpyr_f, lpyr = build_laplacian_pyramid(img, levels)
    for i, l in enumerate(lpyr):
        if i < len(lpyr) - 1:
            vis = np.clip(l + 128, 0, 255).astype(np.uint8)
        else:
            vis = np.clip(l, 0, 255).astype(np.uint8)
        cv2.imwrite(f"results/p3/lpyr_level{i}.png", vis)

    restored = restore_from_laplacian(lpyr)
    cv2.imwrite("results/p3/restored.png", restored)
    cv2.imwrite("results/p3/restore_diff.png", cv2.absdiff(img, restored))

    # Problem 4
    cv_med = cv2.medianBlur(noisy, 5)
    my_med = my_median_blur(noisy, 5)
    cv2.imwrite("results/p4/cv2_median5.png", cv_med)
    cv2.imwrite("results/p4/my_median5.png", my_med)
    cv2.imwrite("results/p4/median_diff.png", cv2.absdiff(cv_med, my_med))

    # 출력 확인
    print("Problem 2")
    print(f"noisy MSE: {np.mean((img.astype(float) - noisy.astype(float))**2):.2f}")
    print(f"median3 MSE: {np.mean((img.astype(float) - noisy_med3.astype(float))**2):.2f}")
    print(f"median5 MSE: {np.mean((img.astype(float) - noisy_med5.astype(float))**2):.2f}")
    print(f"median7 MSE: {np.mean((img.astype(float) - noisy_med7.astype(float))**2):.2f}")
    print()
    print("Problem 3")
    print(f"restored diff: {np.mean((img.astype(float) - restored.astype(float))**2):.6f}")
    print()
    print("Problem 4")
    print(f"my_median vs cv2: {np.mean((cv_med.astype(float) - my_med.astype(float))**2):.6f}")
    print()
    print("HW1 끝")
