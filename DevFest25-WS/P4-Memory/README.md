# Part 4: Agent with Memory - The Adaptive Planner 🗺️

An AI agent that demonstrates sessions and conversational memory. This planner builds multi-day travel itineraries progressively and adapts to your feedback across conversation turns.

## 🔄 Difference from Original Notebook

**Original Notebook Approach:**
- Had explicit code to create and manage sessions
- Demonstrated memory BY breaking it (creating separate sessions)
- Showed side-by-side comparison: WITH memory vs WITHOUT memory

**This Simplified Version:**
- ADK UI automatically manages sessions for you
- Each chat window = one session with memory
- Focus on experiencing memory in action, not the code behind it
- **To test "without memory"**: You'd need to manually open a new chat window (new session)

The concepts are the same, but here we let the UI handle session management!

## Prerequisites

- Python 3.13+
- Google API Key ([Get one here](https://codelabs.developers.google.com/onramp/instructions#1))

## Setup

Use the shared `.env` file from the parent directory, or export the API key:

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
docker build -t memory-agent .

# Option 1: Inline API key
docker run -p 8000:8000 -e GOOGLE_API_KEY='your-api-key-here' memory-agent

# Option 2: Variable (simpler)
GOOGLE_API_KEY='your-api-key-here'
docker run -p 8000:8000 -e GOOGLE_API_KEY=$GOOGLE_API_KEY memory-agent
```

**💡 Critical**: Keep the conversation in the SAME chat window to maintain memory!

## Key Concepts

**Sessions** = Conversation threads. Same session = shared memory.  
**Memory** = Agent remembers destination, preferences, previous days, feedback.  
**Progressive Planning** = One day at a time, with confirmation and adaptation.

## Try It Out

**Test Memory & Adaptation** (in same chat session):

```
Turn 1: "Plan a 3-day trip to Munich with beer gardens and historic sites"
        → Agent provides Day 1

Turn 2: "I don't like museums, change the afternoon activity"
        → Agent remembers Day 1 and adapts only that part

Turn 3: "Perfect! Now plan Day 2 keeping the food theme"
        → Agent builds Day 2 based on Day 1 context
```

**Other scenarios:**
- `Plan a 2-day Bavaria trip with outdoor activities`
- `Create a Rio de Janeiro itinerary focusing on beaches`

## Testing WITHOUT Memory

Want to see what happens without memory? Open a **new chat window** (new session) and try asking for "Day 2" - the agent won't know what trip you're talking about!

This shows why sessions matter for complex, multi-turn interactions.

## Building on Part 3

In [Part 3](../P3-AgentTeams/), you built multi-agent teams with delegation. Now you've added memory, enabling your agents to maintain context across multiple conversation turns.

## What You Learned

✅ Session management for memory  
✅ Multi-turn conversations  
✅ Context preservation across interactions  
✅ Progressive planning with feedback  

## Next Steps

Ready for advanced orchestration? In **[Part 5: Router Agent](../P5-RouterAgent/)**, you'll build an intelligent router that analyzes requests and delegates them to the right specialist agent automatically!

