import pytest
from utils.ioc_extractor import extract_iocs, defang_ioc, refang_ioc

def test_extract_ipv4():
    text = "The C2 server was found at 192.168.1.100 and 10.0.0.1."
    result = extract_iocs(text)
    assert "ipv4" in result
    assert "192.168.1.100" in result["ipv4"]

def test_extract_sha256():
    text = "Malware hash: a3f5b2c1d4e6f7890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f6789"
    result = extract_iocs(text)
    assert "sha256" in result

def test_extract_cve():
    text = "This exploit targets CVE-2021-44228 (Log4Shell)."
    result = extract_iocs(text)
    assert "cve" in result
    assert "CVE-2021-44228" in result["cve"]

def test_extract_email():
    text = "Contact the attacker at evil@malicious-domain.ru for ransom."
    result = extract_iocs(text)
    assert "email" in result

def test_defang_ioc():
    assert defang_ioc("192.168.1.1") == "192[.]168[.]1[.]1"
    assert defang_ioc("http://evil.com") == "hxxp://evil[.]com"

def test_refang_ioc():
    assert refang_ioc("192[.]168[.]1[.]1") == "192.168.1.1"
    assert refang_ioc("hxxp://evil[.]com") == "http://evil.com"

def test_whitelist_filters_google():
    text = "This is not malicious: google.com and microsoft.com"
    result = extract_iocs(text)
    if "domain" in result:
        assert "google.com" not in result["domain"]
        assert "microsoft.com" not in result["domain"]
