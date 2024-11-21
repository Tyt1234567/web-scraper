import cv2
image=cv2.imread('CAPTCHA.png')
kernel_size = (5,5)
blurred_image = cv2.GaussianBlur(image,kernel_size,0)#模糊处理


edges = cv2.Canny(blurred_image,200,450)#边缘检测




contours, hierarchy = cv2.findContours(edges, cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)#轮廓提取
#cv2.drawContours(image,contours,-1,(0,0,0),3)#描绘轮廓




#筛选符合的验证码（通过预先计算的面积）
height, width = image.shape[:2]
optimized_area = [height*width*0.25*0.15*0.8, height*width*0.25*0.15*1.2]
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)  # 外接矩形
    if optimized_area[1]>cv2.contourArea(contour)>optimized_area[0]:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), 4)  # 描绘矩形


cv2.imshow('square',image)
cv2.waitKey(0)
cv2.destroyAllWindows()





'''
for contour in contours:
    x,y,w,h = cv2.boundingRect(contour)#外接矩形


    cv2.rectangle(image,(x,y), (x+w, y+h), (0,0,0), 2)#描绘矩形

    print(cv2.contourArea(contour))
    print(cv2.arcLength(contour,1))

cv2.imshow('image',image)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''