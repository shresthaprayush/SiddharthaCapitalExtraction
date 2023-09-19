# import numpy as np
#
# import cv2
#
# image = cv2.imread('sc.png',1)
#
# image_bw = cv2.imread('sc.png',0)
#
# noiseless_image_bw = cv2.fastNlMeansDenoising(image_bw, None, 20, 7, 21)
#
# noiseless_image_colored = cv2.fastNlMeansDenoisingColored(image,None,20,20,7,21)
#
# cv2.imwrite("scnoisereomoved.jpg", noiseless_image_bw)
