# Standalone LOA Stub API

This project is a Flask-based stub API that simulates a third‑party system
returning Letter of Authorization (LOA) documents as PDF files.

## Features
- Returns actual PDF documents
- Mimics real document APIs using Content-Disposition headers
- Strict request validation
- Swagger UI for API exploration


## Setup
py -m venv venv
venv\Scripts\activate
py -m pip install -r requirements.txt

## Run
py standalone_stub_api.py

## Endpoint
POST /lookup
Request:
{
  "id": 1001
}

Response:
- 200: PDF file download
- 400/404: JSON error response

## Swagger
http://127.0.0.1:5000/swagger