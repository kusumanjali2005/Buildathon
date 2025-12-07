# Buildathon
# 🇮🇳 AI Legal Aid Assistant

An intelligent, multi-language legal aid assistant designed for Indian citizens. Get legal guidance in 11 Indian languages with voice input and text-to-speech support.

## 📋 Table of Contents

- [Features](#features)
- [Supported Languages](#supported-languages)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- 🌐 **Multi-Language Support**: Communicate in 11 Indian languages
- 🎤 **Voice Input**: Speak your questions in your native language
- 🔊 **Text-to-Speech**: Listen to responses in your preferred language
- ⚖️ **Legal Guidance**: Get simple explanations of legal rights and procedures
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🚀 **Fast & Efficient**: Powered by OpenAI GPT-4o-mini

## 🌍 Supported Languages

1. English
2. Hindi (हिंदी)
3. Kannada (ಕನ್ನಡ)
4. Telugu (తెలుగు)
5. Tamil (தமிழ்)
6. Marathi (मराठी)
7. Gujarati (ગુજરાતી)
8. Bengali (বাংলা)
9. Malayalam (മലയാളം)
10. Punjabi (ਪੰਜਾਬੀ)
11. Odia (ଓଡ଼ିଆ)

## 🛠️ Technology Stack

### Frontend
- HTML5
- CSS3
- JavaScript (ES6+)
- Web Speech API

### Backend
- Python 3.11+
- FastAPI
- OpenAI API (GPT-4o-mini)
- Pydantic
- python-dotenv

## 📦 Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Modern web browser (Chrome/Edge recommended for voice features)

### Step 1: Clone the Repository

git clone <repository-url>
cd Legal-Aid-Assistant### Step 2: Install Python Dependencies

pip install -r requirements.txt### Step 3: Set Up Environment Variables

Create a `.env` file in the root directory:
v
OPENAI_API_KEY=your_openai_api_key_here**Important**: Never commit your `.env` file to version control!

### Step 4: Start the Backend Server

uvicorn main:app --reloadThe server will start at `http://127.0.0.1:8000`

### Step 5: Open the Frontend

- Option 1: Simply open `index.html` in your web browser
- Option 2: Use a local server (recommended):
  
  # Using Python
  python -m http.server 8001
  
  # Then open http://localhost:8001/index.html
  ## 🚀 Usage

1. **Select Language**: Choose your preferred language from the dropdown
2. **Enter Your Question**: 
   - Type your legal question in the text area, OR
   - Click the 🎤 microphone button and speak your question
3. **Enable Voice Output** (Optional): Toggle "Enable Voice Assistant" to hear responses
4. **Submit**: Click "Ask Lawyer AI" button
5. **Read Response**: The AI will respond in your selected language

### Example Queries

- "What are my rights as a tenant?"
- "How to file a consumer complaint?"
- "What should I do if my landlord doesn't return my deposit?"
- "My property documents are missing, what should I do?"

## 📡 API Documentation

### Base URL
