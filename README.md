# Enterprise IDWMS v2

**Intelligent Document & Workflow Management System (IDWMS)**

A professional desktop-based document management system developed using **Python, PostgreSQL, CustomTkinter, OCR, AI-based document classification, workflow automation, version control, PDF preview, and audit logging**.

This project is designed as an **enterprise-level document repository and workflow management solution** suitable for organizations that need secure document storage, approval workflows, OCR extraction, AI-assisted search, and complete audit trails.

## Features

### User management

* Role-based login (Admin, Approver, User)
* Secure authentication
* User session handling

### Document repository

* Upload PDF, PNG, JPG, DOCX, and TXT files
* Automatic file storage
* Category-based organization
* Document search
* File preview and opening

### OCR and AI

* OCR text extraction from images
* Automatic document classification
* Smart text search
* AI-assisted document processing

### Workflow management

* Submit documents for approval
* Approve / Reject workflow
* Workflow history
* Pending workflow tracking

### Version control

* Automatic version creation
* Version history
* Document update tracking
* Previous version records

### PDF preview

* In-app PDF preview
* First-page rendering
* Image preview support

### Audit logging

* Document upload logs
* Document delete logs
* Workflow submission logs
* Approval logs
* Rejection logs
* Complete activity history

### Analytics dashboard

* Total documents
* Pending workflows
* Approved workflows
* Rejected workflows
* Category statistics
* Recent document activity

## Technology stack

### Backend

* Python 3.13
* PostgreSQL
* Psycopg2

### GUI

* CustomTkinter

### OCR

* Tesseract OCR
* pytesseract

### PDF

* PyMuPDF (fitz)
* Pillow

### Build

* PyInstaller

## Project structure

IDWMS/

* app.py
* database.py
* gui/
* services/
* storage/
* dist/
* requirements.txt
* README.md

## Installation

### Clone the project

git clone https://github.com/yourusername/enterprise-idwms-v2.git

cd enterprise-idwms-v2

### Create virtual environment

python -m venv venv

venv\Scripts\activate

### Install dependencies

pip install -r requirements.txt

### Configure PostgreSQL

Create a PostgreSQL database and update the connection settings in database.py.

### Run

python app.py

## Build EXE

Run:

build_exe.bat

The executable will be generated in:

dist/Enterprise_IDWMS_v2.exe

## Default login

### Admin

Username: admin

Password: admin123

## Database modules

* users
* documents
* document_versions
* workflows
* workflow_history
* audit_logs

## Future improvements

* Digital signature
* Email notifications
* QR code verification
* Cloud storage integration
* Multi-factor authentication
* AI document summarization
* REST API
* Web dashboard
* Mobile application

## Author

Ratul Hasan

Department of Computer Science & Engineering

Final Year Project

## License

This project is developed for educational and research purposes.
