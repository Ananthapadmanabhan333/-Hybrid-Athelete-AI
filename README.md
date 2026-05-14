# Fuelix - Hybrid Athlete AI Training Platform

An intelligent AI-powered fitness platform designed for hybrid athletes, combining strength training, endurance work, and recovery optimization through advanced machine learning.

## 🎯 About

Fuelix is a comprehensive training platform that uses AI to create personalized workout plans, track progress, provide nutrition guidance, and optimize recovery for athletes pursuing both strength and endurance goals.

## ✨ Features

### 🤖 AI-Powered Training
- Personalized workout generation based on athlete profile
- Adaptive training plans that evolve with your progress
- Intelligent exercise selection and progression
- Real-time form feedback and coaching

### 📊 Progress Tracking
- Comprehensive training session logging
- Performance metrics and analytics
- Progress visualization and trends
- Injury tracking and prevention

### 🥗 Nutrition Management
- Personalized nutrition recommendations
- Meal logging and tracking
- Water intake monitoring
- Macro and calorie tracking

### 💬 AI Coach
- Interactive AI coach for guidance and motivation
- Training conversation history
- Personalized feedback and recommendations
- Recovery and wellness monitoring

### 📱 Modern Interface
- Beautiful, responsive Flutter frontend
- Dark mode optimized design
- Intuitive user experience
- Cross-platform support (Web, iOS, Android)

## 🛠️ Tech Stack

### Backend
- **Framework:** FastAPI (Python)
- **Database:** SQLite with SQLAlchemy ORM
- **Authentication:** JWT tokens with bcrypt password hashing
- **AI Engine:** Custom AI orchestrator for workout generation

### Frontend
- **Framework:** Flutter (Dart)
- **State Management:** Provider pattern
- **UI Design:** Material Design with custom theming
- **API Communication:** HTTP client with authentication

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Flutter SDK 3.0+
- Git

### Backend Setup

1. Navigate to backend directory:
\`\`\`bash
cd backend
\`\`\`

2. Install dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. Create database tables:
\`\`\`bash
python create_tables.py
\`\`\`

4. Start the server:
\`\`\`bash
uvicorn app.main:app --reload
\`\`\`

Backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
\`\`\`bash
cd frontend
\`\`\`

2. Get Flutter dependencies:
\`\`\`bash
flutter pub get
\`\`\`

3. Run the app:
\`\`\`bash
flutter run -d chrome
\`\`\`

## 📁 Project Structure

\`\`\`
fuelix/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Security, config
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── ai_engine/    # AI training logic
│   └── create_tables.py
├── frontend/
│   └── lib/
│       ├── features/     # Feature modules
│       ├── services/     # API services
│       └── core/         # Constants, themes
└── README.md
\`\`\`

## 🔐 Authentication

The platform uses secure JWT-based authentication with:
- Bcrypt password hashing with automatic truncation
- Token-based session management
- Protected API endpoints
- Secure user registration and login

## 🤝 Contributing

This is a personal project, but suggestions and feedback are welcome!

## 📄 License

This project is private and proprietary.

## 👨‍💻 Developer

Developed by Ananthapadmanabhan

---

**Note:** This is an active development project. Features and documentation are continuously being updated.
