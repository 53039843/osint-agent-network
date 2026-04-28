# System Architecture

## Overview

The OSINT Agent Network (OAN) is built on a **six-phase pipeline architecture** that combines the reasoning capabilities of Large Language Models with traditional, battle-tested security intelligence tools. The system is designed to be modular, allowing each component to be upgraded or replaced independently.

## Pipeline Phases

The pipeline is orchestrated by the `OSINTPipeline` class in `core/pipeline.py`, which coordinates the following six sequential phases:

**Phase 1 — Data Collection** is handled by the `CollectorAgent`, which concurrently scrapes data from multiple configured sources including Twitter/X, Reddit, Hacker News, Pastebin, and simulated dark web forums. The agent uses `asyncio.gather()` to parallelize requests, significantly reducing collection time.

**Phase 2 — Multi-modal LLM Analysis** is performed by the `AnalyzerAgent`, which sends collected items to the Xiaomi MiMo V2.5 API. For items containing image URLs (e.g., malware screenshots, architecture diagrams), the agent constructs a multi-modal payload. For text-only items, it performs deep chain-of-thought reasoning to extract Indicators of Compromise (IoCs) and MITRE ATT&CK TTPs.

**Phase 3 — External Enrichment** cross-references LLM-extracted IoCs against established threat intelligence platforms. IP addresses and domains are queried against **Shodan** for open port and banner information, and against **VirusTotal** for file hash and URL reputation scores.

**Phase 4 — Red/Blue Team Validation** is the most computationally intensive phase. Two separate LLM instances are instantiated — a "Red Team" agent tasked with debunking the IoC, and a "Blue Team" agent tasked with defending it. The final verdict is determined by a confidence-weighted random selection, simulating the adversarial debate process used in real security operations centers.

**Phase 5 — STIX 2.1 Report Generation** aggregates all verified intelligence into a structured STIX 2.1 Bundle, which is saved as a JSON file in the `reports/` directory. This format is compatible with industry-standard threat intelligence platforms such as MISP and OpenCTI.

**Phase 6 — MISP Integration** optionally pushes the generated STIX bundle to a configured MISP instance, enabling automated sharing with the broader threat intelligence community.

## Integration Architecture

| Tool | Purpose | Integration Type |
|---|---|---|
| Xiaomi MiMo V2.5 | Multi-modal reasoning, IoC extraction | REST API (OpenAI-compatible) |
| Shodan | Host/network intelligence enrichment | REST API |
| VirusTotal | File hash and domain reputation | REST API v3 |
| MISP | Threat intelligence sharing | REST API |
| Redis + Celery | Async task queue for background jobs | Message Broker |
| FastAPI | REST interface for external consumers | HTTP Server |

## Technology Stack

The project is built entirely on Python 3.10+ and leverages the `asyncio` ecosystem for high-concurrency I/O operations. `Pydantic v2` is used for strict data validation throughout the pipeline. The `aiohttp` library handles all outbound HTTP requests to external APIs in a non-blocking manner.
