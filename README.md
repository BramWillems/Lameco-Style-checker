Lameco Style Checker
Project Overview

The Lameco Style Checker is a Python-based web application developed as part of a school assignment and is intended to be transferred to a company for further development or evaluation.

The application provides a web interface where users can check the styling of documents against configurable settings. It is hosted using FastAPI and integrates with an external AI API to assist with document analysis.

This repository contains the complete source code for the project.

Project Status

Status: Prototype / Proof of Concept

Purpose: Educational project handed over for potential continuation

Production-ready: No (additional security, testing, and configuration required)

Functionality

Web-based interface for document style checking

FastAPI backend for hosting and routing

Configurable style validation settings

External AI API integration (currently Sapling)

Technology Stack

Python

FastAPI

Uvicorn

External AI API (Sapling – configurable)

Local Setup
Prerequisites

Python 3.9 or higher

pip

git

Installation Steps
git clone https://github.com/BramWillems/Lameco-Style-checker
cd Lameco-Style-checker
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

Running the Application

For local development, start the server using:

uvicorn app.main:app --reload


The application will be available at:

http://127.0.0.1:8000

Deployment

For deployment on a server, the host and port can be configured manually:

uvicorn app.main:app --host 127.0.0.1 --port 9000


Further deployment steps such as reverse proxy configuration, HTTPS, and process management (e.g. systemd or Docker) are not included and must be set up separately.

API Key & Configuration
External AI API

The application relies on an external AI API for document analysis.

The API key is defined in app/api.py

The current implementation is configured for Sapling API

The API key must be replaced with a company-owned key before use

Switching to OpenAI (ChatGPT)

If the company wishes to use OpenAI (ChatGPT) instead of Sapling:

Changes will be required in app/api.py

Adjustments mainly involve:

Endpoint URL

Authentication headers

Request/response format

Only minimal structural changes should be necessary

Project Structure
Lameco-Style-checker/
├── app/
│   ├── main.py        # FastAPI entry point
│   ├── api.py         # External API integration
│   └── ...
├── requirements.txt   # Python dependencies
└── README.md

Known Limitations

No authentication or user management

Limited error handling

No automated test suite

API keys currently hardcoded (should be moved to environment variables)
