"""
Part 8: Parallel Power with ParallelAgent ⚡

This demonstrates how to run multiple agents simultaneously for maximum efficiency.
When a user needs multiple independent pieces of information, ParallelAgent executes
all specialists concurrently, then synthesizes their results into a unified response.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent, ParallelAgent, SequentialAgent
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

# --- Specialist Agent 1: Museum Finder ---

museum_finder_agent = Agent(
    name="museum_finder_agent",
    model="gemini-2.5-flash",
    tools=[google_search],
    instruction="""
    You are a museum expert. Find the best museum based on the user's query.
    
    Focus on locations in Munich, Bavaria, or Rio de Janeiro.
    
    Output ONLY the museum's name and a one-sentence description.
    Example: "Deutsches Museum - World's largest science and technology museum"
    """,
    output_key="museum_result"  # Saves to state['museum_result']
)

# --- Specialist Agent 2: Concert Finder ---

concert_finder_agent = Agent(
    name="concert_finder_agent",
    model="gemini-2.5-flash",
    tools=[google_search],
    instruction="""
    You are an events guide. Find a concert or live music event based on the user's query.
    
    Focus on locations in Munich, Bavaria, or Rio de Janeiro.
    
    Output ONLY the concert name, artist, and venue.
    Example: "Beethoven Concert - Munich Philharmonic at Gasteig"
    """,
    output_key="concert_result"  # Saves to state['concert_result']
)

# --- Specialist Agent 3: Restaurant Finder ---

restaurant_finder_agent = Agent(
    name="restaurant_finder_agent",
    model="gemini-2.5-flash",
    tools=[google_search],
    instruction="""
    You are an expert food critic. Find the best restaurant based on the user's request.
    
    Focus on locations in Munich, Bavaria, or Rio de Janeiro.
    
    Output ONLY the restaurant's name and cuisine type.
    Example: "Hofbräuhaus - Traditional Bavarian cuisine"
    """,
    output_key="restaurant_result"  # Saves to state['restaurant_result']
)

# --- Parallel Agent: Runs All Three Specialists Simultaneously ---

parallel_research_agent = ParallelAgent(
    name="parallel_research_agent",
    sub_agents=[museum_finder_agent, concert_finder_agent, restaurant_finder_agent],
    description="Runs multiple research agents in parallel for maximum efficiency"
)

# --- Synthesis Agent: Combines All Results ---

synthesis_agent = Agent(
    name="synthesis_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are a helpful assistant. Combine the following research results into a clear, well-formatted response for the user.
    
    Results:
    - Museum: {museum_result}
    - Concert: {concert_result}
    - Restaurant: {restaurant_result}
    
    Present these as a bulleted list with brief context for each recommendation.
    Make it engaging and helpful!
    """,
    tools=[]
)

# --- Sequential Agent: Chains Parallel Research → Synthesis ---

parallel_planner_agent = SequentialAgent(
    name="parallel_planner_agent",
    sub_agents=[parallel_research_agent, synthesis_agent],
    description="A workflow that finds multiple things in parallel and then summarizes the results."
)

# --- Root Agent (Main Entry Point) ---

root_agent = parallel_planner_agent

