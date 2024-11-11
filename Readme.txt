Receipt Extraction with LayoutLM and PaddleOCR

This project extracts structured data from receipt images using a fine-tuned LayoutLM model and PaddleOCR. The extracted data includes fields like company name, date, address, and total amount, and outputs them in JSON format.

Project Structure

    layoutlm.py: Contains functions to load the LayoutLM model and perform information extraction from OCR data.
    ocr.py: Uses PaddleOCR to detect and extract text from images.
    utils.py: Provides utility functions, including JSON output formatting.
    main.py: Sets up a FastAPI server to handle receipt image uploads and return extracted data.
    Dockerfile: Defines the Docker environment for running the application.
    docker-compose.yml: Configuration to build and run the application in a containerized environment.
    
Prerequisites
    
    Docker and Docker Compose
    Python 3.9+ (if running locally)
    A fine-tuned LayoutLM model saved in D:/receipt_extract/output


 Download the Zip File 
    
    open cmd 
    tar -xf "C:\path\to\your\file.zip" -C "C:\path\to\extract\"
    cd OCR_llm   


Step 2: Prepare the Fine-Tuned Model
    Ensure your fine-tuned model files (e.g., pytorch_model.bin, config.json, etc.) are stored in OCR_llm\layoutlm-base-uncased or update the docker-compose.yml volume path accordingly.

Step 3: Build and Run the Docker Container
Using Docker Compose
    1:Run the following command to build and start the container:

        "docker-compose up --build"

    2:Once started, the application will be available at 
        "http://localhost:8000"
        "http://localhost:8000/docs"



Step 4: Test the API
    You can test the API by sending a POST request to /upload_receipt/ with an image file:

    "curl -X POST "http://localhost:8000/upload_receipt/" -F "file=@/path/to/your/receipt_image.jpg""



Troubleshooting

    1:Error Loading Model: If you see warnings or errors about missing weights, ensure that the model directory (layoutlm-base-uncased) contains a fully fine-tuned LayoutLM model suitable for token classification tasks.

    2:Adjust Docker Volume Path: If using a different directory for your model files, update the docker-compose.yml file accordingly.

    3:Running Issues on Windows: Ensure that Docker is configured to access Windows paths, and double-check path formatting in docker-compose.yml.
    
