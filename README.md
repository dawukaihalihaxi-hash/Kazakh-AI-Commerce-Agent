# Kazakh AI Commerce Agent

AI-powered product marketing assistant for Kazakh e-commerce sellers.

This project uses multimodal AI agents to transform product images and descriptions into localized marketing content and short-video generation workflows.


## Overview

Many small sellers have products but struggle with:

- How to analyze product advantages
- How to create short-video scripts
- How to produce localized marketing content
- How to use AI tools effectively


Kazakh AI Commerce Agent provides an automated workflow:

Product Image
↓
AI Vision Analysis
↓
Product Understanding
↓
Marketing Script Generation
↓
AI Video Generation


## Features

### 1. Multimodal Product Understanding

Upload product images and descriptions.

The system analyzes:

- Product category
- Features
- Selling points
- Target customers
- Marketing opportunities


### 2. AI Marketing Script Generation

Generate localized short-video scripts.

Supported scenarios:

- Kazakh market
- Social commerce
- Short-video marketing


### 3. AI Video Generation Pipeline

Connect generated scripts with video generation models.

Workflow:

Script
+
Product Image
↓
AI Video Model
↓
Generated Marketing Video




## AI Models

Current implementation:

- GLM multimodal model
- GLM text generation model
- AI video generation model


## Tech Stack

- Python
- Flask
- REST API
- Multimodal AI
- LLM Agents


## Run Locally


Install dependencies:

```bash
pip install -r requirements.txt

## Open

http://127.0.0.1:8000
