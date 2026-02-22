"""
Configuration settings for WayPoint AI Career Strategist
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration - Support Ollama (local), Google Gemini (free), and OpenAI (paid)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
USE_OLLAMA = os.getenv("USE_OLLAMA", "true").lower() == "true"  # Default to Ollama

# Determine which provider to use
# Priority: Ollama (local, free) > Google Gemini (free) > OpenAI (paid)
if USE_OLLAMA:
    AI_PROVIDER = "ollama"
    API_KEY = None  # Ollama doesn't need API key
    MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2")  # Local model
elif GOOGLE_API_KEY:
    AI_PROVIDER = "gemini"
    API_KEY = GOOGLE_API_KEY
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-pro-latest")
elif OPENAI_API_KEY:
    AI_PROVIDER = "openai"
    API_KEY = OPENAI_API_KEY
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
else:
    AI_PROVIDER = None
    API_KEY = None
    MODEL_NAME = None

MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "0.7"))
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Conversation Configuration
MAX_CONVERSATION_HISTORY = int(os.getenv("MAX_CONVERSATION_HISTORY", "10"))

# UI Configuration
APP_TITLE = "🎯 WayPoint - AI Career Strategist"
APP_SUBTITLE = "Your Expert Career Development Coach"
SIDEBAR_TITLE = "📋 Your Career Context"

# Tech Stack Database (2024-2025)
TECH_STACKS = {
    "web_frontend": [
        "React", "Next.js 14", "TypeScript", "Tailwind CSS", 
        "Shadcn/ui", "Vite", "Vue 3", "Svelte"
    ],
    "web_backend": [
        "FastAPI", "Django", "Node.js", "Express", 
        "NestJS", "Prisma", "PostgreSQL", "MongoDB", "Redis"
    ],
    "data_ai": [
        "Python", "Pandas", "NumPy", "Scikit-learn",
        "PyTorch", "TensorFlow", "Hugging Face", "LangChain",
        "OpenAI API", "Pinecone", "Weights & Biases"
    ],
    "mobile": [
        "React Native", "Flutter", "Swift", "Kotlin",
        "Expo", "SwiftUI", "Jetpack Compose"
    ],
    "devops": [
        "Docker", "Kubernetes", "GitHub Actions", "CI/CD",
        "AWS", "Azure", "Google Cloud", "Terraform", "Ansible"
    ],
    "tools": [
        "Git", "VS Code", "Jira", "Postman", "Figma",
        "Linear", "Notion", "Slack", "Discord"
    ]
}

# Learning Resources
RESOURCES = {
    "documentation": [
        "MDN Web Docs", "React Docs", "Next.js Docs",
        "Python Official Docs", "TypeScript Handbook"
    ],
    "courses": [
        "Coursera", "freeCodeCamp", "The Odin Project",
        "Fast.ai", "Deep Learning Specialization (Coursera)",
        "Full Stack Open"
    ],
    "practice": [
        "LeetCode", "HackerRank", "CodeWars",
        "Frontend Mentor", "Kaggle", "GitHub"
    ],
    "communities": [
        "Stack Overflow", "Dev.to", "Hashnode",
        "Reddit (r/cscareerquestions)", "Discord servers"
    ]
}

# Validation Settings
GUARDRAILS = {
    "legal_keywords": ["visa", "contract", "lawsuit", "legal advice", "immigration"],
    "medical_keywords": ["depression", "anxiety", "therapy", "mental health diagnosis", "medication"],
    "unethical_keywords": ["lie on resume", "fake reference", "cheat", "plagiarize"]
}
