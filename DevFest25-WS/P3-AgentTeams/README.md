# Part 3: Building Agent Teams - The Specialist Pattern 👥

Build multi-agent systems where agents delegate specialized tasks to other agents using the "Agent-as-a-Tool" pattern.

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
docker build -t agent-teams .

# Option 1: Inline API key
docker run -p 8000:8000 -e GOOGLE_API_KEY='your-api-key-here' agent-teams

# Option 2: Variable (simpler)
GOOGLE_API_KEY='your-api-key-here'
docker run -p 8000:8000 -e GOOGLE_API_KEY=$GOOGLE_API_KEY agent-teams
```

## The Agent Hierarchy

```
Travel Concierge (root_agent)
    └── Hotel Concierge
            └── Restaurant Critic
```

**How it works:** User asks for restaurant → Travel Concierge → Hotel Concierge → Restaurant Critic → response flows back.

## Try It Out

```
Can you recommend a traditional Bavarian restaurant in Munich?
```

```
What's the best place for seafood in Rio de Janeiro?
```

```
Suggest a romantic restaurant in Bavaria with mountain views.
```

Watch the request flow through the agent team!

## Key Concepts

**Agent-as-a-Tool** = Agents using other agents as specialized tools  
**Delegation** = Orchestrator → Specialist pattern  
**Composition** = Build complex systems from focused components

Each agent has a clear role and can be developed independently.

## Building on Part 2

In [Part 2](../P2-CustomTools/), you created custom tools from Python functions. Now you're taking it further - using `AgentTool` to wrap entire agents as tools, enabling agent-to-agent delegation!

## What You Learned

✅ Agent-as-a-Tool pattern (`AgentTool`)  
✅ Building multi-agent hierarchies  
✅ Delegation and specialization  
✅ Coordinating multiple experts  

## Next Steps

Ready to add memory? In **[Part 4: Memory](../P4-Memory/)**, you'll learn how to build agents that remember conversation history and maintain context across multiple interactions!

