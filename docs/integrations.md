# Integrations Guide

OSINT Agent Network integrates with seven external threat intelligence platforms. All integrations are optional — the system degrades gracefully when API keys are absent, falling back to LLM-only analysis.

## Shodan

[Shodan](https://www.shodan.io) is the world's first search engine for internet-connected devices. OAN uses Shodan to enrich extracted IP addresses with open port information, running service banners, and geolocation data. This context is critical for distinguishing legitimate CDN infrastructure from actual C2 servers.

**Setup:** Obtain an API key from [account.shodan.io](https://account.shodan.io) and set `SHODAN_API_KEY` in your `.env` file. The free plan provides 1 query/second and 100 results per query.

## VirusTotal

[VirusTotal](https://www.virustotal.com) aggregates results from 70+ antivirus engines and URL/domain scanners. OAN queries VirusTotal for file hashes, domain reputation, and URL analysis. A VirusTotal score of 5+ malicious detections automatically elevates an IoC's confidence score.

**Setup:** Register at [virustotal.com](https://www.virustotal.com) and set `VIRUSTOTAL_API_KEY`. The free tier allows 4 requests/minute.

## AbuseIPDB

[AbuseIPDB](https://www.abuseipdb.com) is a community-driven database of reported malicious IP addresses. OAN uses it to quickly filter out known-bad IPs and assign a community abuse confidence score (0–100%). IPs with a score above 80% are flagged as high-priority.

**Setup:** Register at [abuseipdb.com](https://www.abuseipdb.com/account/api) and set `ABUSEIPDB_API_KEY`.

## AlienVault OTX

[AlienVault OTX](https://otx.alienvault.com) is the world's largest open threat intelligence community with over 100,000 participants. OAN uses OTX to search for existing threat pulses related to the analysis target, providing historical context and community-validated IoCs.

**Setup:** Register at [otx.alienvault.com](https://otx.alienvault.com) and set `OTX_API_KEY`.

## Censys

[Censys](https://search.censys.io) continuously scans the entire IPv4 address space and provides detailed data on hosts, certificates, and open services. OAN uses Censys as a secondary enrichment source for IP addresses, particularly useful for identifying C2 infrastructure patterns.

**Setup:** Register at [search.censys.io](https://search.censys.io/account/api) and set `CENSYS_API_ID` and `CENSYS_API_SECRET`. The free tier provides 250 queries/month.

## GreyNoise

[GreyNoise](https://www.greynoise.io) collects and analyzes data on IPs that scan the internet. It is invaluable for filtering out background noise — mass scanners, crawlers, and research bots — from real targeted threats. OAN uses GreyNoise to suppress false positives before the validation phase.

**Setup:** Register at [greynoise.io](https://www.greynoise.io/account) and set `GREYNOISE_API_KEY`. The community API is free and covers basic noise classification.

## MISP

[MISP](https://www.misp-project.org) (Malware Information Sharing Platform) is an open-source threat intelligence platform for sharing, storing, and correlating IoCs. OAN automatically creates MISP events and attributes from verified intelligence, enabling seamless sharing with your team or the broader MISP community.

**Setup:** Deploy your own MISP instance (see [misp-project.org](https://www.misp-project.org/download/)) and set `MISP_URL` and `MISP_AUTH_KEY`.

## SpiderFoot

[SpiderFoot](https://github.com/smicallef/spiderfoot) is an open-source OSINT automation tool that can scan targets across 200+ data sources. OAN can optionally trigger SpiderFoot scans and import the results as additional raw intelligence. SpiderFoot must be running locally.

**Setup:** Install SpiderFoot (`pip install spiderfoot`) and start it with `python sf.py -l 127.0.0.1:5001`. Set `SPIDERFOOT_URL=http://localhost:5001`.
