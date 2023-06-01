import cv2

# 거북이 영상 파일 경로
turtle_video_file = "hapsung/turtle.mp4"

# 거북이 영상 캡처 객체 생성
turtle_cap = cv2.VideoCapture(turtle_video_file) 

# 눈 영상 파일 경로
snow_video_file = "hapsung/snow.mp4"

# 눈 영상 캡처 객체 생성
snow_cap = cv2.VideoCapture(snow_video_file)

# 비디오 크기
cap_size = (int(turtle_cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(turtle_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))) 

# 결과 영상 크기
result_size = (int(cap_size[0] / 2), int(cap_size[1] / 2))

# 비디오 저장을 위한 설정
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
out = cv2.VideoWriter('ex.mp4', fourcc, turtle_cap.get(cv2.CAP_PROP_FPS), result_size)

# 배경 제거 모델 생성
sub = cv2.createBackgroundSubtractorKNN(history=1080, dist2Threshold=10000000, detectShadows=False)
# 카메라 열어서 캡쳐
while turtle_cap.isOpened():
    # 거북이 영상 프레임 읽기
    ret, fg_img = turtle_cap.read()

    if not ret:
        break

    # 배경 제거 적용
    mask = sub.apply(fg_img)

    # Morphological Transformations(형태변환)
    # 5*5 형태변환
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    # morphology 의 이미지 바깥의 노이즈 제거
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    # morphology 의 안쪽 바깥의 노이즈 제거
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    # 원본이미지를 굵어지게 만들어주는 효과 
    mask = cv2.dilate(mask, kernel, iterations=2)

    # 거북이 영역 추출
    turtle_roi = cv2.bitwise_and(fg_img, fg_img, mask=mask)

    # 눈 영상 프레임 읽기
    ret, snow_img = snow_cap.read()

    if not ret:
        snow_cap.set(1, 0)
        _, snow_img = snow_cap.read()

    # 눈 영상 크기를 거북이 영상 크기로 조정
    snow_img = cv2.resize(snow_img, dsize=cap_size)

    # 거북이 영역에 눈 합성
    result = cv2.add(turtle_roi, snow_img)

    # 전체 결과 이미지에 합성
    full_result = cv2.bitwise_or(result, fg_img)

    # 결과 영상 크기 조정
    resized_result = cv2.resize(full_result, dsize=result_size)

    # 결과 출력 및 저장
    cv2.imshow('result', resized_result)
    out.write(resized_result)

    if cv2.waitKey(1) == ord('q'):
        break

out.release()
turtle_cap.release()
snow_cap.release()

