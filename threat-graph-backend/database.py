import os
import logging
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

class Neo4jConnection:
    def __init__(self):
        self.driver = None

    def connect(self):
        if self.driver is None:
            try:
                self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
                self.driver.verify_connectivity()
                logger.info("Connected to Neo4j successfully.")
            except Exception as e:
                logger.error(f"Failed to connect to Neo4j: {e}")
                self.driver = None

    def close(self):
        if self.driver:
            self.driver.close()

    def merge_graph(self, entities, relationships):
        self.connect()
        if not self.driver:
            logger.error("Neo4j driver not connected.")
            raise Exception("Database connection failure.")

        with self.driver.session() as session:
            for entity in entities:
                # Sanitize label securely
                label = entity.label.replace("`", "")
                query = (
                    f"MERGE (n:`{label}` {{id: $id}}) "
                    "SET n += $properties"
                )
                session.run(query, id=entity.id, properties=entity.properties)
            
            for rel in relationships:
                # Sanitize relationship type securely
                rel_type = rel.type.replace("`", "").replace(" ", "_").upper()
                query = (
                    f"MATCH (source {{id: $source_id}}) "
                    f"MATCH (target {{id: $target_id}}) "
                    f"MERGE (source)-[r:`{rel_type}`]->(target) "
                    "SET r += $properties"
                )
                session.run(query, source_id=rel.source_id, target_id=rel.target_id, properties=rel.properties)

db = Neo4jConnection()
