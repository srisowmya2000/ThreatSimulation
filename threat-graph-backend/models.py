from pydantic import BaseModel, Field
from typing import List, Dict, Any

class SeedInput(BaseModel):
    cve_text: str = Field(..., description="Text containing CVE information")
    tech_stack: Dict[str, Any] = Field(..., description="Organization tech stack JSON")
    threat_actor_name: str = Field(..., description="Name of the threat actor")

class Entity(BaseModel):
    id: str = Field(..., description="Unique identifier for the entity")
    label: str = Field(..., description="Entity type: Host, Service, Vulnerability, ThreatActor, Defense")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Additional properties of the entity")

class Relationship(BaseModel):
    source_id: str = Field(..., description="ID of the source entity")
    target_id: str = Field(..., description="ID of the target entity")
    type: str = Field(..., description="Type of relationship (e.g., EXPLOITS, RUNS, MITIGATES)")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Additional properties of the relationship")

class KnowledgeGraphExtraction(BaseModel):
    entities: List[Entity]
    relationships: List[Relationship]

# Report Output Models

class TimelineEvent(BaseModel):
    timestamp: str = Field(..., description="Timestamp of the event")
    step: int = Field(..., description="Simulation step number")
    agent: str = Field(..., description="Agent role")
    action_summary: str = Field(..., description="Short summary of the action taken")
    mitre_ids: List[str] = Field(default_factory=list, description="Associated MITRE ATT&CK technique IDs")

class AttackHeatmapEntry(BaseModel):
    mitre_id: str = Field(..., description="MITRE ATT&CK Technique ID (e.g., T1190)")
    technique_name: str = Field(..., description="Human readable name of the technique")
    usage_count: int = Field(..., description="Number of times this technique was attempted in simulation")
    success_count: int = Field(..., description="Number of times this technique succeeded")

class DetectionGap(BaseModel):
    missing_mitigation: str = Field(..., description="The defense/process missing that caused a miss")
    vulnerability_exploited: str = Field(..., description="The ID/CVE of the vulnerability exploited")
    description: str = Field(..., description="Why the detection missed this attack")

class HardeningRecommendation(BaseModel):
    priority: str = Field(..., description="HIGH, MEDIUM, LOW")
    actionable_remediation: str = Field(..., description="Specific action to fix the gap")
    estimated_mttd_improvement: str = Field(..., description="Expected improvement to detection metrics")

class SimulationReport(BaseModel):
    breach_probability_score: float = Field(..., description="Overall probability of breach success based on aggregating parallel simulation worlds (0.0 to 100.0)")
    kill_chain_timeline: List[TimelineEvent] = Field(..., description="List of chronologial events in the simulation")
    attack_heatmap: List[AttackHeatmapEntry] = Field(..., description="Heatmap data of MITRE techniques")
    detection_gaps: List[DetectionGap] = Field(..., description="Identified gaps in the defender's capability")
    recommendations: List[HardeningRecommendation] = Field(..., description="Prioritized recommendations to harden the environment")
