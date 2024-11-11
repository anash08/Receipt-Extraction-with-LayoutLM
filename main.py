from fastapi import FastAPI, File, UploadFile
from ocr import extract_text_from_receipt
from layoutlm import extract_information
from utils import generate_json_output
import json
import time  # Import the time module

app = FastAPI()

@app.post("/upload_receipt/")
async def upload_receipt(file: UploadFile = File(...)):
    # Read and record the start time
    img_bytes = await file.read()
    start_time = time.time()  # Start timer

    # Perform OCR and extraction
    ocr_data, image_size = extract_text_from_receipt(img_bytes)
    extracted_info = extract_information(ocr_data, image_size)
    json_output = generate_json_output(extracted_info, file.filename)

    # Record the end time and calculate the processing time
    end_time = time.time()  # End timer
    processing_time = end_time - start_time  # Calculate elapsed time

    # Include processing time in the response
    response = json.loads(json_output)
    response["processing_time_seconds"] = processing_time

    return response
