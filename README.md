# ⚡ Fuelix — Hybrid Athlete AI Training & Analytics Platform

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Flutter](https://img.shields.io/badge/Frontend-Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white)](https://flutter.dev)
[![Docker](https://img.shields.io/badge/Deployment-Docker--Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)
[![Python](https://img.shields.io/badge/ML%20Engine-PyTorch%20%26%20YAML-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://pytorch.org)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%20%26%20SQLite-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)

Fuelix is an **intelligent, production-grade, AI-driven fitness and recovery platform** engineered specifically for **hybrid athletes**—individuals simultaneously optimizing for extreme endurance (running, cycling, swimming) and high-intensity strength performance (powerlifting, weightlifting). 

Driven by a custom-orchestrated multi-agent ML architecture, Fuelix dynamically synthesizes training regimens, adapts plans to real-time recovery metrics, offers personalized macro nutrition systems, and mitigates injury risks through deep predictive analytics.

---

## 🏛️ System Architecture

Fuelix utilizes a robust, micro-segmented architecture orchestrating high-fidelity communication between a cross-platform client, an Nginx reverse-proxy, a FastAPI backend server, local/production relational databases, and a specialized offline ML adapter-training pipeline.

```mermaid
graph TD
    %% Styling
    classDef client fill:#02569B,stroke:#013B6B,stroke-width:2px,color:#fff;
    classDef proxy fill:#009639,stroke:#006622,stroke-width:2px,color:#fff;
    classDef backend fill:#009688,stroke:#00695C,stroke-width:2px,color:#fff;
    classDef db fill:#4169E1,stroke:#1A365D,stroke-width:2px,color:#fff;
    classDef ml fill:#FF6F00,stroke:#E65100,stroke-width:2px,color:#fff;

    %% Components
    A["📱 Flutter Mobile/Web App"] :::client
    B["🌐 Modern HTML5/JS Landing Page"] :::client
    C["🔒 Nginx Reverse Proxy (Port 80)"] :::proxy
    
    subgraph FastAPI_Core ["FastAPI Core Platform"]
        D["⚙️ API Gateway (CORS / JWT Auth)"] :::backend
        E["🧠 AI Orchestrator (v4 / v5)"] :::backend
        F["🏃‍♂️ Engine Cluster (Metabolic, Injury, Recovery)"] :::backend
    end
    
    subgraph Data_Layer ["Data Storage & Seeding"]
        G["🗄️ PostgreSQL (Prod) / SQLite (Dev)"] :::db
        H["🌱 Data Seeding & Migrations (Alembic)"] :::db
    end

    subgraph ML_Pipeline ["Offline ML Training Pipeline"]
        I["📊 Dataset Generator & Cleaner"] :::ml
        J["🎯 Fine-Tuning Adapters (Coach, Medical, Nutrition, Recovery)"] :::ml
    end

    %% Connections
    A -->|HTTPS / REST API| C
    B -->|Static Requests| C
    C -->|Reverse Proxy /api/v1| D
    
    D --> E
    E --> F
    F -->|SQLAlchemy ORM| G
    H -->|Seed / Migrate| G
    
    I -->|JSONL Datasets| J
    J -.->|Engine Adapters / Weights| E
```

---

## ✨ Features & Core Engines

At the heart of Fuelix is a cluster of high-performance analytics engines designed to calculate and adapt training targets dynamically:

### 1. 🧠 Custom AI Orchestrator (v4 / v5) & Agent Suite
* **Pro-Coach Mode**: Real-time interactive AI coach that tracks conversational histories and acts as an autonomous athletic advisor.
* **Context-Aware Recommendations**: Leverages specialized downstream weights to formulate highly context-specific, professional coaching inputs.

### 2. 🏃‍♂️ Dynamic Athlete Engine Cluster
* **Adaptive Training Engine**: Adjusts training volume, frequency, and intensity based on continuous feedback loops.
* **Recovery Engine v4**: Aggregates heart-rate variability, sleep quality, subjective soreness, and stress inputs to compute daily physical readiness scores.
* **Metabolic & Nutrition Engine**: Tailors daily caloric targets, macronutrient breakdowns (protein, fats, carbohydrates), and hydration schedules to match daily training load demands.
* **Injury Awareness & Prevention Engine**: Flags progressive fatigue, highlights movement pattern vulnerabilities, and curates proactive deload periods.
* **Body Composition & Mental Performance Engines**: Tracks lean body mass changes and logs mental resilience, grit index, and focus metrics over time.

### 3. 🎯 Machine Learning Finetuning Pipeline
* **Synthetic Dataset Generator**: Builds high-entropy JSONL training files matching sophisticated hybrid athlete personas.
* **Multi-Adapter Finetuning**: Standard scripts for training distinct LoRA adapters:
  * `train_coach_adapter.py`: Specializes the LLM on exercise programming and high-performance communication.
  * `train_medical_adapter.py`: Restricts advice to safe, non-invasive physiological bounds.
  * `train_nutrition_adapter.py`: Maximizes metabolic efficiency calculations and energy availability.
  * `train_recovery_adapter.py`: Focuses on supercompensation curves and stress-reduction protocols.

---

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend UI** | **Flutter (Dart)** | Cross-platform (iOS, Android, Web) compiled UI, leveraging the `Provider` pattern for state management. |
| **Landing Web** | **HTML5 / Vanilla CSS / JS** | High-performance, SEO-optimized landing page featuring premium CSS styling, auth overlays, and fluid micro-animations. |
| **Backend API** | **FastAPI (Python)** | High-throughput, asynchronous web server framework utilizing Pydantic schemas and SQLAlchemy ORM. |
| **Databases** | **PostgreSQL & SQLite** | Scalable relational storage mapping detailed profiles, exercises, nutritional logs, and chats. |
| **Dockerization** | **Nginx & Docker Compose** | Orchestrated production runtime featuring Nginx reverse-proxies routing both static frontend assets and API requests seamlessly. |

---

## 📁 Repository Structure

```
fuelix/
├── backend/
│   ├── app/
│   │   ├── api/                           # API Routes (auth, training, metrics, coach)
│   │   ├── core/                          # Security, JWT tokens, configuration settings
│   │   ├── models/                        # DB tables (User, Exercise, Workout, Chat, Recovery)
│   │   ├── schemas/                       # Pydantic validation schemas
│   │   ├── adaptive_training_engine/      # Workload adjustments
│   │   ├── ai_orchestrator_v4/            # Multi-agent orchestrators
│   │   ├── recovery_engine_v4/            # Recovery algorithms
│   │   └── main.py                        # FastAPI startup entry point
│   ├── alembic/                           # Database migration history
│   ├── seed_all_data.py                   # Automated synthetic database populator
│   ├── requirements.txt                   # Backend dependencies
│   └── Dockerfile                         # Backend multi-stage builder
├── frontend/
│   ├── lib/
│   │   ├── core/                          # Theme, styles, constants, routing
│   │   ├── features/                      # Workout logging, dashboard, coach chat pages
│   │   └── services/                      # API network layer
│   ├── web/                               # Flutter Web deployment wrappers
│   ├── nginx.conf                         # Production Nginx reverse-proxy configuration
│   └── Dockerfile                         # Flutter-web compiler & static server image
├── landing/                               # Dynamic, lightweight client marketing/auth page
│   ├── index.html                         # Beautiful structure and layouts
│   ├── styles.css                         # Modern styling and custom animations
│   └── script.js                          # Auth modal flows and client-side validation
├── ml/
│   └── fuelix_training/
│       ├── dataset_builder.py             # Compiles synthetic samples
│       ├── synthetic_dataset_generator.py # Formulates diverse persona files
│       ├── train_coach_adapter.py         # Downstream coach fine-tuning
│       └── requirements_ml.txt            # ML/PyTorch dependencies
├── docker-compose.yml                     # Development container orchestrations
├── docker-compose.prod.yml                # Production multi-container suite
├── start-prod.sh                          # Production runner for Unix platforms
└── start-prod.bat                         # Production runner for Windows platforms
```

---

## 🚀 Local Development Setup

### 1. Backend Setup
Create your virtual environment, install local packages, perform migrations, seed test data, and launch FastAPI:
```bash
cd backend
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Unix
source .venv/bin/activate

pip install -r requirements.txt
python create_tables.py
python seed_all_data.py
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
* API docs are immediately viewable at: `http://localhost:8000/docs`

### 2. Frontend Setup
Launch the Flutter Web application in developer mode:
```bash
cd frontend
flutter pub get
flutter run -d chrome
```

### 3. ML Fine-Tuning Setup
Generate synthetic data files and run custom adapter trainers:
```bash
cd ml/fuelix_training
pip install -r requirements_ml.txt
python synthetic_dataset_generator.py
python train_coach_adapter.py
```

---

## 🐳 Production Deployment (Nginx & Docker Compose)

Deploy the full-stack container suite including the PostgreSQL database, FastAPI app, and Nginx-based Flutter static web server.

### 🌐 Automatic Deployment Scripts
We supply dedicated, cross-platform deploy scripts that automatically handle downing active containers, copying sample configurations, rebuilding environments, and launching backend/frontend ports.

#### For Linux / macOS:
```bash
chmod +x start-prod.sh
./start-prod.sh
```

#### For Windows:
Double-click `start-prod.bat` or run:
```cmd
start-prod.bat
```

### 📦 Manual Deployment
Alternatively, configure the variables in your `.env` file, then launch standard commands:
```bash
# Bring down any pre-existing containers
docker-compose -f docker-compose.prod.yml down

# Build images
docker-compose -f docker-compose.prod.yml build

# Start detached production services
docker-compose -f docker-compose.prod.yml up -d
```

Once running successfully, the stack routes as follows:
* **User/Client Access (Nginx)**: `http://localhost`
* **Secure API Gateway (Reverse Proxied)**: `http://localhost/api/v1`
* **PostgreSQL Engine**: `http://localhost:5432`

---

## 🛡️ Security & Authentication

Fuelix employs strict enterprise-grade security protocols:
* **JWT Authentication**: Secure Bearer tokens utilizing standard cryptography.
* **Robust Password Hashing**: Hashed via standard `bcrypt` algorithms to safeguard credentials.
* **Docker Network Isolation**: The PostgreSQL container (`fuelix_db`) has no external public facing ports unless configured otherwise, communicating solely via the internal private Docker bridge network to `fuelix_backend`.
