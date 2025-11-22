"""
Part 5: Sequential Workflows - Chaining Agents Together 🔗

This demonstrates the SequentialAgent pattern where multiple agents work in sequence,
passing information through a shared state. Perfect for multi-step tasks like
"find a restaurant THEN get directions to it."
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent, SequentialAgent
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

# --- Step 1: Food Finder Agent ---
# This agent finds a restaurant and saves the name to shared state

foodie_agent = Agent(
    name="foodie_agent",
    model="gemini-2.5-flash",
    tools=[google_search],
    instruction="""
    You are an expert food critic. Your goal is to find the best restaurant based on the user's request.
    
    When you recommend a place, output ONLY the name of the establishment.
    For example, if the best Bavarian restaurant is 'Hofbräuhaus München', output only: Hofbräuhaus München
    
    Focus on:
    - Munich: Traditional Bavarian cuisine, beer gardens
    - Bavaria: Regional specialties
    - Rio de Janeiro: Brazilian cuisine, beachfront dining
    """,
    output_key="destination"  # Saves result to state['destination']
)

# --- Step 2: Transportation Agent ---
# This agent reads the destination from state and provides directions

transportation_agent = Agent(
    name="transportation_agent",
    model="gemini-2.5-flash",
    tools=[google_search],
    instruction="""
    You are a navigation assistant. Provide clear directions to the destination.
    
    The destination is: {destination}
    
    Analyze the user's original query to find their starting point.
    Then provide clear, step-by-step directions from that starting point to {destination}.
    
    Include:
    - Best transportation method (walking, public transit, car)
    - Estimated travel time
    - Key landmarks or turns
    """
)

# --- Step 3: Sequential Workflow ---
# This SequentialAgent chains foodie_agent → transportation_agent

find_and_navigate_agent = SequentialAgent(
    name="find_and_navigate_agent",
    sub_agents=[foodie_agent, transportation_agent],
    description="A workflow that first finds a restaurant, then provides directions to it."
)

# --- Root Agent (Main Entry Point) ---
# This is what users interact with

root_agent = find_and_navigate_agent

