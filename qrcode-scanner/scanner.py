import cv2
# pyzbar 가져오기
import pyzbar.pyzbar as pyzbar
import matplotlib.pyplot as plt




# 이미지를 불러오기
img = cv2.imread('QR.jpg')

# BRG2GRAY
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# 이미지를 확인해보기
#plt.imshow(img)
# plt.imshow(gray,cmap='gray')

# matplotlib 실행하기
# plt.show()

# pyzbar로 decode를 해주기
decoded = pyzbar.decode(gray)

for d in decoded:
    #print(d.type)
    print(d.data)
    print(d.data.decode('utf-8'))

    cv2.rectangle(gray,(d.rect[0],d.rect[1]),(d.rect[0]+d.rect[2],d.rect[1]+d.rect[3]),(0,0,255),10)

plt.imshow(gray,cmap='gray')
plt.show()