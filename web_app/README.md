# Home Archive

## Overview
Home Archive empowers families to leverage General AI within their private home network, offering a secure and private way to manage important documents like legal, financial, medical, academic, and tax records. Forget the days of keeping stacks of paper; Home Archive transforms your document management with AI, enabling you to analyze, ask questions, summarize, and gain insights—all within your home's digital space.

## Features
- **Private Document Management**: Securely upload and store documents within your home network, ensuring privacy and accessibility.
- **AI-Powered Insights**: Utilize General AI to analyze documents for financial insights, academic progress, and more.
- **Question and Answer System**: Easily query your document archive to find exactly what you need, when you need it.
- **Local Knowledge Base**: Build a personal knowledge base to explore possibilities and insights unique to your family's needs.

## Architecture
Home Archive consists of a web application built with Flask, interfacing with a backend API called `llm_api`. The system runs locally on a Windows 11 PC equipped with an NVIDIA RTX 3090 Ti GPU, ensuring fast and private processing.

### Components
- **Web App (Flask)**: A user-friendly interface for document management and interaction. It also handles Handles document processing, AI interactions, and data storage.
- **Backend API (`llm_api`)**: This API Layer exposes LLAMA 2 LLM as REST API with OpenAI compatible Chat Completion Interface
- **LLM API**: Powers the AI-driven features, including document analysis and Q&A functionalities.

## Installation
### Prerequisites
- Windows 11 PC with an NVIDIA RTX 3090 TI GPU.
- NVIDIA CUDA Toolkit (Version 12.2.1)
- NVIDIA TensorRT-LLM (Version 0.7.0)
- Python 3.10.13

### Setup
1. Clone the repository:
