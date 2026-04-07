import numpy as np
import cv2
import random

'''
Problem #1 Image Transformations
'''

# 1-1
def translate(image, x, y):
    # 이미지 이동을 위한 2x3 변환 행렬 생성 [1 0 tx; 0 1 ty]
    translation_matrix = np.float32([[1, 0, x], [0, 1, y]])
    # warpAffine을 사용하여 이미지 이동 적용
    transformed_image = cv2.warpAffine(image, translation_matrix, (image.shape[1], image.shape[0]))
    return transformed_image

def rotate(image, angle):
    # 이미지의 중심점을 계산
    height, width = image.shape[:2]
    center = (width / 2, height / 2)
    # 회전 행렬 생성 (중심점, 각도, 스케일)
    transform_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    # warpAffine으로 회전 적용
    transformed_image = cv2.warpAffine(image, transform_matrix, (width, height))
    return transformed_image

def AffineTransformation(image, source_match_point, target_match_point):
    # 3개의 점 쌍으로부터 2x3 아핀 변환 행렬 계산
    transform_matrix = cv2.getAffineTransform(source_match_point, target_match_point)
    # warpAffine 적용
    transformed_image = cv2.warpAffine(image, transform_matrix, (image.shape[1], image.shape[0]))
    return transformed_image

def PerspectiveTransformation(image, source_match_point, target_match_point):
    # 4개의 점 쌍으로부터 3x3 투영 변환 행렬 계산
    transform_matrix = cv2.getPerspectiveTransform(source_match_point, target_match_point)
    # warpPerspective 적용
    transformed_image = cv2.warpPerspective(image, transform_matrix, (image.shape[1], image.shape[0]))
    return transformed_image


'''
Problem #2 Linear Filters
'''

# 2-1
def Gaussian_filter(image):
    # GaussianBlur 적용: 커널 크기 (5, 5), 표준편차 0(커널 크기에 의해 자동 계산)
    result = cv2.GaussianBlur(image, (5, 5), 0)
    return result

def Sobel(image):
    # 흑백 이미지로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # X, Y 방향 미분 계산 (CV_64F로 정밀도 유지)
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    # 절댓값 변환 및 8비트 결합
    abs_sobel_x = cv2.convertScaleAbs(sobel_x)
    abs_sobel_y = cv2.convertScaleAbs(sobel_y)
    result = cv2.addWeighted(abs_sobel_x, 0.5, abs_sobel_y, 0.5, 0)
    return result

def Laplacian(image):
    # 흑백 이미지로 변환 후 라플라시안 필터 적용
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    result = cv2.convertScaleAbs(laplacian)
    return result

# 2-2
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

# 2-2 & 2-3 실행 예시 코드 (메인 로직에 포함 필요)
def filter_noise_experiment(image):
    noisy_img = add_salt_pepper_noise(image, 0.05)
    gaussian_on_noise = Gaussian_filter(noisy_img)
    median_on_noise = cv2.medianBlur(noisy_img, 5)
    return noisy_img, gaussian_on_noise, median_on_noise

# 2-3
def median_blur(image):
    # OpenCV 제공 함수 활용
    result = cv2.medianBlur(image, 5)
    return result


'''
Problem #3 Image Pyramids
'''

def image_pyramid_experiment(image):
    # 3-1: Interpolation 비교
    # Down-sampling (0.5배)
    down_result_01 = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
    down_result_02 = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
    down_result_03 = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

    # Up-sampling (2배)
    up_result_01 = cv2.resize(image, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_NEAREST)
    up_result_02 = cv2.resize(image, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_LINEAR)
    up_result_03 = cv2.resize(image, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)

    # 3-2: Gaussian Pyramid
    Gaussian_down_01 = cv2.pyrDown(image)
    Gaussian_down_02 = cv2.pyrDown(Gaussian_down_01)
    
    Gaussian_up_01 = cv2.pyrUp(Gaussian_down_02)
    Gaussian_up_02 = cv2.pyrUp(Gaussian_up_01)

    # 3-3: Laplacian Pyramid 복원
    # L0 = G0 - expand(G1)
    G0 = image.astype(np.float32)
    G1 = cv2.pyrDown(G0)
    L0 = cv2.subtract(G0, cv2.pyrUp(G1))
    
    # 복원: Restored = L0 + expand(G1)
    Restored_image = cv2.add(L0, cv2.pyrUp(G1))
    Restored_image = np.clip(Restored_image, 0, 255).astype(np.uint8)
    
    return Restored_image


'''
Problem #4 Median Blur 직접 구현
'''
def my_median_blur(image, size):
    # 입력 이미지의 차원 확인 (H, W, C)
    height, width = image.shape[:2]
    pad = size // 2
    result = np.zeros_like(image)

    # 채널별 처리 (BGR)
    for c in range(image.shape[2]):
        for i in range(pad, height - pad):
            for j in range(pad, width - pad):
                # 윈도우 영역 추출
                window = image[i - pad:i + pad + 1, j - pad:j + pad + 1, c]
                # 중앙값 계산 (정렬 후 중간 인덱스 추출)
                result[i, j, c] = np.median(window)
                
    return result


if __name__ == "__main__":
    img = cv2.imread('lenna.png')
    if img is None:
        print("이미지를 불러올 수 없습니다.")
    else:
        # 실행 테스트 및 결과 저장 로직을 여기에 추가하십시오.
        pass