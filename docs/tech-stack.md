# Mystery.AI - Technology Stack (MVP)

This document outlines the specific technologies and their versions selected for the Minimum Viable Product (MVP) of the Mystery.AI system.

## 1. Core Programming Language

-   **Language:** Python
    -   **Version:** 3.12.3 (as per user's environment)
    -   **Rationale:** Specified by the user; excellent ecosystem for AI/ML development; required by the OpenAI Agents SDK.

## 2. AI Agent Framework

-   **Framework:** OpenAI Agents SDK
    -   **Version:** Latest stable version available at the start of development (e.g., `openai-agents==X.Y.Z`). To be specified in `requirements.txt`.
    -   **Python Import:** `import agents`
    -   **Rationale:** Core requirement for the project. Provides primitives for defining agents, orchestration, structured outputs, and LLM interaction.
    -   **Key Primitives to be Used:** `agents.Agent`, `agents.Runner`, Pydantic models for `output_type`.

## 3. Language Models (LLMs)

-   **Provider:** OpenAI
-   **Models (accessed via Agents SDK):**
    -   `gpt-4.1` (or specific variants like `gpt-4-turbo`)
    -   `gpt-4.1-mini`
    -   `gpt-4.1-nano`
    -   `o3`
    -   `o4-mini`
    -   **Note:** The specific model used for each agent may be configured based on task complexity and cost considerations. For MVP, simpler/faster models like `gpt-4.1-mini` or `o4-mini` will be prioritized for most generation tasks to manage cost and speed, with more powerful models reserved if initial quality is insufficient.
    -   **Rationale:** Specified by the user; state-of-the-art capabilities for creative generation and instruction following.

## 4. Data Structuring & Validation

-   **Library:** Pydantic
    -   **Version:** Compatible version automatically installed as a dependency of `openai-agents`, or latest stable if managed separately.
    -   **Rationale:** Used by the OpenAI Agents SDK for defining `output_type` for structured LLM responses. Excellent for data validation, serialization, and defining clear data schemas within Python. Adherence to OpenAI's supported types for structured outputs is mandatory.

## 5. Development Environment & Tooling

-   **Virtual Environment:** Python `venv`
    -   **Rationale:** Standard Python practice; specified by user.
-   **Dependency Management:** `pip` and `requirements.txt`
    -   **Rationale:** Standard Python practice.
-   **API Key Management:** `python-dotenv`
    -   **Version:** Latest stable.
    -   **Rationale:** Securely loads environment variables (like `OPENAI_API_KEY`) from a `.env` file.
-   **Command-Line Interface Parsing:** `argparse` (Python built-in)
    -   **Rationale:** Standard library for creating CLI interfaces for the main execution script.
-   **Code Formatting:** Black
    -   **Version:** As present in user's environment (e.g., `black==25.1.0` or latest stable).
    -   **Rationale:** Opinionated code formatter for consistent style.
-   **Linting:** Ruff (or other, e.g., Flake8, Pylint, if preferred by development team later)
    -   **Version:** As present in user's environment (e.g., `ruff==0.11.9` or latest stable).
    -   **Rationale:** Fast and comprehensive linter.

## 6. Version Control

-   **System:** Git
-   **Hosting:** Not specified (assumed local or user's preferred remote like GitHub, GitLab).

## 7. Operating System (for Development & Execution)

-   **Primary:** Windows 11 Pro (as per user's environment).
-   **Consideration:** The Python application should be cross-platform compatible (Windows, macOS, Linux) as much as standard Python and the OpenAI Agents SDK allow. No OS-specific libraries or calls are planned.

## 8. Excluded Technologies (for MVP)

-   Databases (SQL or NoSQL)
-   Web Frameworks (FastAPI, Django, Flask, Streamlit, React, etc.)
-   Dedicated Web Servers (Nginx, Apache)
-   Containerization (Docker, Kubernetes)
-   Cloud Hosting Services (AWS, GCP, Azure)
-   Task Queues (Celery, RabbitMQ)
-   Complex CI/CD Systems

This stack is intentionally lean to focus on the core AI generation capabilities for the MVP. 