import requests
import json
import time

API_URL = "http://localhost:8000/api/extract"

payload = {
    "cve_text": "CVE-2023-34362 is a critical vulnerability in MOVEit Transfer that allows unauthenticated threat actors to gain unauthorized access to the database. The Cl0p ransomware gang has been observed exploiting this vulnerability to steal data. A patch is available in version 2023.0.1.",
    "tech_stack": {
        "os": "Windows Server 2019",
        "software": ["MOVEit Transfer 2022.1", "Microsoft SQL Server"]
    },
    "threat_actor_name": "Cl0p"
}
def test():
    # Wait for API to be up
    for _ in range(30):
        try:
            resp = requests.get("http://localhost:8000/api/health")
            if resp.status_code == 200:
                print("API is up!")
                # Give Neo4j a bit time to initialize just in case
                time.sleep(2)
                break
        except requests.ConnectionError:
            pass
        time.sleep(1)
    
    print("Sending request to /api/extract...")
    response = requests.post(API_URL, json=payload)
    print("Status Code:", response.status_code)
    try:
        print("Response JSON:\n", json.dumps(response.json(), indent=2))
    except Exception as e:
        print("Response Text:", response.text)
if __name__ == "__main__":
    test()
