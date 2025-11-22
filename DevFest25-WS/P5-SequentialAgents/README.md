# Part 5: Sequential Workflows - Chaining Agents Together 🔗

Learn how to chain multiple agents in sequence using `SequentialAgent`. Perfect for multi-step tasks where the output of one agent becomes the input for the next.

## Prerequisites

- Python 3.13+
- Google API Key ([Get one here](https://codelabs.developers.google.com/onramp/instructions#1))

## Setup

Use the shared `.env` file from parent directory, or:

```bash
export GOOGLE_API_KEY='your-api-key-here'
```

## Run Locally

```bash
uv venv && source .venv/bin/activate && uv sync
adk web --port 8000  # Web UI at http://localhost:8000
# OR
adk run agent        # CLI mode
```

## Run with Docker

```bash
docker build -t sequential-agents .

# Option 1: Inline API key
docker run -p 8000:8000 -e GOOGLE_API_KEY='your-api-key-here' sequential-agents

# Option 2: Variable (simpler)
GOOGLE_API_KEY='your-api-key-here'
docker run -p 8000:8000 -e GOOGLE_API_KEY=$GOOGLE_API_KEY sequential-agents
```

## The Sequential Flow

```
User: "Find best restaurant in Munich and tell me how to get there from train station"

Step 1: Foodie Agent
   ↓ Finds: "Hofbräuhaus München"
   ↓ Saves to: state['destination']

Step 2: Transportation Agent
   ↓ Reads: state['destination']
   ↓ Provides: Directions from train station

Result: Restaurant recommendation + Directions
```

## Key Concepts

**SequentialAgent** = Runs agents in a predefined order  
**Shared State** = Agents pass data via `state` dictionary  
**output_key** = Agent saves result to state (e.g., `state['destination']`)  
**{placeholder}** = Agent reads from state (e.g., `{destination}`)

## Try It Out

```
Find me the best Bavarian restaurant in Munich and tell me how to get there from Hauptbahnhof
```

```
I want to eat at the top-rated restaurant in Rio de Janeiro. How do I get there from Copacabana?
```

```
Recommend a great restaurant near Marienplatz and give me walking directions from the square
```

## How It Works

1. **Foodie Agent** searches for the best restaurant
2. Agent saves restaurant name to `state['destination']`
3. **Transportation Agent** automatically reads `state['destination']`
4. Provides directions from starting point to destination

No manual data extraction needed - ADK handles the plumbing!

## Why SequentialAgent?

**Instead of:**
- Manual Python code to extract data
- Building new queries between agents
- Complex orchestration logic

**You get:**
- Automatic data passing via shared state
- Clean, declarative workflow definition
- Easy to read and maintain

