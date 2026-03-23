import logging
from datetime import datetime
import json
import re

class SimulationLogger:
    def __init__(self, log_file="simulation_events.log"):
        self.log_file = log_file
        
        # Configure standard python logger to write to the file
        self.logger = logging.getLogger("SimulationEngine")
        self.logger.setLevel(logging.INFO)
        
        # Avoid adding multiple handlers if instantiated multiple times
        if not self.logger.handlers:
            fh = logging.FileHandler(self.log_file)
            fh.setLevel(logging.INFO)
            formatter = logging.Formatter('%(message)s')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    def extract_mitre_id(self, text: str) -> list[str]:
        """Extracts MITRE ATT&CK technique IDs (e.g., T1059, T1190) from text."""
        pattern = r"\bT\d{4}(?:\.\d{3})?\b"
        return list(set(re.findall(pattern, text)))

    def log_event(self, step: int, agent_role: str, action: str, details: str, world_id: str = "World-1"):
        """Standardized JSON logging for the simulation events."""
        timestamp = datetime.utcnow().isoformat() + "Z"
        mitre_ids = self.extract_mitre_id(details)
        
        log_entry = {
            "timestamp": timestamp,
            "world_id": world_id,
            "step": step,
            "agent": agent_role,
            "action": action,
            "mitre_attack_ids": mitre_ids,
            "details": details
        }
        
        # Log purely as JSON for easy parsing by external tools later
        self.logger.info(json.dumps(log_entry))
        
        # Also print to terminal for visibility
        print(f"\n[{timestamp}] [{world_id}] Step {step} | {agent_role} -> {action}")
        if mitre_ids:
            print(f"  > Detected ATT&CK IDs: {', '.join(mitre_ids)}")
        print(f"  > {details}\n")

sim_logger = SimulationLogger()
