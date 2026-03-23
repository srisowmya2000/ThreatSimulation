import os
import logging
from agent_factory import create_attacker_agent, create_defender_agent, create_environment_agent

logging.basicConfig(level=logging.INFO)

def test_factory():
    print("Testing Attacker Agent Creation...")
    attacker = create_attacker_agent("Cl0p", session_id="test_session")
    print(f"Role: {attacker.role}\nGoal: {attacker.goal}\n")

    print("Testing Defender Agent Creation...")
    defender = create_defender_agent(session_id="test_session")
    print(f"Role: {defender.role}\nGoal: {defender.goal}\n")
    
    print("Testing Environment Agent Creation...")
    env_agent = create_environment_agent(session_id="test_session")
    print(f"Role: {env_agent.role}\nGoal: {env_agent.goal}\n")

if __name__ == "__main__":
    test_factory()
