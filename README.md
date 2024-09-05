# ABC-TECHNICAL-INTERVIEW-CHALLANGE
 A project to show my technical understanding of software development principles/practices

# Motor Vehicle Maintenance Application

## Overview

This project involves developing a motor vehicle maintenance application for a service station. The application includes features to manage vehicle maintenance data, store and retrieve files, and compress images.

## Features

1. **Motor Vehicle Maintenance Application**
   - **Database Design**: Schema for managing owners, vehicles, and service details.
   - **SQL Queries**:
     - **Fetch Service Activities**: Retrieve a list of service activities with vehicle models, registrations, owner names, and service costs, ordered by the service date.
     - **Owner Statistics**: List owners with the number of services performed and the total amount spent, ordered by the highest spender.
     - **Vehicle Models**: List vehicle models with their service frequency and total income generated, ordered by the most frequently serviced models.

2. **File Server Development**
   - **Image Compression**: Functionality to compress images before storing them to save space.
   - **Endpoints**:
     - **Upload File**: Endpoint to upload files.
     - **Delete File**: Endpoint to delete files.
     - **List File Metadata**: Provides metadata for all stored files including file name, URL, size, and upload date.
     - **File Summary**: Summary of the total number of files and total storage used.
   - **Security**: Implementation of security measures to ensure safe file handling.
   - **Caching**: Strategies to improve efficiency and performance.

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ThiraTheNerd/ABC-TECHNICAL-INTERVIEW-CHALLANGE.git
   cd vehicle_maintenance_service

2. **Install Dependencies**
    ```bash
    pip install -r requirements.txt

3. **Run Migrations**
    ```bash
    python manage.py migrate

2. **Run the Server**
    ```bash
    python manage.py runserver 

## Access the Application

 - The application will be available at
    ```bash
    http://127.0.0.1:8000/