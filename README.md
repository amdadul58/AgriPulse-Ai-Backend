🌱 AgriPulse AI — Smart Agriculture & Crop Disease Advisor

An AI-powered agriculture platform designed to support farm management, crop disease detection, and agricultural decision-making.

AgriPulse AI is a smart agriculture project that combines backend APIs and AI components to support crop management, disease identification, and agricultural recommendations.

🚀 Key Features

- 🔐 Authentication: User registration and login APIs.
- 🚜 Farm Management: Create and retrieve farm records.
- 🌾 Crop Management: Manage crop information and planting details.
- 🦠 Disease Advisory: Analyze crop symptoms and provide disease-related guidance.
- 👁️ Vision AI: Image-based plant disease detection API.
- 🌱 Crop Recommendation: Support crop selection through recommendation functionality.
- 🧪 Fertilizer Recommendation: Provide fertilizer-related recommendations.
- 📚 RAG & Knowledge Retrieval: Retrieve relevant agricultural information from a knowledge base.
- 🔎 Vector Search: Search agricultural knowledge using vector embeddings.
- 🌦️ Weather Module: Weather-related functionality.
- 📖 API Documentation: Interactive API documentation through FastAPI Swagger UI.

«Feature availability and model behavior depend on the current implementation and configuration.»

🛠️ Technology Stack

Category| Technologies
Programming Language| Python
Backend Framework| FastAPI
API Architecture| REST API
Database| SQLite / PostgreSQL configuration
ORM & Database Access| SQLAlchemy / Async database components
AI & Deep Learning| TensorFlow/Keras, PyTorch components where configured
NLP & Generative AI| RAG and embedding-based retrieval workflows
Vector Database| ChromaDB
Database Migrations| Alembic
Testing| Pytest and project test scripts
Development Tools| Git, GitHub, Python Virtual Environment

📁 Project Structure

AgriPulse-Ai-Backend/
├── ai_models/               # AI models and model metadata
├── app/
│   ├── api/                 # API routes and endpoints
│   ├── core/                # Configuration, security and shared utilities
│   ├── models/              # Application/database models, if configured here
│   └── ...                  # Other application modules
├── dataset/
│   └── PlantVillage/        # Plant disease image dataset, if included
├── knowledge_base/
│   └── diseases/            # Agricultural disease knowledge
├── migrations/              # Database migration files
├── scripts/                 # Utility scripts
├── tests/                   # Automated and manual tests
├── .env.example             # Example environment configuration
├── .gitignore
├── alembic.ini              # Alembic configuration
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
├── train_model.py           # Model training script
├── ingest_knowledge.py      # Knowledge ingestion script
└── README.md

The structure above is a guide based on the repository's reported files. Refer to the actual source tree for the definitive structure.

⚙️ Installation & Setup

1. Prerequisites

Install:

- Python compatible with the project's dependencies
- pip
- Git
- PostgreSQL, if using PostgreSQL configuration

2. Clone the Repository

git clone https://github.com/amdadul58/AgriPulse-Ai-Backend.git
cd AgriPulse-Ai-Backend

3. Create a Virtual Environment

python -m venv venv

4. Activate the Environment

For Windows PowerShell:

.\venv\Scripts\Activate.ps1

If PowerShell blocks activation, you can run the virtual environment's Python directly or use an appropriate execution policy for your environment.

5. Install Dependencies

python -m pip install --upgrade pip
pip install -r requirements.txt

6. Configure Environment Variables

Create your local ".env" file using ".env.example" as a reference.

Set the database URL and other required settings according to "app/core/config.py" and the project's configuration.

Security: Never publish real passwords, API keys, database credentials, or production secrets.

7. Run the Backend

python run.py

If the project entry point is configured to launch Uvicorn, the API server should start at the configured host and port.

📖 API Documentation

When the backend is running locally, open:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

The actual routes depend on the current application configuration.

🧪 Testing

The repository contains test-related files, including:

- "tests/"
- "test_db.py"
- "test_prediction.py"
- "test_treatments.py"
- "check_db.py"

Run automated tests with:

pytest

Run individual scripts only after checking their configuration and required environment variables.

🧠 AI & Knowledge Components

The project includes resources for plant disease image classification and agricultural knowledge retrieval.

- Model training and evaluation workflows
- Plant disease image dataset resources
- Disease knowledge base
- Knowledge ingestion utilities
- Vector search and retrieval components

Actual prediction accuracy and supported disease classes depend on the model, dataset, and configuration used.

🔗 Related Project

AgriPulse AI Frontend:
https://github.com/amdadul58/AgriPulse-Ai-Frontend

👨‍💻 Developer

Amdadul Haque
AI Engineering | Full-Stack Development | Generative AI | Computer Vision | MLOps

- GitHub: https://github.com/amdadul58
- LinkedIn: https://www.linkedin.com/in/amdadul58
- Email: amdadulhaque.as@gmail.com

📌 Project Purpose

AgriPulse AI is a project-based learning and development initiative focused on combining AI engineering, backend development, knowledge retrieval, and smart agriculture applications.

---

Built by Amdadul Haque | AgriPulse AI
