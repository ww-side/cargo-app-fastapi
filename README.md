# Cargo App

## Tech Stack

- **FastAPI** – Python web framework for building APIs.
- **SQLAlchemy** – ORM for database interactions.
- **Alembic** – For database migrations.
- **PostgreSQL** – Main relational database.
- **Pydantic** – Data validation and settings management.
- **Uvicorn** – ASGI server for running the FastAPI app.
- **Docker & Docker Compose** – Containerization and orchestration.
- **uv** – Advanced Python package and environment management.
- **Ruff** – Python linter for enforcing code style and catching common issues.

## Main Entities

- **Vessel**: Represents ships that carry cargo on defined routes.
- **Port**: Locations (e.g., cities, harbors) where vessels can depart or arrive.
- **Route**: A predefined series of legs connecting ports in order.
- **Leg**: A segment of a route, defined by an origin port and a destination port, optionally with an assigned vessel.
- **Booking**: A reservation of vessel capacity for a given time window at a port.
- **Shipment**: Represents the movement of cargo, linked to a specific booking.
- **Shipment Audit**: Logs status changes for each shipment for auditing purposes.

## Linting

- **Ruff** is used for linting and maintaining code quality.
- To run Ruff linting manually:
  ```
  uv run ruff check
  ```
- To automatically fix issues:
  ```
  uv run ruff check --fix
  ```
- See `.ruff.toml` for project-specific configuration.

## Quick Start

1. Run `uv sync` to install all dependencies and sync your Python environment.
2. Use the following commands to run the app:
   - `uv run dev` – Start in development mode (hot reload).
   - `uv run prod` – Run in production mode.
   - `uv run docker-build` – Build the Docker image.
   - `uv run docker-up` – Launch via Docker Compose.
