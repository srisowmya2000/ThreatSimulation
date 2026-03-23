import requests
import logging
from typing import List

logger = logging.getLogger(__name__)

def fetch_cves_for_technologies(tech_names: List[str]) -> str:
    """
    Given a list of technology names, fetch the top 5 CVEs for each from the NVD API
    and return them as a formatted text block.
    """
    all_cves_text = []

    for tech in tech_names:
        if not tech or not isinstance(tech, str):
            continue
            
        try:
            # NIST NVD API v2 allows querying by keyword
            # Using resultsPerPage=5 to get the top 5 most relevant results
            url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={tech}&resultsPerPage=5"
            
            # Using a custom User-Agent and timeout to be polite to the API
            headers = {"User-Agent": "ThreatGraph-Ingestion-Bot/1.0"}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                vulnerabilities = data.get("vulnerabilities", [])
                
                if vulnerabilities:
                    all_cves_text.append(f"\n--- CVEs for {tech} ---")
                    for vuln in vulnerabilities:
                        cve_item = vuln.get("cve", {})
                        cve_id = cve_item.get("id", "Unknown CVE ID")
                        
                        # Extract the english description
                        descriptions = cve_item.get("descriptions", [])
                        en_desc = next((d.get("value") for d in descriptions if d.get("lang") == "en"), "No description available")
                        
                        all_cves_text.append(f"{cve_id}: {en_desc}")
            else:
                logger.warning(f"NVD API returned {response.status_code} for {tech}")
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"NVD API unreachable or failed for {tech}: {str(e)}")
            
    if not all_cves_text:
        return "No real CVEs found or NVD API unreachable."
        
    return "\n".join(all_cves_text)

if __name__ == "__main__":
    # Test script directly
    sample = ["nginx", "react"]
    print(fetch_cves_for_technologies(sample))
