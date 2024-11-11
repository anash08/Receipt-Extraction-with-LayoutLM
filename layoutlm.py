import re
from transformers import LayoutLMForTokenClassification, LayoutLMTokenizer
import torch
from datetime import datetime


# Load pre-trained LayoutLM model and tokenizer
# tokenizer = LayoutLMTokenizer.from_pretrained("microsoft/layoutlm-base-uncased")
# model = LayoutLMForTokenClassification.from_pretrained("microsoft/layoutlm-base-uncased")
# Load fine-tuned LayoutLM model and tokenizer from the mounted directory
tokenizer = LayoutLMTokenizer.from_pretrained("/app/model")
model = LayoutLMForTokenClassification.from_pretrained("/app/model")


def normalize_bbox(bbox, width, height):
    x_min = min(bbox[0][0], bbox[3][0])
    y_min = min(bbox[0][1], bbox[1][1])
    x_max = max(bbox[1][0], bbox[2][0])
    y_max = max(bbox[2][1], bbox[3][1])

    return [
        int(1000 * (x_min / width)),
        int(1000 * (y_min / height)),
        int(1000 * (x_max / width)),
        int(1000 * (y_max / height)),
    ]



import re
import torch
from datetime import datetime

def extract_information(ocr_data, image_size):
    width, height = image_size
    words = [item['text'] for item in ocr_data]
    boxes = [normalize_bbox(item['bbox'], width, height) for item in ocr_data]

    # Tokenize input for LayoutLM
    encoding = tokenizer(words, boxes=boxes, return_tensors="pt", padding=True, truncation=True)

    with torch.no_grad():
        outputs = model(**encoding)

    logits = outputs.logits
    predictions = torch.argmax(logits, dim=2)

    extracted_info = {"company_name": "", "date": "", "address": "", "total_amount": ""}
    company_name_line = None  # Track line index where company name is found
    potential_dates = []      # Track potential dates
    potential_amounts = []    # Track all amounts found

    for idx, item in enumerate(ocr_data):
        text = item['text'].strip()

        # Extract Company Name: Look at the first few lines for potential company names
        if company_name_line is None and len(text) > 3 and re.match(r'^[a-zA-Z\s,.()&-]+$', text):
            extracted_info["company_name"] = text
            company_name_line = idx  # Save line index where company name was found
            continue

        # Extract Date: Capture all potential dates for later validation
        date_match = re.search(r'(\d{2}/\d{2}/\d{4}|\d{2}-\d{2}-\d{4}|\d{4}/\d{2}/\d{2}|\d{4}-\d{2}-\d{2})', text)
        if date_match:
            potential_dates.append(date_match.group(1))

        # Extract Address: Capture lines immediately following company name, up to a certain count
        if company_name_line is not None and company_name_line < idx <= company_name_line + 5:
            # Limit address extraction to a few lines after company name
            if text not in extracted_info["address"]:  # Avoid duplicate lines in address
                extracted_info["address"] += text + " "

        # Extract Total Amount: Collect all amounts and take the largest one at the end
        amount_match = re.search(r'(\d{1,3}(,\d{3})*(\.\d{2})?)', text)
        if amount_match:
            # Remove commas for comparison purposes
            amount_str = amount_match.group(1).replace(',', '')
            amount_value = float(amount_str)
            potential_amounts.append(amount_value)

    # Determine the most likely date (if multiple are found, choose the latest)
    if potential_dates:
        for date_str in potential_dates:
            try:
                date_obj = datetime.strptime(date_str, '%d-%m-%Y') if '-' in date_str else datetime.strptime(date_str, '%Y/%m/%d')
                extracted_info["date"] = date_obj.strftime('%Y-%m-%d')  # Use ISO format
                break
            except ValueError:
                continue

    # Determine the total amount as the largest amount found in potential amounts
    if potential_amounts:
        extracted_info["total_amount"] = "{:.2f}".format(max(potential_amounts))

    # Clean up extracted data
    extracted_info["company_name"] = extracted_info["company_name"].strip()
    extracted_info["date"] = extracted_info["date"].strip()
    extracted_info["address"] = extracted_info["address"].strip()
    extracted_info["total_amount"] = extracted_info["total_amount"].strip()

    return extracted_info

    width, height = image_size
    words = [item['text'] for item in ocr_data]
    boxes = [normalize_bbox(item['bbox'], width, height) for item in ocr_data]

    # Tokenize input for LayoutLM
    encoding = tokenizer(words, boxes=boxes, return_tensors="pt", padding=True, truncation=True)

    with torch.no_grad():
        outputs = model(**encoding)

    logits = outputs.logits
    predictions = torch.argmax(logits, dim=2)

    extracted_info = {"company_name": "", "date": "", "address": "", "total_amount": ""}
    company_name_line = None  # Track line index where company name is found
    potential_dates = []      # Track potential dates
    potential_amounts = []    # Track all amounts found

    for idx, item in enumerate(ocr_data):
        text = item['text'].strip()

        # Extract Company Name: Look at the first few lines for potential company names
        if company_name_line is None and len(text) > 3 and re.match(r'^[a-zA-Z\s,.()&-]+$', text):
            extracted_info["company_name"] = text
            company_name_line = idx  # Save line index where company name was found
            continue

        # Extract Date: Capture all potential dates for later validation
        date_match = re.search(r'(\d{2}/\d{2}/\d{4}|\d{2}-\d{2}-\d{4}|\d{4}/\d{2}/\d{2}|\d{4}-\d{2}-\d{2})', text)
        if date_match:
            potential_dates.append(date_match.group(1))

        # Extract Address: Capture lines immediately following company name, up to a certain count
        if company_name_line is not None and company_name_line < idx <= company_name_line + 5:
            # Limit address extraction to a few lines after company name
            if text not in extracted_info["address"]:  # Avoid duplicate lines in address
                extracted_info["address"] += text + " "

        # Extract Total Amount: Collect all amounts and take the largest one at the end
        amount_match = re.search(r'(\d{1,3}(,\d{3})*(\.\d{2})?)', text)
        if amount_match:
            # Remove commas for comparison purposes
            amount_str = amount_match.group(1).replace(',', '')
            amount_value = float(amount_str)
            potential_amounts.append(amount_value)

    # Determine the most likely date (if multiple are found, choose the latest)
    if potential_dates:
        for date_str in potential_dates:
            try:
                date_obj = datetime.strptime(date_str, '%d-%m-%Y') if '-' in date_str else datetime.strptime(date_str, '%Y/%m/%d')
                extracted_info["date"] = date_obj.strftime('%Y-%m-%d')  # Use ISO format
                break
            except ValueError:
                continue

    # Determine the total amount as the largest amount found in potential amounts
    if potential_amounts:
        extracted_info["total_amount"] = "{:.2f}".format(max(potential_amounts))

    # Clean up extracted data
    extracted_info["company_name"] = extracted_info["company_name"].strip()
    extracted_info["date"] = extracted_info["date"].strip()
    extracted_info["address"] = extracted_info["address"].strip()
    extracted_info["total_amount"] = extracted_info["total_amount"].strip()

    return extracted_info