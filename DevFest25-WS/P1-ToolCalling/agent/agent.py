"""
Part 1: Your First Agent - The Day Trip Genie 🧞

This agent generates spontaneous full-day itineraries based on mood, interests, and budget.
It uses Google Search to find real-time information about activities, venues, and operating hours.
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

# Create the Day Trip Genie Agent
root_agent = Agent(
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
    
    RETURN itinerary in MARKDOWN FORMAT with clear time blocks and specific venue names.
    """,
    tools=[google_search]
)
