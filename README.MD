# AI Image Generator with ComfyUI

This project is a simple AI image generator using ComfyUI, FastAPI, and Streamlit.
Uses sdxl1 with LoRA tuning.
Trained and tested on ComfyUI



![Workflow Screenshot](https://raw.githubusercontent.com/RaviKiran752/comfypy/main/Screenshot%20From%202025-03-29%2003-13-19.png)


Picture of the workflow used


## Features
- Generates images using LoRA tuning
- FastAPI backend for AI model processing
- Streamlit UI for user interaction
- Uses WebSockets for communication with ComfyUI

## Requirements
- Python 3.8 or later
- Required dependencies listed in `requirements.txt`

## Installation
1. Clone the repository  

cd comfypy

2. Install dependencies  

pip install -r requirements.txt


## How to Run
1. Start the FastAPI backend  

uvicorn api_workflow:app --reload

2. Start the Streamlit UI  

streamlit run stremlit_ui.py

3. Enter a prompt and generate images  

## API Usage
The FastAPI backend provides an endpoint for generating images.  
- **Endpoint**: `POST /generate`
- **Request Body** (JSON):
```json
{
 "positive_prompt": "A futuristic cyberpunk city",
 "negative_prompt": "low quality, bad composition",
 "seed": 123456,
 "lora_strength": 0.7
}

// Response (JSON):
{
  "images": ["base64_encoded_image_string"]
}


