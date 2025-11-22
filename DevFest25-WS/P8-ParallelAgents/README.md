# Part 8: Parallel Power with ParallelAgent ⚡

Learn how to run multiple agents simultaneously for maximum efficiency. When users need multiple independent pieces of information, `ParallelAgent` executes all specialists concurrently, then synthesizes their results.

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
docker build -t parallel-agents .

# Option 1: Inline API key
docker run -p 8000:8000 -e GOOGLE_API_KEY='your-api-key-here' parallel-agents

# Option 2: Variable (simpler)
GOOGLE_API_KEY='your-api-key-here'
docker run -p 8000:8000 -e GOOGLE_API_KEY=$GOOGLE_API_KEY parallel-agents
```

## The Parallel Pattern

```
                User Query:
     "Find me a museum, concert, and restaurant in Munich"
                        ↓
            ┌───────────────────────┐
            │ SequentialAgent       │
            │ (Orchestrator)        │
            └───────────┬───────────┘
                        │
                        ↓
            ┌───────────────────────┐
            │ ParallelAgent ⚡       │
            │ (Runs Simultaneously) │
            └───────┬───────────────┘
                    │
        ┌───────────┼───────────┐
        ↓           ↓           ↓
   ┌────────┐  ┌────────┐  ┌────────┐
   │Museum  │  │Concert │  │Restaurant│
   │Finder🖼️ │  │Finder🎵│  │Finder🍽️  │
   └───┬────┘  └───┬────┘  └───┬────┘
       │           │           │
       └───────────┴───────────┘
                   ↓
       (All results saved to shared state)
                   ↓
            ┌─────────────┐
            │  Synthesis  │
            │  Agent 📋   │
            └──────┬──────┘
                   ↓
          Combined, formatted
          final response
```

## How It Works

1. **User Query**: "Find me a museum, concert, and restaurant in Munich"

2. **ParallelAgent** launches 3 specialists simultaneously:
   - `museum_finder_agent` → searches for museums
   - `concert_finder_agent` → searches for concerts
   - `restaurant_finder_agent` → searches for restaurants

3. **Shared State**: Each agent saves its result:
   - `state['museum_result']` = "Deutsches Museum - ..."
   - `state['concert_result']` = "Bach Concert at ..."
   - `state['restaurant_result']` = "Hofbräuhaus - ..."

4. **Synthesis Agent**: Reads all results from state and creates a unified, well-formatted response

5. **Final Output**: User gets all three recommendations in one clean response

## Example Prompts

**Basic Parallel Request:**
```
Help me plan a trip to Munich. I need a museum, a concert, and a restaurant.
```

**Rio de Janeiro:**
```
Find me a museum to visit, a concert to attend, and a place to eat in Rio de Janeiro.
```

**Bavaria:**
```
I'm visiting Bavaria. Suggest one museum, one live music event, and one restaurant.
```

## Key Concepts

**ParallelAgent** = Runs multiple sub-agents concurrently  
**Shared State** = All agents read/write to same state dictionary  
**output_key** = Where each agent saves its result (e.g., `output_key="museum_result"`)  
**SequentialAgent** = Chains parallel execution → synthesis  
**Efficiency** = 3 tasks complete in parallel, not sequentially!

## Why Use ParallelAgent?

**Without Parallel:**
```
Museum search:   [====]     (5 seconds)
Concert search:        [====]  (5 seconds)
Restaurant:                [====] (5 seconds)
Total: 15 seconds ⏰
```

**With ParallelAgent:**
```
Museum search:   [====]
Concert search:  [====]  (All run simultaneously)
Restaurant:      [====]
Total: ~5 seconds ⚡
```

**Benefits:**
- ✅ 3x faster (or more with more agents)
- ✅ Better user experience
- ✅ Efficient use of API calls
- ✅ Scales to many parallel tasks

## Architecture Insights

**Component Breakdown:**

1. **Specialist Agents** (3):
   - Each has `google_search` tool
   - Each has `output_key` to save results
   - Run independently in parallel

2. **ParallelAgent**:
   - Takes list of `sub_agents`
   - Executes them concurrently
   - No sequential dependencies

3. **Synthesis Agent**:
   - Reads from `{museum_result}`, `{concert_result}`, `{restaurant_result}`
   - Combines into unified response
   - Runs after parallel execution completes

4. **SequentialAgent** (Orchestrator):
   - Step 1: Run ParallelAgent
   - Step 2: Run Synthesis Agent
   - Ensures proper ordering

## When to Use ParallelAgent

**Perfect For:**
- Multiple independent research tasks
- Gathering diverse information simultaneously
- Time-sensitive applications
- High-throughput systems

**Not Ideal For:**
- Sequential workflows (use SequentialAgent - P6)
- Tasks with dependencies between agents
- Single-task queries

## Performance Characteristics

- **Speed**: O(max) instead of O(sum)
  - Sequential: 3 × 5s = 15s
  - Parallel: max(5s, 5s, 5s) = 5s

- **API Efficiency**: Same number of API calls, faster results

- **Scalability**: Add more specialists without increasing total time (up to concurrency limits)

## Building on Part 7

In [Part 7](../P7-LoopAgents/), you built iterative workflows with refinement loops. Now you're using `ParallelAgent` to run multiple agents simultaneously - maximizing speed when tasks are independent!

## What You Learned

✅ ParallelAgent for concurrent execution  
✅ Maximizing efficiency with parallelism  
✅ Synthesizing results from multiple agents  
✅ Performance optimization patterns  

## Next Steps: Deploy to Production!

You've mastered all core ADK patterns! Ready to deploy your agents to the cloud? Head to **[Part 9: Deployment](../P9-Deployment/)** to learn how to deploy your agents to Google Cloud Run for production-ready, scalable AI applications!

