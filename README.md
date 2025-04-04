# 🧠 CodeTech Backend

AI-Powered Code Grading System — Backend Only (Ollama Edition)

CodeTech is a backend-only project that automates code grading using a local large language model (LLM) via [Ollama](https://ollama.com). Upload your source code files and get back detailed, structured feedback on correctness, efficiency, readability, and more — all without relying on external APIs like OpenAI.

---

## 🚀 Features

- 🔐 Secure File Upload API (supports `.py`, `.js`, etc.)
- ⚙️ Code Evaluation via Local LLM (Mistral / LLaMA3 using Ollama)
- 📝 Auto-generated HTML/JSON Reports with grading feedback
- 📂 Report download & file handling system
- 🔁 REST API with clean, testable architecture
- 🧪 Ready to demo via Postman or cURL — no frontend required

---

## 🧰 Tech Stack

| Layer         | Tech                     |
|--------------|--------------------------|
| Language      | Python / JavaScript     |
| Framework     | Flask / Express         |
| LLM Backend   | Ollama (Mistral, LLaMA) |
| File Handling | Multer / Flask-Uploads  |
| Report Output | HTML / JSON / PDF       |

---

## 📦 Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/your-username/codetech-backend.git
cd codetech-backend
```

### 2. Install Ollama & Run Model
```bash
brew install ollama           # or follow Linux instructions
ollama run mistral            # or llama2/llama3
```

### 3. Install Dependencies
```bash
# Python (Flask)
pip install -r requirements.txt

# Node.js (Express)
npm install
```

### 4. Run the Server
```bash
# Python
flask run

# Node
npm start
```

---

## 📡 API Endpoints

| Method | Route            | Description                            |
|--------|------------------|----------------------------------------|
| POST   | `/upload`        | Upload code file for grading           |
| POST   | `/grade`         | Analyze code and return report         |
| GET    | `/report/:id`    | Fetch specific grading report          |
| POST   | `/feedback`      | Submit feedback (optional)             |

---

## 📋 Sample Prompt to LLM
```text
Please grade the following Python code based on:
- Correctness
- Efficiency
- Readability
- Style
- Security
- Fragility

Also provide brief feedback for each section.

<INSERT CODE HERE>
```

---

## 🧪 Testing the API (via Postman)
- Upload your `.py` file to `/upload`
- Use the returned file path in `/grade`
- View or download the HTML report via `/report/:id`

---

## 🤝 Team

- **Khushi Kaushik** – Project Manager, AI/ML Integration  
- **Alyssa Amancio** – File Systems, Architecture  
- **Trang Ngo** – LLM Prompt Engineering, Report Generation

---

## 🧠 Stretch Goals

- ⚡ Offline-first local LLM performance improvements
- 📊 Add scoring customization and rubrics
- 🔐 JWT Authentication and user dashboard
- 🕸️ GitHub integration for pull request grading

---

## 📃 License
This project is for educational/demo purposes only.

---

## 💬 Feedback
Have suggestions? Submit them to `/feedback` or open an issue!

Happy grading! 🧠💻
