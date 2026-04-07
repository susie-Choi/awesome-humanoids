# HW1 보고서 작성용 메모

> 이 메모는 보고서(report.pdf)에 넣을 내용을 정리한 것입니다.
> 본인 문체로 다시 작성하세요. LLM 사용 의심 시 감점 대상입니다.

---

## 문제 1. Image Transformations

### 코드 설명
- Translation: 2×3 행렬 [[1,0,tx],[0,1,ty]]를 직접 구성하여 cv2.warpAffine에 전달. tx=50, ty=30으로 설정하여 오른쪽 아래로 이동.
- Rotation: cv2.getRotationMatrix2D로 이미지 중심 기준 45도 회전 행렬 생성. scale=1.0으로 크기 유지.
- Affine: 3쌍의 대응점을 지정하고 cv2.getAffineTransform으로 2×3 행렬 계산. 직선의 평행성은 유지됨.
- Perspective: 4쌍의 대응점으로 cv2.getPerspectiveTransform을 통해 3×3 행렬 계산. cv2.warpPerspective 적용.

### 결과 분석
- Translation: 이미지 형태는 그대로이고 위치만 이동. 이동된 영역 바깥은 검정(0)으로 채워짐.
- Rotation: 회전 후 모서리 부분에 검정 영역 발생. 이미지 내용 자체는 보존됨.
- Affine: 평행선은 유지되지만 각도와 길이 비율이 변형됨. 기울어지거나 찌그러진 형태.
- Perspective: 원근 왜곡이 반영되어 사각형이 사다리꼴 형태로 변형 가능. 가장 자유도가 높은 변환.

---

## 문제 2. Filters

### 코드 설명
- Gaussian Filter: cv2.GaussianBlur에 커널 (7,7), sigma=1.5 적용. 이미지 전체를 부드럽게 만듦.
- Sobel Filter: 그레이스케일 변환 후 cv2.Sobel로 x, y 방향 1차 미분 계산. sqrt(sx²+sy²)로 magnitude 합성.
- Laplacian Filter: 그레이스케일 변환 후 cv2.Laplacian(CV_64F, ksize=3) 적용. convertScaleAbs로 시각화.
- Salt & Pepper Noise: prob=0.05로 설정. 각 픽셀에 대해 확률적으로 0 또는 255 할당.
- Median Filter: cv2.medianBlur를 ksize=3, 5, 7로 각각 적용하여 커널 크기별 효과 비교.

### 결과 분석
- Gaussian Filter는 전체적으로 블러 처리되어 고주파 성분(에지, 노이즈)이 감소함.
- Sobel은 수평/수직 에지를 검출. Laplacian은 모든 방향의 에지를 동시에 검출하며 더 날카로운 결과.
- Salt & Pepper 노이즈에 Gaussian을 적용하면 극단값(0, 255)이 주변과 평균화되어 잔상이 남음. PSNR은 noisy 대비 개선되지만 완전한 제거는 어려움.
- Median Filter는 윈도우 내 중앙값을 선택하므로 극단적 outlier(소금/후추)를 효과적으로 제거. PSNR이 Gaussian 대비 크게 향상됨.
- Median ksize가 커질수록 노이즈 제거 효과는 증가하지만 세부 디테일도 함께 손실됨.

---

## 문제 3. Image Pyramids

### 코드 설명
- 3-1: cv2.resize로 down-sampling(1/2)과 up-sampling(2배) 수행. 보간법 3종 비교:
  - Down: INTER_NEAREST, INTER_LINEAR, INTER_AREA
  - Up: INTER_NEAREST, INTER_LINEAR, INTER_CUBIC
- 3-2: cv2.pyrDown을 반복 적용하여 4단계 Gaussian Pyramid 구성. cv2.pyrUp으로 역방향 확대도 수행.
- 3-3: float32 기반으로 Laplacian Pyramid 생성. L[i] = G[i] - pyrUp(G[i+1]). 복원 시 역순으로 pyrUp + L[i] 누적.

### 결과 분석
- Down-sampling: INTER_NEAREST는 블록 현상(aliasing)이 뚜렷. INTER_LINEAR는 무난. INTER_AREA는 축소 시 가장 자연스러움(안티앨리어싱 효과).
- Up-sampling: INTER_NEAREST는 계단 현상이 심함. INTER_LINEAR는 약간 흐릿. INTER_CUBIC이 가장 부드럽고 자연스러운 결과.
- Gaussian Pyramid: 레벨이 내려갈수록 해상도가 절반씩 줄고 세부 정보가 소실됨. 저주파 성분만 남음.
- Laplacian Pyramid: 각 레벨은 해당 해상도에서의 고주파(디테일) 정보를 저장. 모든 레벨을 합산하면 원본을 거의 완벽하게 복원 가능.
- float32로 계산하면 복원 오차(MSE)가 0에 수렴함.

---

## 문제 4. Median Blur 직접 구현

### 코드 설명
- 각 픽셀 위치에서 size×size 윈도우를 추출하고, flatten 후 sort하여 중앙값을 결과로 사용.
- 경계 처리는 np.pad(mode='edge')로 가장자리 픽셀을 복제하여 패딩.
- 컬러 이미지는 채널별(B, G, R)로 독립 처리.

### 결과 분석
- 직접 구현한 my_median_blur와 cv2.medianBlur(ksize=5)의 결과를 비교하면 MSE가 0에 가까움.
- cv2.medianBlur도 내부적으로 edge 패딩과 동일한 방식을 사용하므로 결과가 일치함.
- 직접 구현은 3중 for문으로 인해 속도가 매우 느림. OpenCV는 최적화된 C++ 구현이므로 실용적으로는 cv2.medianBlur 사용이 권장됨.

---

## 실행 방법

```
# lenna.png와 같은 폴더에 kiro_hw1_solution.py를 두고 실행
python kiro_hw1_solution.py
```

실행 후 `results/` 폴더 아래에 문제별 결과 이미지와 `summary.txt`가 생성됩니다.
