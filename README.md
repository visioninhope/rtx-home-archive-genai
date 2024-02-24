
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
