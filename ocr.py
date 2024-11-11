from paddleocr import PaddleOCR
import cv2
import numpy as np

ocr = PaddleOCR(use_angle_cls=True, lang='en')

def extract_text_from_receipt(img_bytes):
    img_np = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    height, width, _ = img.shape

    result = ocr.ocr(img, cls=True)
    ocr_data = [{"text": word_info[1][0], "bbox": word_info[0]} for line in result for word_info in line]
    
    return ocr_data, (width, height)
