# Governor IT Q4 H1 - AI Robotics Education Platform

This is a comprehensive RAG (Retrieval-Augmented Generation) system for learning about humanoid robotics, ROS2, and AI integration. The platform combines a Docusaurus-based frontend with a FastAPI backend to provide an interactive chat interface for educational content.

## 🚀 Features

- **Interactive Chat Interface**: Ask questions about robotics, ROS2, and AI concepts
- **Semantic Search**: Powered by Cohere embeddings and Qdrant vector database
- **AI-Powered Answers**: Uses OpenRouter for context-aware responses
- **Educational Content**: Comprehensive modules on ROS2, Gazebo, Unity, NVIDIA Isaac, and Vision-Language-Action systems
- **Real-time Integration**: Frontend-backend communication for seamless experience

## 🛠️ Tech Stack

- **Frontend**: Docusaurus v3+, React 18+, JavaScript/TypeScript
- **Backend**: FastAPI, Python 3.8+
- **Vector Database**: Qdrant Cloud
- **Embeddings**: Cohere
- **LLM**: OpenRouter (GPT-3.5-turbo)
- **Architecture**: RAG (Retrieval-Augmented Generation)

## 📋 Prerequisites

- Node.js (v18 or higher)
- Python 3.8+
- npm or yarn
- Git

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Governor_IT_Q4_H1
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Install Python dependencies
pip install -r ingestion/requirements.txt
pip install -r retrieval/requirements.txt
pip install -r answer_generation/requirements.txt

# Create environment file (see .env.example)
cp .env.example .env

# Edit .env with your API keys
# (see Environment Variables section below)
```

### 3. Frontend Setup

```bash
# Navigate to frontend
cd frontend_H_book

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Start development server
npm start
```

### 4. Start the Backend Server

```bash
# From the backend directory
cd backend
python -m uvicorn api_server:app --host 0.0.0.0 --port 8002
```

## 🔐 Environment Variables

Create `.env` files in both the backend and frontend directories:

### Backend (.env)

```env
# Qdrant Configuration
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=book_content_chunks

# Cohere Configuration
COHERE_API_KEY=your_cohere_api_key_here

# Sitemap Configuration
SITEMAP_URL=https://your-site-url.com/sitemap.xml

# OpenRouter Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openai/gpt-3.5-turbo
APP_NAME=g-house-project
```

### Frontend (.env)

```env
NODE_ENV=development
REACT_APP_API_BASE_URL=http://localhost:8002
REACT_APP_AUTH_TOKEN=your_auth_token_if_required
```

## 🏗️ Project Structure

```
Governor_IT_Q4_H1/
├── backend/                 # FastAPI backend
│   ├── api_server.py       # Main API server
│   ├── ingestion/          # Content ingestion system
│   ├── retrieval/          # Semantic retrieval system
│   └── answer_generation/  # AI answer generation
├── frontend_H_book/        # Docusaurus frontend
│   ├── src/               # Source files
│   ├── docs/              # Educational content
│   ├── components/        # React components
│   └── pages/             # Page components
├── specs/                 # Project specifications
└── history/               # Prompt history records
```

## 📚 Educational Modules

The platform covers:

1. **ROS2 Fundamentals**: Core concepts of Robot Operating System 2
2. **Digital Twin Simulation**: Gazebo and Unity integration
3. **AI Robot Brain**: NVIDIA Isaac integration
4. **Vision-Language-Action**: Advanced robotics AI systems

## 🔧 API Endpoints

- `GET /health` - Health check
- `POST /retrieve` - Retrieve relevant content
- `POST /answer` - Generate answers from context
- `POST /qa` - Complete Q&A pipeline (retrieve + answer)

## 🤖 Usage

1. Start the backend server on port 8002
2. Start the frontend server on port 3000
3. Access the application at http://localhost:3000
4. Use the chat interface to ask questions about robotics content

## 📝 Notes

- The system is designed to work with educational robotics content
- API keys are required for vector database and LLM services
- The RAG system retrieves relevant content and generates contextual answers
- All sensitive information should be kept in environment variables

## 📄 License

[Add your license information here]