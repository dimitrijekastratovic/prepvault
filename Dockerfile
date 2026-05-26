# Production image for PrepVault FastAPI backend.
# Dependencies are managed by uv — see docs/adr/0002-dependency-management-with-uv.md.

FROM python:3.10-slim

# Install uv by copying its binary from the official distroless image.
# This avoids needing curl/pip on the runtime image and gives us a pinned uv version.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy only the files needed to resolve dependencies first, so the install layer
# is cached and only rebuilt when pyproject.toml or uv.lock changes.
COPY pyproject.toml uv.lock ./

# --frozen   : fail if uv.lock is out of sync with pyproject.toml (no implicit resolution in prod)
# --no-dev   : skip the [dependency-groups.dev] group (no pytest/ruff in the image)
# --no-install-project : we're not installing PrepVault itself as a package, only its deps
RUN uv sync --frozen --no-dev --no-install-project

# Copy the rest of the application code.
COPY . .

# Put the project venv first on PATH so `uvicorn` resolves to the locked version.
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
