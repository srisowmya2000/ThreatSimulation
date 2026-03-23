import os
import json
import shutil
import subprocess

ACTORS = [
    "Cl0p", "APT28", "APT29", "Lazarus Group", "LockBit", 
    "BlackCat", "Sandworm", "Scattered Spider", "Volt Typhoon", "BlackMatter"
]

def main():
    print("Starting Multi-World Threat Actor Array Simulation")
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    
    leaderboard = []

    for actor in ACTORS:
        print(f"\n{'='*40}")
        print(f"Evaluating Threat Actor: {actor}")
        print(f"{'='*40}")

        # Clear logs
        if os.path.exists("simulation_events.log"):
            os.remove("simulation_events.log")

        # Run Simulation
        print(f"[*] Running simulation worlds for {actor}...")
        subprocess.run(["python", "simulation.py", actor], check=True)

        # Run Reporter
        print(f"[*] Compiling Breach Probability Score...")
        subprocess.run(["python", "reporter.py"], check=True)

        # Read Score
        score = 0.0
        if os.path.exists("report.json"):
            with open("report.json", "r") as f:
                report_data = json.load(f)
                score = report_data.get("breach_probability_score", 0.0)
        
        # Save results
        actor_dir = os.path.join(results_dir, actor.replace(" ", "_"))
        os.makedirs(actor_dir, exist_ok=True)
        
        if os.path.exists("report.json"):
            shutil.copy("report.json", os.path.join(actor_dir, "report.json"))
        if os.path.exists("report.pdf"):
            shutil.copy("report.pdf", os.path.join(actor_dir, "report.pdf"))

        print(f"[*] -> {actor} Breach Probability Score: {score}")
        leaderboard.append((actor, score))

    # Print Leaderboard
    leaderboard.sort(key=lambda x: x[1], reverse=True)
    
    print("\n\n")
    print("==================================================")
    print("       🔥 FINAL THREAT ACTOR LEADERBOARD 🔥       ")
    print("==================================================")
    print(f"{'Rank':<5} {'Threat Actor':<25} {'Breach Probability':<20}")
    print("-" * 50)
    for idx, (actor, score) in enumerate(leaderboard, 1):
        print(f"{idx:<5} {actor:<25} {score:.1f}%")

if __name__ == "__main__":
    main()
