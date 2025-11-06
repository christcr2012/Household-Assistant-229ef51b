# Robinson Household Assistant

This project implements a modular backend for the personal assistant outlined in `READ_ME.txt`. The system provides
multi-tenant user onboarding with Google or Apple accounts, tools for calendar/email/inventory management, and an AI
assistant orchestration layer.

## Features

- **OAuth-style onboarding** – `/auth/google` and `/auth/apple` endpoints persist user profiles and provider tokens per tenant.
- **Multi-tenant isolation** – every record is scoped by user/tenant identifiers to prevent cross-account access.
- **Household tools** – calendar, email, and inventory APIs expose the core functionality expected from the assistant.
- **Assistant orchestration** – `/assistant/query` maintains conversation state and optionally integrates with OpenAI if an
  API key is provided. A rule-based fallback keeps the assistant responsive without external dependencies.
- **Provider abstractions** – thin integration layers represent Google Workspace and Apple ecosystem behaviours, allowing the
  application code to remain provider-agnostic.

## Getting Started

### Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Configuration

Set environment variables (optional). All configuration values are prefixed with `ASSISTANT_`.

- `ASSISTANT_DATABASE_URL` – database connection string (defaults to `sqlite:///./assistant.db`).
- `ASSISTANT_OPENAI_API_KEY` – supply an OpenAI API key to enable LLM responses.

### Running the API

```bash
uvicorn app.main:app --reload
```

The interactive documentation will be available at `http://localhost:8000/docs`.

### Example Workflow

1. **Authenticate** – send a POST request to `/auth/google` or `/auth/apple` with tokens from the respective ecosystem.
2. **Use tools** – with the returned `user_id`, pass the `X-User-Id` header to interact with calendar, email, or inventory endpoints.
3. **Chat with the assistant** – call `/assistant/query` to maintain conversation context and receive tool guidance.

### Testing

```bash
pytest
```

## Project Structure

- `app/core` – configuration and shared settings.
- `app/db` – database engine setup and base declarative class.
- `app/models` – SQLAlchemy ORM models for multi-tenant data.
- `app/services` – business logic for authentication, integrations, and assistant orchestration.
- `app/api` – FastAPI routers exposing public endpoints.
- `tests` – integration-style tests covering onboarding and key assistant flows.
