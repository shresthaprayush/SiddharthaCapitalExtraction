# import cv2
# import pytesseract
#
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#
# image = cv2.imread("scnoisereomoved.jpg", cv2.IMREAD_GRAYSCALE)
# cv2.dilate(image, (5, 5), image)
# print('Image Extracted Value')
# print(f'{pytesseract.image_to_string(image)}')