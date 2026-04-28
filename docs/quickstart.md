# Quickstart Guide

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.10 or higher
- Docker and Docker Compose (optional, for containerized deployment)
- A Xiaomi MiMo API key (obtain from [platform.xiaomimimo.com](https://platform.xiaomimimo.com))

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/osint-agent-network.git
cd osint-agent-network
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Copy the example environment file and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env` with your credentials. At minimum, you need to set `MIMO_API_KEY`. All other integrations (Shodan, VirusTotal, MISP) are optional but recommended for full functionality.

## Running the CLI

To run a one-off analysis from the command line:

```bash
python main.py --target "APT29 SolarWinds"
```

The pipeline will execute all six phases and save the STIX 2.1 report to the `reports/` directory.

## Running the API Server

To start the FastAPI server for programmatic access:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

You can then trigger an analysis via HTTP:

```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
     -H "Content-Type: application/json" \
     -d '{"target": "Lazarus Group"}'
```

Check the status of a running analysis:

```bash
curl "http://localhost:8000/api/v1/status/Lazarus%20Group"
```

## Docker Deployment

For production deployment using Docker Compose:

```bash
docker-compose up -d
```

This will start the API server, a Celery background worker, and a Redis broker.
