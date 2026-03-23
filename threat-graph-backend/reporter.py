import os
import json
import re
from crewai import Task, Crew, Process
from agent_factory import create_report_agent
from models import SimulationReport
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

def read_simulation_logs(log_file="simulation_events.log") -> str:
    """Reads the chronological JSON strings from the simulation output."""
    if not os.path.exists(log_file):
        return "No simulation logs found."
    
    logs = []
    with open(log_file, "r") as f:
        for line in f:
            logs.append(line.strip())
    # Format them as a pretty array for the agent to parse
    return "[\n" + ",\n".join(logs) + "\n]"

def calculate_breach_probability(log_file="simulation_events.log") -> float:
    """Calculates deterministic breach probability tracking success/failure of attacks per world."""
    if not os.path.exists(log_file):
        return 0.0
        
    world_compromises = {}
    
    with open(log_file, "r") as f:
        for line in f:
            try:
                event = json.loads(line.strip())
                world_id = event.get("world_id")
                action = event.get("action")
                
                if world_id and action == "Topology State Calculation":
                    details_str = str(event.get("details", "")).lower()
                    
                    # Core indicators of a successful exploit phase in the topology
                    is_compromised = any(indicator in details_str for indicator in [
                        '"success": true',
                        '"outcome": "success"',
                        '"result": "pass"',
                        '"pathcorrelation": "succeeds"',
                        '"pathcorrelation": "partially_successful"'
                    ])
                    
                    if world_id not in world_compromises:
                        world_compromises[world_id] = False
                    
                    if is_compromised:
                        world_compromises[world_id] = True
            except json.JSONDecodeError:
                continue
                
    total_worlds = len(world_compromises)
    if total_worlds == 0:
        return 0.0
        
    compromised_count = sum(1 for v in world_compromises.values() if v)
    score = float((compromised_count / total_worlds) * 100.0)
    return round(score, 1)

def generate_pdf_report(report: dict, output_file="report.pdf"):
    """Takes the Pydantic-dict mapping of the Report and converts to a formatted PDF metric report."""
    print(f"Writing PDF report to {output_file}...")
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter
    
    y = height - 50
    left_margin = 50
    line_height = 14
    max_text_width = width - 2 * left_margin
    
    def write_text(text, fontsize=10, bold=False):
        nonlocal y
        c.setFont("Helvetica-Bold" if bold else "Helvetica", fontsize)
        # Handle simple wrapping using reportlab utility
        lines = simpleSplit(str(text), "Helvetica-Bold" if bold else "Helvetica", fontsize, max_text_width)
        for line in lines:
            if y < 50:
                c.showPage() # Create new page if at bottom
                y = height - 50
                c.setFont("Helvetica-Bold" if bold else "Helvetica", fontsize)
            c.drawString(left_margin, y, line)
            y -= line_height
            
    # Title
    write_text("Threat Agent Simulation - Security Report", 16, True)
    y -= 10
    
    write_text(f"Swarm Intelligence Breach Probability Score: {report.get('breach_probability_score', 0)}%", 14, True)
    y -= 15
    
    # 1. Kill Chain Timeline
    write_text("1. Aggregated Kill Chain Timeline", 14, True)
    for event in report.get("kill_chain_timeline", []):
        text = f"Step {event.get('step')}: [{event.get('agent')}] {event.get('action_summary')} (Techniques: {', '.join(event.get('mitre_ids', []))})"
        write_text(text, 10, False)
    y -= 10
    
    # 2. ATT&CK Heatmap
    write_text("2. MITRE ATT&CK Heatmap", 14, True)
    for t in report.get("attack_heatmap", []):
        text = f"- {t.get('mitre_id')} ({t.get('technique_name')}): Attempted {t.get('usage_count')} time(s), Succeeded {t.get('success_count')} time(s)"
        write_text(text, 10, False)
    y -= 10
    
    # 3. Detection Gaps
    write_text("3. Identified Detection Gaps", 14, True)
    for gap in report.get("detection_gaps", []):
        write_text(f"Missing Mitigation: {gap.get('missing_mitigation')} | Vuln/CVE: {gap.get('vulnerability_exploited')}", 10, True)
        write_text(gap.get('description'), 10, False)
        y -= 5
    y -= 10
    
    # 4. Hardening Recommendations
    write_text("4. Hardening Recommendations", 14, True)
    for rec in report.get("recommendations", []):
        write_text(f"[{rec.get('priority')}] {rec.get('actionable_remediation')}", 10, True)
        write_text(f"Expected MTTD Imrpovement: {rec.get('estimated_mttd_improvement')}", 10, False)
        y -= 5
        
    c.save()
    print("PDF Generation complete.")

