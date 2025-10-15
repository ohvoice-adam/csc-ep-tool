# CSC EP Tool

A Flask application deployed on Google Cloud Run.

## Prerequisites

- Python 3.11+
- Google Cloud SDK (`gcloud` CLI)
- Docker (for local testing)

## Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The app will be available at `http://localhost:8080`

## Local Testing with Docker

Build and run the Docker container locally:

```bash
docker build -t csc-ep-tool .
docker run -p 8080:8080 -e PORT=8080 csc-ep-tool
```

## Deployment to Google Cloud Run

1. Set your Google Cloud project:
```bash
gcloud config set project YOUR_PROJECT_ID
```

2. Build and deploy:
```bash
gcloud run deploy csc-ep-tool \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

Or build with Cloud Build and deploy:
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/csc-ep-tool
gcloud run deploy csc-ep-tool \
  --image gcr.io/YOUR_PROJECT_ID/csc-ep-tool \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Endpoints

- `GET /` - Hello world endpoint
- `GET /health` - Health check endpoint
