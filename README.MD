# intelia ML SPecialization Demo#3: Vector Match Job Search Conversational AI Agent

## Description

This project builds a conversational AI agent powered by a data processing pipeline that analyzes job postings from Kaggle. The system leverages natural language processing and vector search to answer user queries about available jobs.

## Architecture
![System Architecture]('architecture.png')
### Data Source:

- A dataset of job postings from Kaggle.

### Data Ingestion:

- **Cloud Storage bucket:** Acts as a temporary landing zone for data.
- **Cloud Function:** Triggered by upload, ingests data into BigQuery tables.

### Data Processing and Embeddings:

- **BigQuery tables:** Store both raw and processed data.
- **Cloud Functions:** Handle various tasks:
  - Generating embeddings for job descriptions using two modes:
    - Vertex AI Batch Embeddings: Generates embeddings for large datasets.
    - Pre-trained model: Uses a pre-trained model for efficient embedding generation.
  - Creating and managing a Vector Search index based on generated embeddings.
- **Google Drive folders:** Store user data and Vertex AI outputs.

### Vector Search and Dialogflow Integration:

- **Vector Search index:** Points to the GCS bucket containing job description embeddings.
- **Dialogflow CX agent:** Handles user interactions and processes queries.
- **Cloud Function:** Acts as a webhook for Dialogflow.
- **BigQuery tables:** Store Dialogflow export and user interaction data.

## Technologies

- **Google Cloud Platform (GCP):**
  - **Cloud Storage:** For temporary data storage.
  - **Cloud Functions:** For event-driven data processing.
  - **BigQuery:** For scalable data warehousing.
  - **Vertex AI Batch Embeddings:** For efficient large-scale embedding generation.
  - **Dialogflow CX:** For building and deploying conversational AI agents.
- **Kaggle:** For accessing the job posting dataset.
- **Vector Search Index:** (e.g., Faiss) To efficiently retrieve relevant job postings based on user queries.

## Key Features

- **Natural language search:** Users can query the system using natural language to find relevant job postings.
- **Vector search:** Embeddings enable accurate and efficient retrieval of similar jobs based on user queries.
- **Continuous learning:** The system can be updated with new job data to improve its accuracy and relevance over time.

## Getting Started

1. Clone the project repository.
2. Set up required GCP resources and configure access.
3. Deploy the Cloud Functions and Dialogflow agent.
4. Populate the Kaggle dataset into the specified bucket.
5. Run the data ingestion and processing scripts.
6. Train the pre-trained embedding model (optional).
7. Test the system through the Dialogflow interface.

## Documentation

Detailed documentation for each component is available in the respective directories. This README file provides a high-level overview of the project.

## Contributing

We welcome contributions to improve the system. Please follow the contributing guidelines in the `CONTRIBUTING.md` file.

## License

This project is licensed under the [license name]. See the `LICENSE` file for details.

## Contact

For any questions or feedback, please contact varun.kumar@intelia.com.au.