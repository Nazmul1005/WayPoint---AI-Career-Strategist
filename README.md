# 🎯 WayPoint - AI Career Strategist

**Your Expert Career Development Coach powered by LangChain and Streamlit**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg?style=for-the-badge&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Latest-green.svg?style=for-the-badge&logo=chainlink&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local_AI-blue.svg?style=for-the-badge)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-AI-purple.svg?style=for-the-badge&logo=google&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT_Models-black.svg?style=for-the-badge&logo=openai&logoColor=white)

WayPoint is an intelligent career coaching application that provides honest, actionable career guidance through AI-powered conversations. It features a modern, clean interface and sophisticated orchestration to guide you through career assessments, transitions, and growth.

---

## 🏗️ Project Structure

```bash
WayPoint/
├── app.py                 # 🚀 Main entry point - Streamlit Application
├── career_advisor.py      # 🧠 AI Brain - LangChain logic (Ollama, Gemini, OpenAI)
├── prompts.py             # 📝 Persona & Framework - System prompts & templates
├── config.py              # ⚙️ Settings - Constants & AI configuration
├── utils.py               # 🛠️ Helpers - Persona detection & guardrail logic
├── styles.css             # 🎨 Aesthetics - Custom glassmorphic styling
├── .env                   # 🔑 Secrets - API keys (gitignored)
└── requirements.txt       # 📦 Dependencies - Python packages
```

---

## ✨ Features

| Feature | Description |
| :--- | :--- |
| **🤖 Multi-Provider AI** | Support for **Ollama** (Local/Free), **Google Gemini** (Free API), and **OpenAI**. |
| **🧼 Simple Chat UI** | A streamlined, distraction-free chat interface using standard Streamlit components. |
| **🎭 Persona Detection** | Automatically identifies if you are a **Student**, **Professional**, or **Career Pivot-Seeker**. |
| **🛡️ Built-in Guardrails** | Expertly redirects legal, medical, or unethical queries to proper professional channels. |
| **🧠 Smart Context** | Persistent memory of conversation history and optional sidebar user context. |
| **🗺️ Actionable Roadmaps** | Provides specific strategic milestones and the "Monday Morning Test" action items. |

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository and navigate into it
cd WayPoint

# Install dependencies (ensure Python 3.8+ is installed)
pip install -r requirements.txt
```

### 2. Configure AI Provider

Edit the `.env` file to select your preferred AI brain:

- **Option A (Ollama):** Set `USE_OLLAMA=true`. Ensure [Ollama](https://ollama.com/) is running and run `ollama pull llama3.2`.
- **Option B (Gemini):** Add your `GOOGLE_API_KEY` and set `USE_OLLAMA=false`.
- **Option C (OpenAI):** Add your `OPENAI_API_KEY` and set `USE_OLLAMA=false`.

### 3. Launch the Application

```bash
streamlit run app.py
```

---

## 🎯 WayPoint Principles

> [!IMPORTANT]
> **The "Monday Morning Test"**
> Every major piece of advice response ends with a specific, immediate action the user can take right now to advance their career.

> [!TIP]
> **Diagnose Before Prescribing**
> WayPoint is designed to ask 2-3 targeted clarifying questions before providing a roadmap, ensuring advice is personalized to your skills and experience.

---

Developed with precision for modern career development.
