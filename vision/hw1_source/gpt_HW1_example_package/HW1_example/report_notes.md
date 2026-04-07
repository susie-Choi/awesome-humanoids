# HW1 보고서 메모

아래는 보고서에 바로 복붙하기보다, 본인 문체로 다시 정리할 때 참고할 메모입니다.

## 문제 1
- Translation: x축과 y축으로 평행이동. 객체의 형태는 유지되지만 위치만 이동.
- Rotation: 중심 기준 회전. 가장자리에는 검은 영역이 생길 수 있음.
- Affine: 평행성은 유지되지만 각도/길이는 변형 가능.
- Perspective: 원근 왜곡이 반영되어 사각형이 사다리꼴처럼 변형 가능.

## 문제 2
- Gaussian filter는 전체적으로 부드럽게 만들어 고주파 성분과 작은 잡음을 줄임.
- Sobel filter는 수평/수직 방향 경계 검출에 적합.
- Laplacian filter는 모든 방향의 2차 미분 기반이라 경계가 더 강하게 강조됨.
- Salt & Pepper noise에는 Gaussian filter도 일부 효과가 있지만, 점 형태의 극단값을 완전히 제거하지 못함.
- Median filter는 주변 픽셀의 중앙값을 사용하므로 Salt & Pepper noise 제거에 더 적합.
- 이번 실행 예시에서는 noisy 대비 Gaussian 적용 후 PSNR이 증가했고, Median 적용 후 PSNR이 더 크게 증가함.

## 문제 3
- resize down-sampling에서 INTER_NEAREST는 블록 현상이 잘 보이고, INTER_LINEAR는 무난하며, INTER_CUBIC은 비교적 부드럽다.
- up-sampling에서도 INTER_NEAREST는 계단 현상이 뚜렷하고, INTER_CUBIC이 가장 자연스럽게 보였다.
- Gaussian pyramid는 level이 내려갈수록 해상도와 세부 정보가 감소한다.
- Laplacian pyramid는 각 level 사이의 세부 정보 차이를 저장하므로, 이를 다시 더하면 원본 복원이 가능하다.
- float32 기반으로 계산하면 복원 오차를 거의 0으로 맞출 수 있다.

## 문제 4
- 직접 구현한 median blur는 각 윈도우의 중앙값을 선택하는 방식으로 동작한다.
- OpenCV medianBlur와 동일한 border 처리(edge padding)를 맞추면 결과가 완전히 같아질 수 있다.
- 본 예시 코드에서는 cv2.medianBlur와 직접 구현 결과의 MSE가 0으로 확인되었다.
