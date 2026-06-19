# 🧠 Sales Memory Agent

A Memory-Aware AI Sales Assistant powered by Hindsight AI that helps sales teams retain customer context, recall historical interactions, and generate personalized sales intelligence.

## 🚀 Problem Statement

Sales teams interact with prospects across multiple meetings, emails, demos, and follow-ups. Valuable context such as objections, budgets, timelines, competitor mentions, and stakeholder information is often lost between interactions.

Traditional CRMs store data but fail to intelligently utilize historical context during future engagements.

Sales Memory Agent solves this problem by providing persistent memory for AI-powered sales workflows.

---

## 💡 Key Features

### Memory Retention

* Store customer interactions as long-term memory
* Capture objections, budgets, competitors, and timelines
* Maintain deal-specific context

### Memory Recall

* Retrieve relevant historical interactions
* Surface important customer intelligence
* Provide contextual insights before meetings

### AI-Powered Sales Intelligence

* Generate personalized follow-up emails
* Create deal-specific sales briefs
* Compare responses with and without memory
* Improve customer engagement through contextual awareness

### Memory Inspector

* View retained memories
* Inspect recall activity
* Monitor memory usage and effectiveness

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │     User Interface  │
                    │      Streamlit      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │      Backend        │
                    └──────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
      ┌──────────────────┐      ┌──────────────────┐
      │  Hindsight AI    │      │ Local Fallback   │
      │ Memory Platform  │      │ Memory Store     │
      └────────┬─────────┘      └────────┬─────────┘
               │                         │
               └─────────────┬───────────┘
                             ▼
                  ┌─────────────────────┐
                  │      LLM Layer      │
                  │ Reasoning & Recall  │
                  └──────────┬──────────┘
                             ▼
                  Sales Intelligence Output
```

---

## 🛠️ Tech Stack

### Frontend

* Streamlit
* HTML/CSS
* Pandas

### Backend

* FastAPI
* Pydantic
* Uvicorn

### AI & Memory

* Hindsight AI
* LLM Integration
* Semantic Retrieval
* Context-Aware Memory Recall

### Development

* Python
* Git
* GitHub

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/tripathianand23/sales-memory-agent.git
cd sales-memory-agent
```

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd frontend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

---

## 📈 Business Impact

This solution can help organizations:

* Improve sales productivity
* Reduce information loss
* Generate personalized customer communication
* Accelerate deal progression
* Improve onboarding for new sales representatives
* Create institutional memory across teams

---

## 🎯 Future Scope

* Salesforce Integration
* HubSpot Integration
* Meeting Transcript Processing
* Voice Agent Support
* Multi-User Collaboration
* Real-Time Sales Coaching
* Analytics Dashboard
* Autonomous Follow-Up Generation

---

## 🏆 Hackathon Project

Built during a hackathon to demonstrate how memory-enabled AI can transform enterprise sales workflows by combining long-term memory with intelligent reasoning.

---

## 👨‍💻 Author

Anand Tripathi

GitHub: https://github.com/tripathianand23
LinkedIn: https://www.linkedin.com/in/YOUR-LINKEDIN/