def main():
    print("Initializing ReportAgent...")
    report_agent = create_report_agent(session_id="sim_report_1")
    
    logs = read_simulation_logs()
    
    # CrewAI Task to parse the logs and enforce structured Pydantic output
    report_task = Task(
        description=(
            "Evaluate the chronological raw JSON logs from the swarm of parallel simulation worlds below:\n\n"
            f"{logs}\n\n"
            "Produce a structured Intelligence Report that aggregates the events. "
            "You MUST calculate a 'breach_probability_score' (0.0 to 100.0) based on the success rate of attacks across the different worlds. "
            "Extract the kill chain timeline, calculate a heatmap of MITRE ATT&CK techniques used and their success rate, "
            "list exact vulnerabilities exploited that the defender failed to detect (Detection Gaps), "
            "and lastly create priority based hardening recommendations.\n"
            "CRITICAL: You must populate the actual fields with your mathematical analysis. DO NOT return the JSON Schema definition."
        ),
        expected_output=(
            "Output VALID JSON matching this exact structure, with no schema definitions, and NO conversational text. Example:\n"
            "{\n"
            '  "breach_probability_score": 85.5,\n'
            '  "kill_chain_timeline": [\n'
            '    {"timestamp": "2023-01-01T00:00:00Z", "step": 1, "agent": "Attacker", "action_summary": "Scanned", "mitre_ids": ["T1595"]}\n'
            '  ],\n'
            '  "attack_heatmap": [\n'
            '    {"mitre_id": "T1595", "technique_name": "Active Scanning", "usage_count": 5, "success_count": 5}\n'
            '  ],\n'
            '  "detection_gaps": [\n'
            '    {"missing_mitigation": "IDS", "vulnerability_exploited": "CVE-2023-1234", "description": "No TLS inspection"}\n'
            '  ],\n'
            '  "recommendations": [\n'
            '    {"priority": "HIGH", "actionable_remediation": "Enable TLS inspection", "estimated_mttd_improvement": "50%"}\n'
            '  ]\n'
            "}"
        ),
        agent=report_agent
    )
    
    crew = Crew(
        agents=[report_agent],
        tasks=[report_task],
        process=Process.sequential,
        verbose=True
    )
    
    print("\nRunning ingestion of simulation logs into ReportAgent...")
    crew.kickoff()
    
    # Manually parse the raw JSON to avoid Haiku schema-reflection bugs
    if report_task.output and report_task.output.raw:
        raw_output = report_task.output.raw
        
        # Extract JSON content between braces
        match = re.search(r'\{.*\}', raw_output, re.DOTALL)
        if match:
            json_str = match.group(0)
            try:
                report_data = json.loads(json_str)
                
                # Mathematically calculate breach probability based on exact simulation outputs
                exact_score = calculate_breach_probability("simulation_events.log")
                report_data["breach_probability_score"] = exact_score
                
                # Write structured JSON to disk
                with open("report.json", "w") as f:
                    json.dump(report_data, f, indent=2)
                print("Generated pure structured JSON: report.json")
                
                # Write PDF to disk
                generate_pdf_report(report_data, "report.pdf")
            except json.JSONDecodeError as e:
                print(f"Error: Failed to parse JSON: {e}\nRaw Output: {raw_output}")
        else:
            print(f"Error: Could not find JSON block.\nRaw: {raw_output}")
            
    else:
        print("Error: The agent failed to output a response.")

if __name__ == "__main__":
    main()
