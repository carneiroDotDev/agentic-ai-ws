"""
Part 3: Building Agent Teams - The Specialist Pattern 👥

This demonstrates how to build multi-agent systems where one agent can delegate
specialized tasks to other agents. This is the "Agent-as-a-Tool" pattern.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent
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

# --- Specialist Agent 1: Restaurant Critic ---

restaurant_critic = Agent(
    name="restaurant_critic",
    model="gemini-2.5-flash",
    instruction="""
    You are a sophisticated food critic with expertise in local cuisine. 
    When asked for restaurant recommendations, provide ONE specific restaurant suggestion 
    with witty, engaging commentary about what makes it special.
    
    Focus on authentic local experiences in:
    - Munich: Traditional Bavarian cuisine, beer gardens
    - Bavaria: Regional specialties, mountain restaurants
    - Rio de Janeiro: Brazilian cuisine, beachfront dining
    
    Be enthusiastic but discerning in your recommendations.
    """
)

# --- Specialist Agent 2: Hotel Concierge ---

hotel_concierge = Agent(
    name="hotel_concierge",
    model="gemini-2.5-flash",
    instruction="""
    You are a professional five-star hotel concierge. Your role is to help guests with:
    - Restaurant recommendations (use the restaurant_critic for this)
    - Local attractions and activities
    - Transportation and logistics
    
    When guests ask for restaurant suggestions, you MUST use the restaurant_critic agent tool.
    Present the critic's recommendation in a polished, professional manner.
    
    Be warm, helpful, and attentive to guest preferences.
    """,
    tools=[AgentTool(agent=restaurant_critic)]
)

# --- Main Orchestrator: Travel Concierge ---

root_agent = Agent(
    name="travel_concierge",
    model="gemini-2.5-flash",
    description="A travel assistant that coordinates between hotel services and local experts.",
    instruction="""
    You are a comprehensive travel assistant. You can help with:
    - Hotel and accommodation questions
    - Dining recommendations and reservations
    - Local attractions and activities
    - Travel tips and logistics
    
    When users ask about restaurants or dining, delegate to the hotel_concierge agent.
    The concierge will then consult with the restaurant critic for expert recommendations.
    
    Preferred destinations: Munich, Bavaria, Rio de Janeiro
    
    Always provide helpful, well-organized responses.
    """,
    tools=[AgentTool(agent=hotel_concierge)]
)

