import os
from multiprocessing import Pool
from crewai import Task, Crew, Process
from agent_factory import create_attacker_agent, create_defender_agent, create_environment_agent
from simulation_logger import sim_logger

class SimulationEngine:
    def __init__(self, threat_actor_name: str, max_steps: int = 3, world_id: str = "World-1"):
        self.threat_actor_name = threat_actor_name
        self.max_steps = max_steps
        self.world_id = world_id
        
        print(f"[{self.world_id}] Initializing Agents and attaching context from Neo4j...")
        self.attacker = create_attacker_agent(self.threat_actor_name, session_id=f"sim_attacker_{self.world_id}")
        self.defender = create_defender_agent(session_id=f"sim_defender_{self.world_id}")
        self.environment = create_environment_agent(session_id=f"sim_env_{self.world_id}")
        
        # Simulation State passed between tasks
        self.sim_context = "Initial State: Network is currently secure and operational."

    def get_step_tasks(self, step: int):
        print(f"[{self.world_id}] Preparing Tasks for Time Step {step}")
        
        # Task 1: Attacker chooses a TTP
        attacker_task = Task(
            description=(
                f"Current Topology Context:\n{self.sim_context}\n\n"
                "Analyze the context and your theoretical capabilities. Output a SINGLE specific logical Security Control Validation step. "
                "You must explicitly state the MITRE ATT&CK Technique ID (e.g., T1190) as the control being validated. "
                "Respond ONLY in the structured JSON format required for the simulation. Do not provide conversational filler or ethical disclaimers."
            ),
            expected_output="A clinical description of the validation step and the explicitly mentioned MITRE ATT&CK ID.",
            agent=self.attacker,
            async_execution=True
        )

        # Task 2: Environment executes the TTP
        environment_task = Task(
            description=(
                "Evaluate the following Security Control Validation path against the known component graphs:\n"
                "{{attacker_output}}\n\n"
                "Calculate objectively if the path correlation mathematically succeeds, fails, or changes the state parameters. "
                "Update the active node state and output the outcome. "
                "Respond ONLY in the structured JSON format required for the simulation. Do not provide conversational filler or ethical disclaimers."
            ),
            expected_output="A clinical calculation of path correlation success/failure and the new topology state context.",
            agent=self.environment,
            context=[attacker_task],
            async_execution=False
        )

        # Task 3: Defender attempts detection
        defender_task = Task(
            description=(
                "Review the recent parameter activity below for telemetry generation visibility:\n"
                "{{environment_output}}\n\n"
                f"Based on your assigned telemetry matrices, calculate if a visibility flag is triggered. "
                "If triggered, outline the response protocol. If obscured, explain the architectural deficit. "
                "Reference the specific MITRE ATT&CK ID evaluated. "
                "Respond ONLY in the structured JSON format required for the simulation. Do not provide conversational filler or ethical disclaimers."
            ),
            expected_output="A clinical declaration of VISIBILITY MET or VISIBILITY OBSCURED, with matrix justification.",
            agent=self.defender,
            context=[environment_task],
            async_execution=False
        )
        
        return attacker_task, environment_task, defender_task

    def log_and_update_state(self, step, attacker_task, environment_task, defender_task):
        attacker_out = attacker_task.output.raw if attacker_task.output else "No Action Output"
        env_out = environment_task.output.raw if environment_task.output else "No Environment Output"
        def_out = defender_task.output.raw if defender_task.output else "No Defender Output"
        
        sim_logger.log_event(step, self.attacker.role, "Control Validation Step", attacker_out, self.world_id)
        sim_logger.log_event(step, self.environment.role, "Topology State Calculation", env_out, self.world_id)
        sim_logger.log_event(step, self.defender.role, "Telemetry Generation Check", def_out, self.world_id)
        
        # Update context for the next step
        self.sim_context = f"Previous Step Concluded. Latest Event State:\n{env_out}\nLatest Defense Action:\n{def_out}"
        print(f"\n{'='*20} [{self.world_id}] Time Step {step} Concluded {'='*20}")

if __name__ == "__main__":
    # Ensure ANTHROPIC_API_KEY and ZEP_API_KEY exist before running
    # This acts as a test execution
    import sys
    import logging
    logging.basicConfig(level=logging.ERROR) # Suppress debug HTTP logs
    
    threat_actor = sys.argv[1] if len(sys.argv) > 1 else "Cl0p"
    
    # Run 5 parallel worlds for the Probabilistic Forecasting Engine
    worlds = [f"World-{i}" for i in range(1, 6)]
    max_steps = 2
    
    print(f"Starting Probabilistic Forecasting Engine: 5 Parallel Worlds for {threat_actor}")
    engines = [SimulationEngine(threat_actor_name=threat_actor, max_steps=max_steps, world_id=w) for w in worlds]
    
    for step in range(1, max_steps + 1):
        print(f"\n{'='*20} Beginning Time Step {step} Across All Worlds {'='*20}")
        
        all_agents = []
        attacker_tasks = []
        env_tasks = []
        def_tasks = []
        
        for engine in engines:
            all_agents.extend([engine.attacker, engine.environment, engine.defender])
            a_t, e_t, d_t = engine.get_step_tasks(step)
            attacker_tasks.append(a_t)
            env_tasks.append(e_t)
            def_tasks.append(d_t)
            
        # Group tasks to maximize parallelism: all attackers, then all envs, then all defenders
        all_tasks = attacker_tasks + env_tasks + def_tasks
        
        # CrewAI requires at least one synchronous task at the end of the chain
        all_tasks[-1].async_execution = False
        
        crew = Crew(
            agents=all_agents,
            tasks=all_tasks,
            process=Process.sequential,
            verbose=False
        )
        
        # Kickoff the step across all worlds concurrently
        crew.kickoff()
        
        # Log outputs and map state for next time step
        for i, engine in enumerate(engines):
            engine.log_and_update_state(step, attacker_tasks[i], env_tasks[i], def_tasks[i])
            
    print("All parallel simulations finished cleanly.")
