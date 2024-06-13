# Movie API

## Overview

This application provides a RESTful API to load and export movie data. The data can be loaded from CSV or XLSX files and exported in the same formats.

## Project Structure

```bash
movie-api/
│
├── app.py
├── IMDBMovies2000-2020.csv
├── IMDBMovies2000-2020.xlsx
├── config.py
├── requirements.txt
├── migrations/
│   └── ... (migration files)
├── instance/
│   └── movie.db
├── tests/
│   └── test_app.py
│   └── test_data.csv
├── init-db.sh
└── README.md
```
## Requirements

- Python 3.x
- Flask
- pandas
- Flask-Migrate
- Flask-SQLAlchemy
- pytest

## Setup

1. **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Initialize the migration environment and create the database:**

    Run the following script to set up the database:

    ```bash
    ./init-db.sh
    ```

5. **Run the application:**

    ```bash
    python app.py
    ```

## API Endpoints

### Load Data

- **Endpoint:** `/load-data`
- **Method:** `POST`
- **Description:** Load data from a CSV or XLSX file.
- **Example:**

    ```bash
    curl -F 'file=@IMDBMovies2000-2020.csv' http://127.0.0.1:5000/load-data
    ```

### Export Data

- **Endpoint:** `/export-data`
- **Method:** `GET`
- **Description:** Export data to a CSV or XLSX file.
- **Parameters:**
    - `format`: Specify the export format (`csv` or `xlsx`). Default is `csv`.
- **Example:**

    ```bash
    curl http://127.0.0.1:5000/export-data?format=csv -o exported_data.csv
    ```

## Running Tests

1. **Ensure you have the required dependencies installed:**

    ```bash
    pip install pytest
    ```

2. **Run the tests:**

    ```bash
    pytest
    ```

## Bash Script for Database Initialization

A bash script named `init-db.sh` initialize the database:

### `init-db.sh`

```bash
#!/usr/bin/env bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

### Summary

1. **Clone the repository** and navigate to the project directory.
2. **Create a virtual environment** and activate it.
3. **Install required packages** using `pip install -r requirements.txt`.
4. **Initialize the database** by running the `init-db.sh` script.
5. **Run the application** using `python app.py`.
6. **Use the API** to load and export data.
7. **Run tests** using `pytest` to ensure everything is working correctly.