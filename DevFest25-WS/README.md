# DevFest 2025 Workshop - Agentic AI with Google ADK

This workshop teaches you how to build AI agents using Google's Agent Development Kit (ADK).

## Quick Setup

All workshop parts share the same API configuration:

```bash
# Copy the example file and add your API key
cp env.example .env
# Edit .env and replace 'your-api-key-here' with your actual Google API Key
```

Get your API key here: https://codelabs.developers.google.com/onramp/instructions#1

## Workshop Parts

- **P1-ToolCalling**: Your First Agent - The Day Trip Genie 🧞
  - Learn agent basics
  - Use built-in tools (Google Search)
  - Create budget-aware itineraries

- **P2-CustomTools**: Supercharging Agents with Custom Tools 🛠️
  - Create custom function tools
  - Integrate external APIs (Weather Service)
  - Use real-time data in recommendations

- **P3-Memory**: Agent with Memory - The Adaptive Planner 🗺️
  - Understand sessions and conversational memory
  - Build multi-day itineraries progressively
  - Adapt to user feedback across conversation turns

## Structure

```
DevFest25-WS/
├── .env                    # Shared API keys (create from env.example)
├── env.example             # Template for environment variables
├── P1-ToolCalling/         # Part 1: Basic agent with tools
├── P2-CustomTools/         # Part 2: Custom tools with external APIs
├── P3-Memory/              # Part 3: Sessions and memory
└── source/                 # Original workshop notebooks
```

