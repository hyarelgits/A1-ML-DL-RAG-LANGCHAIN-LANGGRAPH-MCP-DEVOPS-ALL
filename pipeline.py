# Python Pipeline Controller - Controls Entire Workflow
# Run: python3 pipeline.py
import subprocess
# # subprocess = To run shell commands from Python

def run(cmd):
    # # def run = Function to run one command, cmd = Command string
    print(f"Running: {cmd}")
    # # print = Show which command is running
    subprocess.run(cmd, shell=True, check=False)
    # # subprocess.run = Run command, shell=True = Run in shell, check=False = Don't stop on error, continue

if __name__ == "__main__":
    # # if __name__ == "__main__" = Run only if this file is run directly, not imported
    print("=== Pipeline Started ===")
    # # Print started
    run("pip install -r backend/requirements.txt")
    # # Step 1 - Install packages
    run("python3 backend/train_ai.py")
    # # Step 2 - Train AI
    run("python3 rag/rag.py")
    # # Step 3 - Run RAG
    run("docker build -t security-app:1.0 backend/")
    # # Step 4 - Build Docker
    run("helm upgrade --install security-app k8s/helm/security-app")
    # # Step 5 - Deploy Helm
    print("=== Pipeline Done ===")
    # # Print done
    print("App deployed via Helm, Argo CD will sync, Prometheus+Grafana monitoring, Jenkins logs")
    # # Print summary
