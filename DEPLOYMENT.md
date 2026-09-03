# 🚀 MedAssist-AI — Cloud Deployment, Postman & DevOps Guide

This document fulfills the **Milestone 4 Cloud & DevOps Requirements**:
- **Dev & Deployment Tools**: VS Code, Git + GitHub, Docker & Docker Compose
- **Cloud Deployment**: AWS / Azure (100% Free-Tier eligible instructions) + Zero-Credit PaaS option
- **API Testing**: Postman Collection (`MedAssist_AI_Postman_Collection.json`)
- **Monitoring & Logging**: Health checks, container telemetry, and access logs

---

## 📋 Table of Contents
1. [100% Free AWS Cloud Deployment (EC2 Free Tier)](#1-100-free-aws-cloud-deployment-ec2-free-tier)
2. [100% Free Azure Cloud Deployment (Azure for Students / Free Tier)](#2-100-free-azure-cloud-deployment-azure-for-students--free-tier)
3. [Zero-Credit-Card Free Cloud Alternative (Render.com)](#3-zero-credit-card-free-cloud-alternative-rendercom)
4. [Postman API Testing Setup](#4-postman-api-testing-setup)
5. [Monitoring & Logging Tools](#5-monitoring--logging-tools)

---

## 1. 100% Free AWS Cloud Deployment (EC2 Free Tier)

AWS offers **750 hours/month of free `t2.micro` or `t3.micro` instance usage** for 12 months under the AWS Free Tier.

### Step 1: Launch an AWS EC2 Free Tier Instance
1. Log in to the [AWS Management Console](https://aws.amazon.com/console/).
2. Navigate to **EC2** $\rightarrow$ Click **Launch Instance**.
3. **Name**: `medassist-ai-server`
4. **OS Image**: **Ubuntu Server 24.04 LTS** (Free tier eligible).
5. **Instance Type**: `t2.micro` (or `t3.micro` depending on region — both free tier eligible).
6. **Key Pair**: Create a new key pair (e.g. `medassist-key.pem`) and download it.
7. **Network Settings (Security Group)**:
   - Check **Allow SSH traffic from Anywhere (0.0.0.0/0)**
   - Check **Allow HTTP traffic from the internet (Port 80)**
   - Check **Allow HTTPS traffic from the internet (Port 443)**
   - Click **Add security group rule** $\rightarrow$ Custom TCP $\rightarrow$ Port `3000` $\rightarrow$ Anywhere (for direct frontend access)
   - Click **Add security group rule** $\rightarrow$ Custom TCP $\rightarrow$ Port `8000` $\rightarrow$ Anywhere (for direct API access)
8. **Storage**: Keep default **30 GB gp3** (Free tier allows up to 30 GB free storage).
9. Click **Launch Instance**.

### Step 2: Connect to your EC2 Instance
Open your terminal (PowerShell / Command Prompt / Git Bash) in the folder where your `medassist-key.pem` is saved:

```bash
# Set key permissions (if on Mac/Linux)
chmod 400 medassist-key.pem

# SSH into your EC2 server (replace with your EC2 Public IP)
ssh -i "medassist-key.pem" ubuntu@YOUR_EC2_PUBLIC_IP
```

### Step 3: Install Docker & Docker Compose (1-minute setup)
On your EC2 server, run:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl openssl

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
```

### Step 4: Clone & Launch MedAssist-AI
```bash
# Clone the repository
git clone https://github.com/HEMANTH-KARUMANCHI/MedAssist-AI.git
cd MedAssist-AI

# Run Docker Compose in detached mode
docker compose up --build -d
```

### Step 5: Access Your Live Application
- **Frontend Web Portal**: `http://YOUR_EC2_PUBLIC_IP:3000`
- **FastAPI Documentation & Swagger UI**: `http://YOUR_EC2_PUBLIC_IP:8000/docs`

---

## 2. 100% Free Azure Cloud Deployment (Azure for Students / Free Tier)

Azure provides **$100 in free credits + 12 months of free B1s virtual machines** (or Azure App Service F1 Free tier).

### Step 1: Create an Azure Linux Virtual Machine
1. Open the [Azure Portal](https://portal.azure.com/).
2. Click **Create a Resource** $\rightarrow$ **Virtual Machine**.
3. **Resource Group**: `MedAssist-RG`
4. **Virtual Machine Name**: `medassist-ai-vm`
5. **Image**: `Ubuntu Server 22.04 LTS` (Gen 2).
6. **Size**: `Standard_B1s` (1 vcpu, 1 GiB memory — Free tier eligible).
7. **Inbound Port Rules**: Select `SSH (22)`, `HTTP (80)`, `HTTPS (443)`.
8. Under **Networking**, add Inbound Port Rules for `3000` and `8000`.
9. Click **Review + Create**.

### Step 2: Deploy Containers via SSH
```bash
ssh azureuser@YOUR_AZURE_PUBLIC_IP
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker

git clone https://github.com/HEMANTH-KARUMANCHI/MedAssist-AI.git
cd MedAssist-AI
docker compose up --build -d
```

---

## 3. Zero-Credit-Card Free Cloud Alternative (Render.com)

If you do not want to provide a credit card for AWS/Azure verification, **Render.com** provides 100% free hosting for web services and static sites:

1. **Free PostgreSQL Database**:
   - Go to [dashboard.render.com](https://dashboard.render.com) $\rightarrow$ New **PostgreSQL** (Free tier).
   - Copy the database connection URL.
2. **Free Backend Container**:
   - New **Web Service** $\rightarrow$ Connect GitHub Repo $\rightarrow$ Select `backend/Dockerfile`.
   - Add environment variables: `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `SECRET_KEY`.
3. **Free Frontend**:
   - New **Static Site** $\rightarrow$ Root: `frontend` $\rightarrow$ Build: `npm install && npm run build` $\rightarrow$ Publish: `dist`.

---

## 4. Postman API Testing Setup

We have included a pre-configured, comprehensive Postman Collection:
👉 **[`MedAssist_AI_Postman_Collection.json`](file:///c:/Users/Hemanth/Documents/Projects_2026/MedAssist-AI/MedAssist_AI_Postman_Collection.json)**

### How to Import & Run in Postman:
1. Open **Postman**.
2. Click **Import** (top left) $\rightarrow$ Select `MedAssist_AI_Postman_Collection.json`.
3. The collection contains 5 organized folders:
   - **1. Authentication**: User Registration & Login (Auto-captures JWT Bearer Token into collection variables).
   - **2. AI Predictions & ML Models**: Typo-resilient disease prediction, symptom list, and patient risk assessment.
   - **3. Patient Medical Records**: Profile retrieval, symptom recording, and PDF medical report downloads.
   - **4. Caretaker Clinical Modules**: Assigned patients, Caretaker analytics, Care plan formulation & deletion.
   - **5. System Health & Monitoring**: Backend status check.
4. Set the `baseUrl` variable to `http://localhost:8000` (or `http://YOUR_AWS_PUBLIC_IP:8000`).
5. Run the **Login** request $\rightarrow$ The JWT token is automatically saved and passed in the `Authorization` header for all protected endpoints!
6. Click **Run Collection** to execute all automated test assertions with 1 click.

---

## 5. Monitoring & Logging Tools

### A. Live Container Telemetry & Stats
View CPU usage, memory consumption, and network I/O in real time:
```bash
docker stats
```

### B. Container Access & Error Logs
Inspect live output from any running container:
```bash
# View backend logs (including FastAPI requests & ML inference times)
docker logs -f medassist_backend

# View database query logs
docker logs -f medassist_db

# View Nginx web server access logs
docker logs -f medassist_frontend
```

### C. Automated Health Check Endpoint
- Backend Health Probe: `GET http://localhost:8000/` $\rightarrow$ Returns `{"message": "MedAssist AI Backend is running"}`
- Swagger Interactive Documentation & Diagnostics: `http://localhost:8000/docs`
