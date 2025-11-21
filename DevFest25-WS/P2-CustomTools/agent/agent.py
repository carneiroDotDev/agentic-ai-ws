"""
Part 2: Supercharging Agents with Custom Tools 🛠️

This agent demonstrates how to create custom tools by connecting to external APIs.
It uses a real-time weather API to check conditions before making trip recommendations.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import requests
from google.adk.agents import Agent
from .constants import LOCATION_COORDINATES, MOCK_WEATHER

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

# --- Custom Tool: Weather API Integration ---

def get_live_weather_forecast(location: str) -> dict:
    """Gets the weather forecast for a specified location.
    
    This tool provides weather information for cities in Germany, Bavaria, Brazil, and the United States.
    Use this before making outdoor activity recommendations.
    
    Args:
        location: The city name, e.g., "Munich", "Rio de Janeiro", "Bavaria", or "San Francisco".
    
    Returns:
        A dictionary containing the temperature and a detailed forecast.
    """
    print(f"🛠️ TOOL CALLED: get_live_weather_forecast(location='{location}')")
    
    # Find the location in our database
    normalized_location = location.lower()
    location_data = None
    location_key = None
    
    for key, val in LOCATION_COORDINATES.items():
        if key in normalized_location:
            location_data = val
            location_key = key
            break
    
    if not location_data:
        return {"status": "error", "message": f"I don't have weather data for {location}. Try: Munich, Bavaria, Rio de Janeiro, or US cities."}
    
    # For international locations (mock data for demo purposes)
    if location_data["mock"] if "mock" in location_data else False:
        weather = MOCK_WEATHER[location_key] if location_key in MOCK_WEATHER else None
        if weather:
            return {
                "status": "success",
                "temperature": f"{weather['temp']}°{weather['unit']}",
                "forecast": weather['forecast'],
                "note": "Demo weather data for workshop"
            }
        return {"status": "error", "message": f"No weather data available for {location}"}
    
    # For US locations, use real NWS API
    try:
        coords_str = location_data["coords"]
        points_url = f"https://api.weather.gov/points/{coords_str}"
        headers = {"User-Agent": "ADK Workshop Agent"}
        points_response = requests.get(points_url, headers=headers)
        points_response.raise_for_status()
        forecast_url = points_response.json()['properties']['forecast']
        
        forecast_response = requests.get(forecast_url, headers=headers)
        forecast_response.raise_for_status()
        
        current_period = forecast_response.json()['properties']['periods'][0]
        return {
            "status": "success",
            "temperature": f"{current_period['temperature']}°{current_period['temperatureUnit']}",
            "forecast": current_period['detailedForecast']
        }
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"API request failed: {e}"}

# --- Create the Weather-Aware Trip Planner Agent ---

root_agent = Agent(
    name="weather_aware_planner",
    model="gemini-2.5-flash",
    description="A trip planner that checks the real-time weather before making suggestions.",
    instruction="""
    You are a cautious trip planner. Before suggesting any outdoor activities, you MUST use the 
    `get_live_weather_forecast` tool to check conditions. Incorporate the live weather details 
    into your recommendation.
    
    Always be specific about weather conditions and how they affect the activities you suggest.
    If the weather is bad, suggest indoor alternatives.
    """,
    tools=[get_live_weather_forecast]
)

