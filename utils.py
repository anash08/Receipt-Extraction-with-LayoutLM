import json

def generate_json_output(extracted_info, filename):
    return json.dumps({
        "company_name": extracted_info["company_name"].strip(),
        "date": extracted_info["date"].strip(),
        "address": extracted_info["address"].strip(),
        "total_amount": extracted_info["total_amount"].strip(),
        "filename": filename
    }, indent=4)
