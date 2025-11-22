FROM python:3.13-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml .
COPY requirements.txt .
COPY agent/ ./agent/

# Create virtual environment and install dependencies
RUN uv venv && \
    . .venv/bin/activate && \
    uv pip install -r requirements.txt

# Expose the ADK UI port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Note: The agent will look for .env file two folders up (../../../.env)
# When using Docker, prefer passing GOOGLE_API_KEY via -e flag:
# docker run -e GOOGLE_API_KEY='your-key' ...

# Run the ADK web interface
CMD [".venv/bin/adk", "web", "--port", "8000", "--host", "0.0.0.0"]

