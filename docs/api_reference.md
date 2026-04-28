# API Reference

The OSINT Agent Network exposes a REST API built with FastAPI. Interactive documentation is available at `/docs` (Swagger UI) and `/redoc` (ReDoc) when the server is running.

## Base URL

```
http://localhost:8000
```

## Endpoints

### Health Check

```
GET /health
```

Returns the API server status and current version.

**Response:**
```json
{
  "status": "ok",
  "version": "0.3.0"
}
```

---

### Start a Scan

```
POST /api/v1/scans/
```

Submits a new OSINT analysis task to the background worker queue.

**Request Body:**
```json
{
  "target": "APT29 SolarWinds",
  "sources": ["twitter", "reddit"],
  "priority": "high"
}
```

**Response:**
```json
{
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "target": "APT29 SolarWinds",
  "status": "queued",
  "message": "Scan task submitted to worker queue"
}
```

---

### Get Scan Status

```
GET /api/v1/scans/{task_id}
```

Polls the status of a previously submitted scan task.

**Response (completed):**
```json
{
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "completed",
  "result": {
    "status": "success",
    "target": "APT29 SolarWinds",
    "threats_found": 4,
    "report_path": "reports/stix_report_APT29_SolarWinds_1714291200.json"
  }
}
```

---

### Extract IoCs from Text

```
POST /api/v1/iocs/extract
```

Runs regex-based IoC extraction on raw text input.

**Request Body:**
```json
{
  "text": "C2 server at 198.51.100.43. Malware hash: a3f5b2c1d4e6f789..."
}
```

**Response:**
```json
{
  "raw_iocs": {
    "ipv4": ["198.51.100.43"],
    "sha256": ["a3f5b2c1d4e6f789..."]
  },
  "defanged_iocs": {
    "ipv4": ["198[.]51[.]100[.]43"],
    "sha256": ["a3f5b2c1d4e6f789..."]
  },
  "total_count": 2
}
```

---

### Enrich an IP Address

```
POST /api/v1/iocs/enrich/ip
```

Queries AbuseIPDB, GreyNoise, and VirusTotal concurrently for a given IP address.

**Request Body:**
```json
{
  "ip": "198.51.100.43"
}
```

**Response:**
```json
{
  "ip": "198.51.100.43",
  "virustotal": { "...": "..." },
  "abuseipdb": {
    "abuseConfidenceScore": 87,
    "totalReports": 142,
    "countryCode": "RU"
  },
  "greynoise": {
    "noise": false,
    "classification": "malicious"
  }
}
```
