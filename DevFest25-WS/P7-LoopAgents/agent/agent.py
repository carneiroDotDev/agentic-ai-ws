"""
Part 6: Iterative Refinement with LoopAgent 🔁

This demonstrates the LoopAgent pattern for iterative workflows where agents
critique and refine plans until meeting constraints. The loop runs up to 3 iterations,
automatically stopping when a good plan is found.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent, SequentialAgent, LoopAgent
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

# --- Step 1: Planner Agent ---
# Creates an initial plan with activity + restaurant

planner_agent = Agent(
    name="planner_agent",
    model="gemini-2.5-flash",
    tools=[google_search],
    instruction="""
    You are a trip planner. Based on the user's request, propose ONE activity and ONE restaurant.
    
    Focus on locations in:
    - Munich: Museums, beer gardens, historic sites
    - Bavaria: Castles, mountain activities
    - Rio de Janeiro: Beaches, attractions
    
    Output ONLY the names in this format:
    Activity: [Name], Restaurant: [Name]
    
    Example: Activity: Deutsches Museum, Restaurant: Augustiner Bräustuben
    """,
    output_key="current_plan"  # Saves to state['current_plan']
)

# --- Step 2: Critic Agent (runs in loop) ---
# Checks if travel time meets constraints

critic_agent = Agent(
    name="critic_agent",
    model="gemini-2.5-flash",
    tools=[google_search],
    instruction="""
    You are a logistics expert. Your job is to critique a travel plan based on travel time.
    
    Current Plan: {current_plan}
    
    TASK:
    1. Use Google Search to check travel time between the two locations
    2. Analyze if the travel time is reasonable (under 45 minutes is ideal)
    3. Provide your critique:
       - If TOO FAR: "Travel time is [X] minutes. Find a restaurant closer to the activity."
       - If GOOD: "Approved: Travel time is [X] minutes, which is acceptable."
    
    Be specific about the actual travel time you find!
    """,
    output_key="criticism"  # Saves to state['criticism']
)

# --- Step 3: Refiner Agent (runs in loop) ---
# Refines the plan based on criticism

refiner_agent = Agent(
    name="refiner_agent",
    model="gemini-2.5-flash",
    tools=[google_search],
    instruction="""
    You are a trip planner, refining a plan based on criticism.
    
    Original Request: {session.query}
    Current Plan: {current_plan}
    Critique: {criticism}
    
    DECISION:
    - IF critique says "Approved": Simply confirm the plan is good, no changes needed
    - ELSE: Generate a NEW plan addressing the critique
    
    For new plans, output ONLY names in this format:
    Activity: [Name], Restaurant: [Name]
    
    Keep the activity but find a restaurant closer to it!
    """,
    output_key="current_plan"  # Updates state['current_plan']
)

# --- Step 4: Loop Agent ---
# Manages the critique → refine cycle
# Runs up to 3 iterations, each iteration = critic checks, refiner improves

refinement_loop = LoopAgent(
    name="refinement_loop",
    sub_agents=[critic_agent, refiner_agent],
    max_iterations=3  # Up to 3 attempts to find a good plan
)

# --- Step 5: Sequential Agent ---
# Combines: Initial Plan → Iterative Refinement Loop
# 1. Planner creates first draft
# 2. Loop: Critic checks → Refiner improves (repeat up to 3x)

iterative_planner_agent = SequentialAgent(
    name="iterative_planner_agent",
    sub_agents=[planner_agent, refinement_loop],
    description="Creates an initial plan, then iteratively refines it through critic-refiner cycles until constraints are met."
)

# --- Root Agent (Main Entry Point) ---

root_agent = iterative_planner_agent

