# Part 1: Your First Agent - The Day Trip Genie 🧞

A simple AI agent that generates spontaneous full-day itineraries based on mood, interests, and budget using Google's ADK.

## Prerequisites

- Python 3.13+
- Google API Key ([Get one here](https://codelabs.developers.google.com/onramp/instructions#1))
# recommend to install uv for the following steps
- (Optional) Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh` (for Linux)

## Setup API Key

**Option 1: Shared .env file (Recommended for workshop)**

```bash
# From the DevFest25-WS directory
cd ..
cp env.example .env
# Edit .env and add your actual API key
```

**Option 2: Export command**

```bash
export GOOGLE_API_KEY='your-api-key-here'
```

## Run Locally

```bash
# Assume we are still at the `DevFest25-WS` directory
cd P1-ToolCalling

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
uv sync
```

### Option A: Run with Web UI (Recommended)

```bash
# Start the ADK web interface
adk web --port 8000
```

The UI will be available at `http://localhost:8000`. Select the `agent` in the upper left corner to start chatting.

### Option B: Run with CLI

```bash
# Interactive command-line interface
adk run agent
```

Type your queries directly in the terminal. Type `exit` or press `Ctrl+C` to quit.

## Run with Docker

```bash
# Build the image
docker build -t day-trip-agent .

# Option 1: Run with inline API key
docker run -p 8000:8000 -e GOOGLE_API_KEY='your-api-key-here' day-trip-agent

# Option 2: Or define a variable first (simpler)
GOOGLE_API_KEY='your-api-key-here'
docker run -p 8000:8000 -e GOOGLE_API_KEY=$GOOGLE_API_KEY day-trip-agent
```

The UI will be available at `http://localhost:8000`

## Try It Out

Example prompts:
```
Plan a relaxing and artsy day trip in Munich, Germany. Keep it affordable!
```

```
I want an adventurous day exploring Bavaria. What should I do?
```

```
Suggest a food-focused day trip in Rio de Janeiro with local cuisine!
```

## What You Learned

✅ Creating your first ADK agent  
✅ Using built-in tools (`google_search`)  
✅ Setting up environment variables  
✅ Running agents locally and with Docker  

## Next Steps

Ready for more? In **[Part 2: Custom Tools](../P2-CustomTools/)**, you'll learn to create your own tools and integrate external APIs like the National Weather Service!

