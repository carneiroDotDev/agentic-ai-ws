"""
Part 5: Router Agent - Intelligent Request Delegation 🧠

This demonstrates a router pattern where a master agent analyzes requests
and delegates them to specialist agents. Foundation for complex multi-agent systems.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool

# Load environment variables from shared .env file (two folders up)
env_path = Path(__file__).parent.parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ Loaded environment variables from {env_path}")
else:
    print(f"ℹ️  No .env file found at {env_path}, using system environment variables")

# Verify API key is set
if not os.getenv('GOOGLE_API_KEY'):
    print("⚠️  WARNING: GOOGLE_API_KEY not found. Please set it via .env file or export command.")

# --- Specialist Agent 1: Day Trip Planner ---

day_trip_agent = Agent(
    name="day_trip_agent",
    model="gemini-2.5-flash",
    description="Agent specialized in generating spontaneous full-day itineraries based on mood, interests, and budget.",
    instruction="""
    You are the "Spontaneous Day Trip" Generator 🚗 - a specialized AI assistant that creates engaging full-day itineraries.
    
    Your Mission:
    Transform a simple mood or interest into a complete day-trip adventure with real-time details, while respecting a budget.
    
    Guidelines:
    1. **Budget-Aware**: Pay close attention to budget hints like 'cheap', 'affordable', or 'splurge'. Use Google Search to find activities (free museums, parks, paid attractions) that match the user's budget.
    2. **Full-Day Structure**: Create morning, afternoon, and evening activities.
    3. **Real-Time Focus**: Search for current operating hours and special events.
    4. **Mood Matching**: Align suggestions with the requested mood (adventurous, relaxing, artsy, etc.).
    
    Focus on locations in Munich, Bavaria, or Rio de Janeiro.
    
    RETURN itinerary in MARKDOWN FORMAT with clear time blocks and specific venue names.
    """,
    tools=[google_search]
)

# --- Specialist Agent 2: Food Expert ---

foodie_agent = Agent(
    name="foodie_agent",
    model="gemini-2.5-flash",
    description="Expert food critic specialized in finding the best restaurants and culinary experiences.",
    instruction="""
    You are an expert food critic. Your goal is to find the absolute best food, restaurants, or culinary experiences based on a user's request.
    
    Focus on locations in Munich, Bavaria, or Rio de Janeiro.
    
    When you recommend a place, provide:
    - Restaurant name
    - Type of cuisine
    - Why it's special
    - Approximate price range
    
    Use Google Search to find current information and reviews.
    """,
    tools=[google_search]
)

# --- Specialist Agent 3: Events Guide ---

weekend_guide_agent = Agent(
    name="weekend_guide_agent",
    model="gemini-2.5-flash",
    description="Local events guide specialized in finding concerts, festivals, and weekend activities.",
    instruction="""
    You are a local events guide. Your task is to find interesting events, concerts, festivals, and activities happening on a specific weekend or timeframe.
    
    Focus on locations in Munich, Bavaria, or Rio de Janeiro.
    
    Provide:
    - Event name and type
    - Date and time
    - Location
    - Ticket information (if applicable)
    
    Use Google Search to find current and upcoming events.
    """,
    tools=[google_search]
)

# --- Specialist Agent 4: Navigation Assistant ---

transportation_agent = Agent(
    name="transportation_agent",
    model="gemini-2.5-flash",
    description="Navigation assistant providing directions and transportation options.",
    instruction="""
    You are a navigation assistant. Given a starting point and a destination, provide clear directions on how to get from start to end.
    
    Focus on locations in Munich, Bavaria, or Rio de Janeiro.
    
    Include:
    - Best transportation method (walk, metro, bus, car)
    - Estimated travel time
    - Step-by-step directions
    - Any helpful tips
    
    Use Google Search to find current route information.
    """,
    tools=[google_search]
)

# --- Delegation Tools: Wrap Specialists as Callable Tools ---

# AgentTool wraps an agent so it can be called as a tool by another agent
# The router will see these as tools it can invoke to delegate work

day_trip_tool = AgentTool(agent=day_trip_agent)
foodie_tool = AgentTool(agent=foodie_agent)
weekend_guide_tool = AgentTool(agent=weekend_guide_agent)
transportation_tool = AgentTool(agent=transportation_agent)

# --- Router Agent: The Brain of the Operation ---

router_agent = Agent(
    name="router_agent",
    model="gemini-2.5-flash",
    description="Master router that analyzes requests and delegates to specialist agents.",
    instruction="""
    You are a request router and intelligent delegator. Your job is to:
    
    1. **Analyze** the user's query carefully
    2. **Determine** which specialist agent is best suited to handle it
    3. **Use the appropriate delegation tool** to invoke that specialist
    4. **Return** the specialist's response to the user
    
    Available Specialist Agents (via AgentTools):
    - **day_trip_agent**: For full-day itinerary planning, spontaneous trips, mood-based suggestions
    - **foodie_agent**: For restaurant recommendations, food experiences, dining suggestions
    - **weekend_guide_agent**: For events, concerts, festivals, weekend activities
    - **transportation_agent**: For directions, navigation, getting from A to B
    
    IMPORTANT: You MUST use one of the agent tools to get the answer. Do not try to answer directly.
    After receiving the specialist's response, present it to the user.
    """,
    tools=[day_trip_tool, foodie_tool, weekend_guide_tool, transportation_tool]
)

# --- Root Agent (Main Entry Point) ---
# The router agent is the main interface

root_agent = router_agent

