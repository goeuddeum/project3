import cv2
import time
import random

cap = cv2.VideoCapture('muyaho.mp4')
# 무야호 시작
cap.set(1,900)

# 영상의 크기를 구하기. w,h
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# 영상을 열고 캡쳐하기
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
out = cv2.VideoWriter('output_%s.mp4' % time.time(), fourcc, cap.get(cv2.CAP_PROP_FPS) / 2, (w,h))

while cap.isOpened():
    # ret는 영상이 끝났을 때 false
    ret, img = cap.read()
    if not ret:
        break


# 영상에 효과를 주기
    if random.random() > 0.9:
        theta = random.randint(-3, 3)
        x, y = random.randint(-10,10), random.randint(-10,10)
        # 영상의 중심을 기준으로 회전하기
        M = cv2.getRotationMatrix2D(center=(w//2, h//2), angle=theta, scale=1.0)
        M[0, 2] += x
        M[1, 2] += y
        # 이미지를 기하학적 변형
        cv2.warpAffine(img, M=M, dsize=(w,h))
    #뿌옇도록 하는 효과
    img = cv2.GaussianBlur(img,ksize=(9,9), sigmaX=0)
    # 연필효과 주는 함수
    
    gray, color = cv2.pencilSketch(img, sigma_s=3, sigma_r=0.05, shade_factor=0.15)

    cv2.imshow('gray', gray)
    out.write(cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR))

    if cv2.waitKey(1) ==ord ('q'):
        break
# 영상 닫기
out.release()
cap.release()

