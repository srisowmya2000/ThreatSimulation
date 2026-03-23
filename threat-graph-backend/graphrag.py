import os
import json
import logging
import anthropic
from dotenv import load_dotenv
from models import SeedInput, KnowledgeGraphExtraction, Entity, Relationship

load_dotenv()
logger = logging.getLogger(__name__)
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def extract_entities_and_relationships(seed_input: SeedInput) -> KnowledgeGraphExtraction:
    """
    Uses Anthropic's Claude to extract entities and relationships from the provided input
    using tool calling functionality to enforce JSON schema.
    """
    system_prompt = (
        "You are an expert cybersecurity analyst and knowledge graph engineer. "
        "Your task is to extract entities and relationships from the provided context to build a Threat Intelligence Knowledge Graph. "
        "You must extract ONLY the following entity types: Host, Service, Vulnerability, ThreatActor, Defense. "
        "Create logical relationships between these entities (e.g., ThreatActor EXPLOITS Vulnerability, Host RUNS Service, Defense MITIGATES Vulnerability). "
        "Ensure entity IDs are consistent so relationships connect properly."
    )

    user_content = f"""
    Context to Analyze:
    
    1. Threat Actor Name: {seed_input.threat_actor_name}
    
    2. Target Organization Tech Stack (JSON):
    {json.dumps(seed_input.tech_stack, indent=2)}
    
    3. CVE / Vulnerability Intelligence Text:
    {seed_input.cve_text}
    """

    tools = [
        {
            "name": "create_knowledge_graph",
            "description": "Output the extracted knowledge graph entities and relationships.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "entities": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string", "description": "Unique identifier for the entity (e.g., CVE-2023-1234, IP address, Service name)"},
                                "label": {"type": "string", "enum": ["Host", "Service", "Vulnerability", "ThreatActor", "Defense"]},
                                "properties": {
                                    "type": "object",
                                    "description": "Additional context properties as key-value pairs"
                                }
                            },
                            "required": ["id", "label"]
                        }
                    },
                    "relationships": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "source_id": {"type": "string", "description": "ID of the source entity"},
                                "target_id": {"type": "string", "description": "ID of the target entity"},
                                "type": {"type": "string", "description": "Type of relationship in ALL CAPS (e.g., EXPLOITS, RUNS, MITIGATES, TARGETS)"},
                                "properties": {
                                    "type": "object",
                                    "description": "Additional context properties for the relationship"
                                }
                            },
                            "required": ["source_id", "target_id", "type"]
                        }
                    }
                },
                "required": ["entities", "relationships"]
            }
        }
    ]

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=4096,
            system=system_prompt,
            tools=tools,
            tool_choice={"type": "tool", "name": "create_knowledge_graph"},
            messages=[
                {"role": "user", "content": user_content}
            ]
        )

        for content_block in response.content:
            if content_block.type == "tool_use" and content_block.name == "create_knowledge_graph":
                tool_input = content_block.input
                entities = [Entity(**e) for e in tool_input.get("entities", [])]
                relationships = [Relationship(**r) for r in tool_input.get("relationships", [])]
                return KnowledgeGraphExtraction(entities=entities, relationships=relationships)
                
        return KnowledgeGraphExtraction(entities=[], relationships=[])
        
    except Exception as e:
        logger.error(f"Failed to extract knowledge graph: {e}")
        raise e
