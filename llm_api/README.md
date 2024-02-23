# Project Title: Accelerated LLM API Layer for Home Document Management

## Overview
This project focuses on leveraging the power of Generative AI for private Home Document Management through an accelerated LLM API Layer. Our process involves obtaining the base model of Llama2, exporting it as ONNX, creating an accelerated model using NVIDIA's AMQ framework, and building a TensorRT (TRT) engine for a Windows 11 PC equipped with an RTX 3090 TI GPU. We then load this TRT engine and the original tokenizer using NVIDIA's TensorRT inference framework. Our API, built using Flask, is designed to align with the OpenAI Chat Completion interface API, ensuring seamless integration and operation entirely locally on a Windows 11 PC.

### Key Features:
- **Base Model Acquisition:** Retrieve the Llama2 base model for initial setup.
- **ONNX Export:** Convert the base model to the ONNX format for compatibility with various acceleration frameworks.
- **Acceleration with NVIDIA AMQ:** Utilize NVIDIA's AMQ framework to enhance model performance significantly.
- **TensorRT Engine Building:** Construct a TRT engine optimized for Windows 11 PCs with RTX 3090 TI GPUs, focusing on efficient inference.
- **API Exposure with Flask:** Deploy a Flask-based API that mirrors the OpenAI Chat Completion interface, facilitating easy integration and use.

## Setup and Installation

### Prerequisites:
- Windows 11 PC with an NVIDIA RTX 3090 TI GPU.
- NVIDIA CUDA Toolkit (Version 12.2.1)
- NVIDIA TensorRT-LLM (Version 0.7.0)
- Python 3.10.13

### Step-by-Step Guide:

1. **Base Model Preparation:**
   - Download the Llama2 model from Huggingface.
   - Ensure the model is compatible with the requirements for ONNX export.

2. **Exporting to ONNX:**
   - Use the provided script to convert the base model to ONNX format.

3. **Creating Accelerated Model:**
   - Follow NVIDIA's AMQ framework documentation to accelerate the ONNX model.

4. **Building the TRT Engine:**
   - Utilize the script  with your specific GPU architecture in mind.

5. **Loading the TRT Engine and Tokenizer:**
   - Ensure the NVIDIA TensorRT inference framework is properly installed.
   - Use the script to initialize the engine and tokenizer.

6. **API Deployment:**
   - Navigate to the Flask application directory.
   - Run app.py with start.bat script to start the server. 

### Setup
1. Clone the repository
2. cd llm_api and run start.bat

## Usage

To interact with the deployed model API, send POST requests to the relevant endpoints. 
e.g. http://localhost:8081/models/Llama2


## Acknowledgments

- NVIDIA for providing the AMQ framework and TensorRT.
- The creators of Llama2 for their foundational work in generative AI.


