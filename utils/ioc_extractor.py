import re
from typing import Dict, List

# Compiled regex patterns for common IoC types
PATTERNS = {
    "ipv4": re.compile(
        r'\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b'
    ),
    "ipv6": re.compile(
        r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b'
    ),
    "domain": re.compile(
        r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b'
    ),
    "url": re.compile(
        r'https?://[^\s<>"{}|\\^`\[\]]+'
    ),
    "md5": re.compile(
        r'\b[a-fA-F0-9]{32}\b'
    ),
    "sha1": re.compile(
        r'\b[a-fA-F0-9]{40}\b'
    ),
    "sha256": re.compile(
        r'\b[a-fA-F0-9]{64}\b'
    ),
    "email": re.compile(
        r'\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Z|a-z]{2,}\b'
    ),
    "cve": re.compile(
        r'\bCVE-\d{4}-\d{4,7}\b',
        re.IGNORECASE
    ),
    "bitcoin_address": re.compile(
        r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b'
    ),
}

# Known false-positive domains to filter out
WHITELIST_DOMAINS = {
    "google.com", "microsoft.com", "github.com", "example.com",
    "localhost", "cloudflare.com", "amazon.com", "youtube.com"
}

def extract_iocs(text: str) -> Dict[str, List[str]]:
    """
    Extracts all Indicators of Compromise (IoCs) from a given text string.
    Returns a dictionary keyed by IoC type.
    """
    results: Dict[str, List[str]] = {}
    
    for ioc_type, pattern in PATTERNS.items():
        matches = list(set(pattern.findall(text)))
        
        # Apply whitelist filtering for domains
        if ioc_type == "domain":
            matches = [m for m in matches if m not in WHITELIST_DOMAINS]
            
        if matches:
            results[ioc_type] = matches
            
    return results

def defang_ioc(ioc: str) -> str:
    """
    Defangs an IoC for safe display in reports (e.g., 1.2.3.4 -> 1[.]2[.]3[.]4).
    """
    defanged = ioc.replace(".", "[.]").replace("http", "hxxp")
    return defanged

def refang_ioc(ioc: str) -> str:
    """
    Refangs a defanged IoC back to its original form.
    """
    refanged = ioc.replace("[.]", ".").replace("hxxp", "http")
    return refanged
