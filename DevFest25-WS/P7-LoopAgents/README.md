# Part 6: Iterative Refinement with LoopAgent 🔁

Learn how to build agents that iteratively improve their work through cycles of planning, critique, and refinement using `LoopAgent`.

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
docker build -t loop-agents .

# Option 1: Inline API key
docker run -p 8000:8000 -e GOOGLE_API_KEY='your-api-key-here' loop-agents

# Option 2: Variable (simpler)
GOOGLE_API_KEY='your-api-key-here'
docker run -p 8000:8000 -e GOOGLE_API_KEY=$GOOGLE_API_KEY loop-agents
```

## The Iterative Flow

```
User: "Plan a day in Munich with museum and dinner, travel time under 45 min"

Step 1: Planner
   ↓ Proposes: "Activity: Deutsches Museum, Restaurant: Hofbräuhaus"
   ↓ Saves to: state['current_plan']

--- LOOP STARTS (max 3 iterations) ---

Iteration 1:
  Critic: Checks travel time → "Travel time is 35 minutes. Approved!"
  Refiner: Sees "Approved" → Confirms plan is good
  
--- LOOP ENDS (good plan found) ---

Result: Optimized plan meeting constraints


Alternative scenario (needs refinement):

Iteration 1:
  Critic: "Travel time is 60 minutes. Too far!"
  Refiner: "Activity: Deutsches Museum, Restaurant: Wirtshaus in der Au"
  
Iteration 2:
  Critic: "Travel time is 20 minutes. Approved!"
  Refiner: Confirms plan is good

--- LOOP ENDS ---
```

## Key Concepts

**LoopAgent** = Runs sub-agents repeatedly (up to max_iterations)  
**max_iterations** = Maximum refinement cycles (prevents infinite loops)  
**Shared State** = Plans and feedback passed via state dictionary  
**Iterative Refinement** = Critique → Improve → Repeat pattern

## Try It Out

```
Plan a day in Munich with a museum visit and dinner. Travel time between them must be under 45 minutes.
```

```
I want to visit an attraction and have lunch in Rio de Janeiro. Make sure they're close to each other.
```

```
Suggest an activity and restaurant in Bavaria. They should be within 30 minutes of each other.
```

Watch the agent iterate until finding a plan that meets your constraints!

## How It Works

1. **Planner** creates initial plan (activity + restaurant)
2. **Loop starts** (up to 3 iterations):
   - **Critic** checks travel time between locations
   - **Refiner** either confirms good plan OR creates improved plan
3. **Loop ends** when:
   - Critic approves the plan, OR
   - Maximum 3 iterations reached
4. **Result**: Best plan found within constraints

## Why LoopAgent?

**Perfect for:**
- Tasks requiring trial-and-error
- Plans with hard constraints
- Iterative improvement workflows
- Self-critique and refinement

**Instead of:**
- Single-shot planning (might fail constraints)
- Manual retry logic
- Complex conditional code

**You get:**
- Automatic iteration until success
- Built-in safety (max_iterations)
- Clean, declarative workflow

## Building on Part 6

In [Part 6](../P6-SequentialAgents/), you chained agents in a linear sequence. Now you're using `LoopAgent` to create iterative workflows where agents critique and refine their work until meeting constraints!

## What You Learned

✅ LoopAgent for iterative refinement  
✅ Plan-critique-refine cycles  
✅ Handling constraints through iteration  
✅ max_iterations safety mechanism  

## Next Steps

Ready for parallel execution? In **[Part 8: Parallel Agents](../P8-ParallelAgents/)**, you'll learn to run multiple agents simultaneously for maximum speed and efficiency!

