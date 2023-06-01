import pyzbar.pyzbar as pyzbar  # pip install pyzbar
import numpy as np              # pip install numpy
import cv2                      # pip install opencv-python

# 바코드 찾는 엔진
def decode(im):
    # 바코드 찾기
    decodedObjects = pyzbar.decode(im)

    # 결과
    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', obj.data, '\n')

    return decodedObjects


# 바코드창 (QR)띄우기
def display(im, decodedObjects):
    for decodedObject in decodedObjects:
        points = decodedObject.polygon

        if len(points) > 4:
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points;

        
        n = len(hull)

        
        for j in range(0, n):
            cv2.line(im, hull[j], hull[(j + 1) % n], (255, 50, 100), 3)

  
    cv2.imshow("Results", im);
    cv2.waitKey(0);

# 파일명 QR.jpg의 이미지에서 바코드를 탐지하면 해당 코드를 리턴
# Main
if __name__ == '__main__':
    # Read image
    im = cv2.imread('QR.jpg')

    decodedObjects = decode(im)
    display(im, decodedObjects)


