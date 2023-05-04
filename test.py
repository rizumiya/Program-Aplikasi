# import cv2
# import numpy as np

# img = cv2.imread('approx.png')
# img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ret,thresh = cv2.threshold(img1,127,255,0)
# contours,_ = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# # print("Number of contours detected:", len(contours))
# cnt = contours[0]

# # compute straight bounding rectangle
# x,y,w,h = cv2.boundingRect(cnt)
# img = cv2.drawContours(img,[cnt],0,(255,255,0),2)
# img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

# # compute rotated rectangle (minimum area)
# rect = cv2.minAreaRect(cnt)
# box = cv2.boxPoints(rect)
# box = np.int0(box)

# # draw minimum area rectangle (rotated rectangle)
# img = cv2.drawContours(img,[box],0,(0,255,255),2)
# cv2.imshow("Bounding Rectangles", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# ========================================================================================

import cv2
import numpy as np

def process_img(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_canny = cv2.Canny(img_gray, 100, 100)
    kernel = np.ones((2, 3))
    img_dilate = cv2.dilate(img_canny, kernel, iterations=1)
    img_erode = cv2.erode(img_dilate, kernel, iterations=1)
    return img_erode
    
def get_centeroid(cnt):
    length = len(cnt)
    sum_x = np.sum(cnt[..., 0])
    sum_y = np.sum(cnt[..., 1])
    return int(sum_x / length), int(sum_y / length)

def get_centers(img):
    contours, hierarchies = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        if cv2.contourArea(cnt) > 100:
            yield get_centeroid(cnt)

def get_rows(img, centers, row_amt, row_h):
    centers = np.array(centers)
    d = row_h / row_amt
    for i in range(row_amt):
        f = centers[:, 1] - d * i
        a = centers[(f < d) & (f > 0)]
        yield a[a.argsort(0)[:, 0]]

img = cv2.imread("p.jpg")
img = cv2.resize(img, (600, 800))
img_processed = process_img(img)
centers = list(get_centers(img_processed))

h, w, c = img.shape
count = 0

for row in get_rows(img, centers, 1, h):
    cv2.polylines(img, [row], False, (255, 0, 255), 2)
    for x, y in row:
        count += 1
        cv2.circle(img, (x, y), 10, (0, 0, 255), -1)  
        cv2.putText(img, str(count), (x - 10, y + 5), 1, cv2.FONT_HERSHEY_PLAIN, (0, 255, 255), 2)

cv2.imshow("Ordered", img)
cv2.waitKey(0)