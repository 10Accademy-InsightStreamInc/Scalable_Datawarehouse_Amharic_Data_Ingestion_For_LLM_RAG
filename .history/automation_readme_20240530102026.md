# Amharic Language NLP Pipeline

This repository contains the implementation of an automated pipeline for Natural Language Processing (NLP) tasks focusing on the Amharic language. The pipeline is designed to collect, clean, process, and store Amharic language data, enabling various NLP applications.

## Overview

The project aims to enhance NLP capabilities for the Amharic language by automating the entire data pipeline using Apache Airflow, Docker, and other tools. The pipeline includes stages for data collection, cleaning, processing, storage, and access.

## Workflow Overview

The workflow is orchestrated using Apache Airflow and containerized using Docker for seamless deployment and scalability. Here's an overview of the workflow:

1. **Data Collection**: Collect Amharic language data from various online sources such as news websites, blogs, and social media platforms.

2. **Data Cleaning**: Pre-process the collected data to ensure quality and relevance, including tasks like text normalization, tokenization, and removing noise.

3. **Data Processing**: Perform NLP tasks such as semantic analysis, sentiment analysis, and topic modeling on the cleaned data.

4. **Data Storage**: Store the processed data in a structured database for easy access and retrieval.

5. **API Development**: Develop APIs to facilitate seamless integration and querying of the dataset for NLP applications.

## Repository Structure

scalable_data_warehouse/
│
├── dags/
│   ├── data_collection.py     # Airflow DAG for data collection
│   └── data_processing.py     # Airflow DAG for data processing
│
├── tests/
│   ├── test_data_cleaning.py  # Unit tests for data cleaning
│   └── test_data_collection.py# Unit tests for data collection
│
├── Dockerfile                  # Dockerfile for main application
├── Dockerfile.api              # Dockerfile for API component
├── Dockerfile.cleaning         # Dockerfile for data cleaning component
├── Dockerfile.collection       # Dockerfile for data collection component
├── docker-compose.yaml         # Docker Compose file for orchestration
├── prometheus.yml              # Prometheus configuration
├── plugins/                    # Airflow plugins
│
├── app/
│   ├── main.py                 # API entry point
│   ├── routes/                 # API routes
│   ├── view_models/            # Pydantic models (schemas)
│   ├── controllers/            # Business logic
│   └── models/                 # SQLAlchemy models
│
├── data/
│   └── raw/
│       ├── alain_news.csv      # Raw data files
│       └── ...
│
├── schema/
│   ├── news_schema.sql         # SQL schema for news
│   └── ...
│
├── db/
│   └── connection/
│       └── db_connection.py    # Database connection script
│
├── scrapper/
│   ├── news_sites/             # News sites scrapping scripts
│   ├── telegram/               # Telegram Scrapping scripts
│   ├── other/                  # Other sites scripts
│   └── ...
│
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation


## Getting Started

To get started with the pipeline, follow these steps:

1. **Install Docker and Docker Compose on your system**:
   - **Ubuntu**: Follow the instructions [here](https://docs.docker.com/desktop/install/ubuntu/).
   - **Windows**: Follow the instructions [here](https://docs.docker.com/desktop/install/windows-install/).
   - **Mac**: Follow the instructions [here](https://docs.docker.com/desktop/install/mac-install/).

2. **Clone this repository**:
   ```sh
   git clone https://github.com/MoraaOntita/Scalable_Datawarehouse_Amharic_Data_Ingestion_For_LLM_RAG/tree/automation_branch`

3. **Navigate to the repository directory**:
    `cd Scalable_Datawarehouse_Amharic_Data_Ingestion_For_LLM_RAG`

4. **Start the pipeline using Docker Compose**:
    `docker-compose up`

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these guidelines:

- Fork the repository on GitHub.
- Make your changes and commit them to your fork.
- Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the [MIT License](LICENSE).