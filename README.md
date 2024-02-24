
# Home Archive: Empowering Families with Private GenAI

## Project Description

Home Archive is an innovative project designed to revolutionize the way families manage and utilize their documents within the privacy of their own home network. Gone are the days of overflowing file cabinets and lost documents. With Home Archive, families can now digitize legal, financial, medical, academic, and tax documents, freeing up physical space and ensuring that important papers are never misplaced or thrown away unknowingly.

This project is more than just a digital storage solution; it's a private hub for families to securely upload and manage documents without the fear of external internet exposure. At its core, Home Archive leverages the power of Generative AI (GenAI) to provide families with the ability to analyze, ask questions, summarize, and gain insights from their stored documents. Whether it's understanding financial health, tracking a child's academic progress, or building a personalized knowledge base, the possibilities with Home Archive are limitless.

## Technical Overview

Home Archive is built as a web application using Flask, providing a user-friendly interface for document management. The backend is powered by a comprehensive API, named `all_api`, which includes both `llm_api` for GenAI interactions and additional functionalities. This setup ensures that all processing is done locally, maintaining privacy and data security.

Running on a robust Windows 11 PC equipped with a 3090 Ti GPU, Home Archive offers fast and efficient processing capabilities for GenAI tasks, even for large volumes of data. This local deployment model ensures that your family's data never leaves your home network, aligning with our commitment to privacy and security.

## Join Us

Dive into the future of document management and family knowledge building with Home Archive. Explore the endless possibilities of leveraging GenAI privately within your home. Start your journey today by visiting our GitHub repository for installation instructions and more.

# Home Archive Application Architecture

This document outlines the architecture of the Home Archive application, designed to allow families to privately manage their home documents with AI-enhanced features for insights, summarization, and question-answering capabilities.

## System Overview

The application is structured into two main layers: the Web Layer and the API Layer. These interact with the TRT Engine to leverage the LLAMA2 13B 4Bit AMQ Model on an NVIDIA 3090 Ti GPU for processing.

```
User
  |
  v
Web Layer (Flask)
  |
  v
API Layer (Flask RESTful)
  |
  v
TRT Engine (LLAMA2 13B 4Bit AMQ Model)
  |
  v
NVIDIA 3090 Ti GPU
```

## Components Description

- **User**: The end-user interface for uploading, managing, and interacting with home documents.
- **Web Layer**: Built using Flask, this layer handles user interactions, serving as the frontend of the application.
- **API Layer**: Also built with Flask RESTful, it exposes the functionalities of the TRT Engine to the Web Layer, acting as a bridge between the frontend and the AI processing backend.
- **TRT Engine**: Utilizes the LLAMA2 13B 4Bit AMQ Model for AI-based document processing, including summarization and question-answering.
- **NVIDIA 3090 Ti GPU**: Provides the computational power needed to accelerate AI inferences with the TRT Engine and the LLAMA2 model.

## Workflow

1. Users interact with the Web Layer to upload and manage documents.
2. The Web Layer communicates with the API Layer to process these documents.
3. The API Layer utilizes the TRT Engine, leveraging the LLAMA2 model for AI-enhanced document processing.
4. The TRT Engine performs the heavy lifting of AI computations on the NVIDIA 3090 Ti GPU, ensuring fast and efficient processing.
5. Processed data is sent back through the layers to the user, providing insights and answers derived from their documents.

## GitHub Repository Structure

The GitHub repository for Home Archive is structured as follows: [Home Archive GitHub Repository](https://github.com/tarunchy/rtx-home-archive)

- `llm_api`: This folder contains the Flask-based application responsible for exposing the LLMA2 model as an API. It serves as the backend for GenAI interactions.
- `web_app`: This folder houses the main web application built with Flask, which consumes the `llm_api` and provides the user interface for document management.
- `sample_data`: Contains sample documents and data for testing and demonstration purposes.

Each of the `llm_api` and `web_app` directories includes a `start.bat` file, which simplifies the process of setting up and running the application. Running this batch file takes care of creating the necessary conda environment and starting the app, ensuring a smooth setup process.

## Getting Started

For detailed installation instructions, starting the application, and exploring its features, please refer to the `README.md` files within the `llm_api` and `web_app` folders of the GitHub repository.



