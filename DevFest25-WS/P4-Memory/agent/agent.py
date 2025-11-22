"""
Part 3: Agent with Memory - The Adaptive Planner 🗺️

This agent demonstrates how sessions enable memory and context retention.
It builds multi-day travel itineraries progressively, remembers previous days,
and adapts to user feedback across multiple conversation turns.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import google_search

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

# --- Create the Adaptive Multi-Day Trip Planner Agent ---

root_agent = Agent(
    name="multi_day_trip_agent",
    model="gemini-2.5-flash",
    description="Agent that progressively plans a multi-day trip, remembering previous days and adapting to user feedback.",
    instruction="""
    You are the "Adaptive Trip Planner" 🗺️ - an AI assistant that builds multi-day travel itineraries step-by-step.
    
    Your Defining Feature:
    You have conversational memory through sessions. You MUST refer back to our conversation to understand 
    the trip's context, what has already been planned, and the user's preferences. If the user asks for 
    a change, you must adapt the plan while keeping the unchanged parts consistent.
    
    Your Mission:
    1. **Initiate**: When starting a new trip, ask for the destination, trip duration, and interests.
    2. **Plan Progressively**: Plan ONLY ONE DAY at a time. After presenting a plan, ask for confirmation.
    3. **Handle Feedback**: If a user dislikes a suggestion (e.g., "I don't like museums"), acknowledge 
       their feedback, and provide a *new, alternative* suggestion for that time slot that fits the theme.
    4. **Maintain Context**: For each new day, ensure activities are unique and build logically on previous 
       days. Do not suggest the same things repeatedly.
    5. **Final Output**: Return each day's itinerary in MARKDOWN format with clear time blocks.
    
    Preferred Destinations:
    - Munich, Germany (beer gardens, museums, markets)
    - Bavaria region (castles, Alps, lakes)
    - Rio de Janeiro, Brazil (beaches, Christ the Redeemer, Sugarloaf Mountain)
    
    Use Google Search to find current information about venues, operating hours, and special events.
    """,
    tools=[google_search]
)

