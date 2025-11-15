#  AI Verifier

**Analyze any claim --- powered by AI and trusted fact-checking
sources.**\
A full-stack application that combines **FastAPI**, **Next.js**,
**TailwindCSS**, and **Ollama (Llama 3)** to verify information and
analyze statements using both real fact-checking APIs and local AI
models.

------------------------------------------------------------------------

##  Overview

AI Verifier is a local showcase project built to demonstrate how
artificial intelligence can assist in verifying news, claims, or online
statements.\
The system cross-checks information through multiple **fact-checking
APIs** (e.g., Google Fact Check) and leverages an **AI model (via
Ollama)** to analyze and summarize the results.

This project was designed as a **portfolio-grade example** --- modular,
clean, and fully containerized using Docker.

------------------------------------------------------------------------

##  Architecture

    frontend/   → Next.js + TailwindCSS interface
    backend/    → FastAPI application (API routes, AI integration, and database)
    ollama/     → Local AI model service (Llama 3)
    docker-compose.yml  → Unified environment setup
    .env.example        → Template for environment configuration

The app follows a **3-tier architecture**:

1.  **Frontend (Next.js)** --- beautiful and responsive UI for
    submitting claims and viewing analyzed results.\
2.  **Backend (FastAPI)** --- orchestrates API requests, aggregates
    fact-check results, and manages local AI calls.\
3.  **AI Service (Ollama)** --- runs Llama 3 locally to analyze claims
    and generate natural summaries.

------------------------------------------------------------------------

##  Tech Stack

  Layer              Technologies
  ------------------ ---------------------------------
  **Frontend**       Next.js 13+, React, TailwindCSS
  **Backend**        FastAPI, Python 3.11, Requests
  **AI Layer**       Ollama (Llama 3 model)
  **DevOps**         Docker, Docker Compose
  **Integrations**   Google Fact Check API

------------------------------------------------------------------------

##  Environment Variables

Before running, create a `.env` file in the root directory (based on
`.env.example`):

``` bash
cp .env.example .env
```

Then open `.env` and fill in your credentials:

    GOOGLE_FACTCHECK_API_KEY=YOUR_GOOGLE_API_KEY
    OLLAMA_HOST=http://ollama:11434
    ENVIRONMENT=development

> ⚠️ Do **not** commit your `.env` file --- it's already ignored via
> `.gitignore`.

------------------------------------------------------------------------

## 🐳 Running Locally (Docker)

The entire project runs in containers.\
To build and start all services:

``` bash
docker compose up --build
```

Then open your browser at:

    Frontend: http://localhost:3000
    Backend:  http://localhost:8000/docs
    Ollama:   http://localhost:11434

> The backend automatically checks if the **Llama 3 model** is available
> inside the Ollama container and pulls it if needed.

------------------------------------------------------------------------

##  How It Works

1.  **User inputs a claim** (e.g. "NASA confirms new life on Mars").\
2.  **Backend** queries multiple **fact-check APIs** for relevant
    articles.\
3.  **AI Model (Ollama)** analyzes the claim and those sources.\
4.  The result is returned to the frontend, where it appears as elegant,
    interactive cards:
    -   Source details (publisher, title, rating)
    -   AI-generated summary
    -   Option to save the result to your local history

------------------------------------------------------------------------

##  UI Highlights

-   Clean, modern design using **TailwindCSS**
-   Responsive layout (works beautifully on desktop and mobile)
-   Soft color palette and subtle animations
-   Cards with hover effects and action buttons (`View Source`,
    `Show AI Summary`, `Save to History`)
-   Global Navbar with routes: `/` (Verify) and `/history`

------------------------------------------------------------------------

##  Development Tips

Useful commands for local development:

``` bash
# Rebuild containers after code changes
docker compose build

# Stop containers
docker compose down

# View backend logs
docker compose logs backend -f
```

------------------------------------------------------------------------

##  Project Structure

    ai-verifier/
    ├── backend/
    │   ├── app/
    │   │   ├── api/          # Fact-checking routes and AI integrations
    │   │   ├── core/         # Config and utility logic
    │   │   └── main.py       # FastAPI entry point
    │   ├── Dockerfile
    │   └── requirements.txt
    │
    ├── frontend/
    │   ├── app/              # Next.js pages and components
    │   ├── components/       # Reusable UI components (ResultCard, etc.)
    │   ├── Dockerfile
    │   └── package.json
    │
    ├── docker-compose.yml
    ├── .env.example
    └── README.md

------------------------------------------------------------------------

##  Future Improvements

-   Add support for multiple AI models (e.g., Mistral, Phi-3)
-   Integrate with OpenAI or Anthropic for optional cloud analysis
-   Implement database persistence for user history (PostgreSQL)
-   Build an API documentation page in the frontend
-   Add light/dark mode toggle

------------------------------------------------------------------------

##  Demo Video

🎥 Watch the 1:25 demo on
[LinkedIn](https://linkedin.com/in/enrico-mann)\
See how the app verifies claims and generates instant summaries using
local AI.

------------------------------------------------------------------------

##  Author

**Built by [Enrico Mann](https://github.com/EnricoMann)**\
💡 Web & Data Engineer passionate about AI, data pipelines, and
real-world problem-solving.

------------------------------------------------------------------------

## 📄 License

This project is released under the [MIT
License](https://opensource.org/licenses/MIT).\
Feel free to fork, modify, and learn from it.
