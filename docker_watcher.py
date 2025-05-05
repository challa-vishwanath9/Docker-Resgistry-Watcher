import requests
import json
import subprocess
import os

# Configuration
DOCKER_USERNAME = "challavishwanath"  # For official images like nginx
IMAGE_NAME = "docker-watcher"
DEPLOYMENT_NAME = "nginx-deployment"
CONTAINER_NAME = "watcher"
NAMESPACE = "default"
TAG_FILE = "/data/last_tag.json"  # Mounted path for persistence

# Get latest tag from Docker Hub
def get_latest_tag():
    url = f"https://registry.hub.docker.com/v2/repositories/{DOCKER_USERNAME}/{IMAGE_NAME}/tags"
    response = requests.get(url)
    data = response.json()
    tags = sorted(
        data["results"],
        key=lambda result: result["last_updated"]
    )
    tags = [result["name"] for result in tags]
    return tags[-1] if tags else None

# Save the latest tag to a file
def save_tag(tag):
    os.makedirs(os.path.dirname(TAG_FILE), exist_ok=True)
    # print(f"[DEBUG] Saving tag to {TAG_FILE}")
    with open(TAG_FILE, "w") as f:
        print(f"[DEBUG] Saving tag to {TAG_FILE}")
        json.dump({"last_tag": tag}, f)

# Load the last seen tag
def load_tag():
    if not os.path.exists(TAG_FILE):
        return None
    with open(TAG_FILE, "r") as f:
        print(f"[DEBUG] Trying to read tag from {TAG_FILE}")
        return json.load(f).get("last_tag")

# Update Kubernetes deployment
def update_kubernetes(tag):
    new_image = f"{DOCKER_USERNAME}/{IMAGE_NAME}:{tag}"
    cmd = [
        "kubectl", "set", "image",
        f"deployment/{DEPLOYMENT_NAME}",
        f"{CONTAINER_NAME}={new_image}",
        "-n", NAMESPACE
    ]
    subprocess.run(cmd)
    print(f"[+] Updated deployment to {new_image}")

# Main logic
def main():
    latest_tag = get_latest_tag()
    print(f"[i] Latest tag on Docker Hub: {latest_tag}")
    
    last_tag = load_tag()
    print(f"[i] Last deployed tag: {last_tag}")

    if latest_tag != last_tag:
        print("[!] New tag found. Updating deployment...")
        update_kubernetes(latest_tag)
        save_tag(latest_tag)
    else:
        print("[✓] No new tag found. Nothing to do.")

if __name__ == "__main__":
    main()
