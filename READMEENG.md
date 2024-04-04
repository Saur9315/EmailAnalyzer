# Email Analyzer Project


## Overview

The Email Analyzer project is designed to retrieve and analyze email messages. It involves components for email retrieval, machine learning-based analysis, and interaction with a PostgreSQL database.

## Prerequisites

Make sure you have the required dependencies installed. You can install them using the following command:

```
pip install -r requirements.txt
```

## Configuration

The configuration for the project is managed through the '.env' file. Make sure to fill in the necessary information before running the project.

```
EMAIL_ADDRESS='email address'
PASSWORD='email password'

CLIENT_EMAIL_LIST="customer email list"

DATA_GENERATOR=True/False
NUM_SENTENCES_PER_LABEL=int

MODEL_PATH='model/model_name.joblib'
VECTORIZER_PATH='model/vectorizer_name.joblib'
TRAIN_THE_MODEL=True/False
```

The configuration of database is through the 'database.ini' file.
```
[postgresql]
host=localhost
database='database name'
user='username'
password='database password'
port=5432
```

## Running the Project

To run the entire project, run the main.py file. This script performs the following tasks:

1. Reads and extracts information from email messages.
2. Analyzes the content of emails and predicts their labels using a trained machine learning model.
3. Stores results, including sender information, email subject lines, predicted labels, and other relevant information, in a database.

Make sure you fill out the required configurations in the .env file, including email credentials, client email list, and database configurations.
```
python main.py
```

***

# Project Structure

- main.py: processes email searches, performs analysis and classification of incoming messages, interacts with the database.
- ml_model.py: contains functions for training and prediction using a machine learning model.
- temp_data_generator.py: generates synthetic data for training a machine learning model (replace with suitable data).
- db_config.py: manages database creation, table creation, data recording and updating.
- .env: project configuration file.
