import sys
import json
import logging
import requests
from bs4 import BeautifulSoup
import anthropic
import os
from dotenv import load_dotenv

from models import SeedInput
from graphrag import extract_entities_and_relationships
from database import db

# Load environment variables
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def scrape_website(url: str) -> str:
    """Scrapes the textual content of a given URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        text = soup.get_text(separator=' ', strip=True)
        return text[:4000] # Limit to 4000 chars to avoid massive LLM context costs
    except requests.exceptions.HTTPError as e:
        # Fallback for severe 403 blocks: just return a stub so simulation doesn't crash
        logger.warning(f"Failed to scrape {url}: {e}. Returning fallback stub.")
        print(f"[!] Warning: Scraper blocked by {url}. Using generic tech stack stub.")
        return f"Company URL: {url}. Architecture: Uses cloud infrastructure, modern web frameworks, and RESTful APIs."
    except Exception as e:
        logger.error(f"Failed to scrape {url}: {e}")
        raise

def build_seed_input(text_content: str, url: str) -> SeedInput:
    """Use Claude to convert raw scraped text into a structured SeedInput object."""
    system_prompt = (
        "You are an expert security reconnaissance agent. "
        "Analyze the provided website text and extract the likely technology stack. "
        "Also synthesize a realistic 'CVE intelligence' summary based on typical vulnerabilities for this stack, "
        "and name a hypothetical or known threat actor likely targeting this space."
    )
    
    tools = [
        {
            "name": "generate_seed_input",
            "description": "Output the extracted tech stack and threat intelligence.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "tech_stack": {
                        "type": "object",
                        "description": "A JSON object summarizing the frameworks, languages, infrastructure, and services inferred."
                    },
                    "cve_text": {
                        "type": "string",
                        "description": "A synthesized 2-paragraph narrative summarizing relevant vulnerabilities (CVEs) affecting this stack."
                    },
                    "threat_actor_name": {
                        "type": "string",
                        "description": "A known threat actor group name (e.g., APT29, Cl0p, Lazarus Group)."
                    }
                },
                "required": ["tech_stack", "cve_text", "threat_actor_name"]
            }
        }
    ]
    
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        system=system_prompt,
        tools=tools,
        tool_choice={"type": "tool", "name": "generate_seed_input"},
        messages=[{"role": "user", "content": f"Website Content for {url}:\n\n{text_content}"}]
    )
    
    for block in response.content:
        if block.type == "tool_use" and block.name == "generate_seed_input":
            tool_input = block.input
            return SeedInput(
                tech_stack=tool_input["tech_stack"],
                cve_text=tool_input["cve_text"],
                threat_actor_name=tool_input["threat_actor_name"]
            )
            
    raise ValueError("Failed to extract SeedInput from the LLM response.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python ingest.py <company_url>")
        sys.exit(1)
        
    url = sys.argv[1]
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
        
    print(f"[*] Starting Automated Graph Ingestion for: {url}")
    
    print("[*] Scrapping website content...")
    scraped_text = scrape_website(url)
    print(f"    -> Extracted {len(scraped_text)} characters.")
    
    print("[*] Generating Graph Seed Input via Claude...")
    seed_input = build_seed_input(scraped_text, url)
    print(f"    -> Extracted Threat Actor: {seed_input.threat_actor_name}")
    print(f"    -> Extracted Tech Stack: {json.dumps(seed_input.tech_stack, indent=2)}")
    
    from cve_fetcher import fetch_cves_for_technologies
    tech_names = []
    if isinstance(seed_input.tech_stack, dict):
        for category, items in seed_input.tech_stack.items():
            if isinstance(items, list):
                tech_names.extend(items)
            elif isinstance(items, str):
                tech_names.append(items)
                
    print("[*] Fetching real CVEs from NVD API...")
    real_cves = fetch_cves_for_technologies(tech_names)
    seed_input.cve_text = f"{seed_input.cve_text}\n\n=== RECENT REAL WORLD CVES ===\n{real_cves}"
    
    print("[*] Running GraphRAG Extraction against the seed input...")
    extraction = extract_entities_and_relationships(seed_input)
    print(f"    -> Found {len(extraction.entities)} entities and {len(extraction.relationships)} relationships.")
    
    print("[*] Merging Threat Graph into Neo4j...")
    db.merge_graph(extraction.entities, extraction.relationships)
    print("[*] Graph Ingestion Complete!")

if __name__ == "__main__":
    main()
