# Part 5: Router Agent - Intelligent Request Delegation 🧠

Learn how to build a router agent that analyzes user requests and intelligently delegates them to specialist agents. This is the foundation for complex multi-agent systems.

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
docker build -t router-agent .

# Option 1: Inline API key
docker run -p 8000:8000 -e GOOGLE_API_KEY='your-api-key-here' router-agent

# Option 2: Variable (simpler)
GOOGLE_API_KEY='your-api-key-here'
docker run -p 8000:8000 -e GOOGLE_API_KEY=$GOOGLE_API_KEY router-agent
```

## The Router Pattern

```
                    User Query
                        ↓
                 ┌──────────────┐
                 │ Router Agent │ 🧠
                 │ (Analyzes &  │
                 │  Delegates)  │
                 └──────┬───────┘
                        │
        ┌───────────────┼───────────────┬──────────────┐
        ↓               ↓               ↓              ↓
  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
  │Day Trip  │   │ Foodie   │   │ Weekend  │   │Transport │
  │ Agent 🚗 │   │Agent 🍽️  │   │Guide 🎉  │   │Agent 🚇  │
  └────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘
       │              │              │              │
       └──────────────┴──────────────┴──────────────┘
                        ↓
                 Final Response
                 (from selected specialist)
```

## How It Works

1. **Router Agent** receives user query
2. **Analyzes** the request to determine intent
3. **Selects** the most appropriate specialist agent:
   - `day_trip_agent`: Full-day itinerary planning
   - `foodie_agent`: Restaurant and food recommendations
   - `weekend_guide_agent`: Events, concerts, festivals
   - `transportation_agent`: Directions and navigation
4. **Invokes** the selected specialist using delegation tools
5. **Returns** the specialist's response to the user

The router uses **delegation tools** (`call_day_trip_agent`, `call_foodie_agent`, etc.) to actually execute the specialist agents and get real answers!

## Example Prompts

**Day Trip Planning:**
```
I want a spontaneous, adventurous day trip in Munich with a moderate budget
```

**Food Recommendations:**
```
Find me the best traditional Bavarian restaurant in Munich
```

**Events:**
```
What concerts or festivals are happening in Munich this weekend?
```

**Navigation:**
```
How do I get from Munich Central Station to Marienplatz?
```

**Mixed Query (Router decides):**
```
I'm visiting Rio de Janeiro tomorrow. What should I do?
```

## What You'll See

When you run a query:
1. **Router** analyzes your request
2. **AgentTool Invocation** - Router calls the appropriate specialist (e.g., `foodie_agent` via `foodie_tool`)
3. **Specialist Execution** - The selected agent executes with your query using its tools
4. **Final Response** - You get the complete answer from the specialist

In the ADK UI trace, you'll see the full delegation chain and all tool calls!

## Key Concepts

**Router Pattern** = Central agent that classifies and delegates requests  
**Specialist Agents** = Focused agents optimized for specific tasks  
**Delegation** = Router analyzes intent and hands off to the right expert  
**Scalability** = Easy to add new specialists without changing router logic

## Why Use a Router?

**Without Router:**
- User must know which agent to use
- Complex queries require manual orchestration
- Hard to scale to many specialized agents

**With Router:**
- ✅ Single entry point for all requests
- ✅ Automatic classification and delegation
- ✅ Easy to add new specialist agents
- ✅ Foundation for complex multi-agent workflows

## Building on Part 4

In [Part 4](../P4-Memory/), you added memory to agents. Now you're building an intelligent router that can analyze any request and automatically delegate it to the right specialist - a key pattern for scalable multi-agent systems!

## Architecture Insights

**Implementation Pattern:**
- Router analyzes query intent
- Uses **AgentTool** to wrap specialist agents as callable tools
- Router invokes specialist via tool calls
- Returns actual results from specialist agents

**Key Technique:**
- `AgentTool(agent=specialist_agent)` wraps agents as tools
- Router has these AgentTools in its `tools` list
- Same pattern as P3-AgentTeams (agent-as-a-tool)
- Foundation for more complex orchestration (P6, P7)

**Why This Matters:**
- Demonstrates the fundamental routing pattern
- Shows how agents can delegate to other agents
- Foundation for SequentialAgent workflows (P6)
- Enables complex multi-agent systems

## What You Learned

✅ Router pattern for intelligent delegation  
✅ Request classification and routing  
✅ Using AgentTool to wrap specialists  
✅ Building scalable multi-agent architectures  

## Next Steps

Ready for multi-step workflows? In **[Part 6: Sequential Agents](../P6-SequentialAgents/)**, you'll learn to chain agents together where each step's output becomes the next step's input!

