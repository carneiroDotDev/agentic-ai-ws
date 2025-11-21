# Part 2: Supercharging Agents with Custom Tools 🛠️

An AI agent that demonstrates how to create custom tools by integrating external APIs. This weather-aware trip planner checks real-time weather conditions before making outdoor activity recommendations.

## Prerequisites

- Python 3.13+
- Google API Key ([Get one here](https://codelabs.developers.google.com/onramp/instructions#1))

## Setup API Key

**Option 1: Shared .env file (Recommended for workshop)**

```bash
# From the DevFest25-WS directory
cd ..
cp env.example .env
# Edit .env and add your actual API key
```

**Option 2: Export command**

```bash
export GOOGLE_API_KEY='your-api-key-here'
```

## Run Locally

```bash
# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
uv sync
```

### Option A: Run with Web UI (Recommended)

```bash
# Start the ADK web interface
adk web --port 8000
```

The UI will be available at `http://localhost:8000`. Select the `agent` in the upper left corner to start chatting.

### Option B: Run with CLI

```bash
# Interactive command-line interface
adk run agent
```

Type your queries directly in the terminal. Type `exit` or press `Ctrl+C` to quit.

## Run with Docker

```bash
# Build the image
docker build -t weather-agent .

# Option 1: Run with inline API key
docker run -p 8000:8000 -e GOOGLE_API_KEY='your-api-key-here' weather-agent

# Option 2: Or define a variable first (simpler)
GOOGLE_API_KEY='your-api-key-here'
docker run -p 8000:8000 -e GOOGLE_API_KEY=$GOOGLE_API_KEY weather-agent
```

The UI will be available at `http://localhost:8000`

## What You'll Learn

This example demonstrates:
- **Custom Function Tools**: How to create Python functions that agents can call
- **API Integration**: Connecting to weather data sources (NWS API for US, mock data for international)
- **Real-Time Data**: Using weather data to inform agent recommendations

## Supported Locations

**Germany & Bavaria:**
- Munich, Bavaria region, Königsee, Neuschwanstein, Berlin, Nuremberg

**Brazil:**
- Rio de Janeiro, Copacabana, Ipanema

**United States:**
- San Francisco, Lake Tahoe, Sunnyvale

## Try It Out

Example prompts:
```
I want to go hiking near Königsee in Bavaria, what's the weather like?
```

```
Should I plan outdoor activities in Munich today?
```

```
What's the weather forecast for Munich? Recommend some outdoor activities!
```

```
I'm going to Rio de Janeiro - is it good beach weather today?
```

```
Check the weather in Neuschwanstein and suggest if it's a good day to visit the castle.
```

## How It Works

The agent has access to a custom `get_live_weather_forecast()` tool that:
1. Takes a city name as input (Munich, Rio de Janeiro, Bavaria, etc.)
2. Fetches weather data:
   - **US locations**: Real-time data from National Weather Service API
   - **International locations**: Mock data for workshop demonstration
3. Returns current temperature and detailed forecast
4. The agent uses this data to make informed recommendations

The key is the **docstring** - ADK uses it to teach the agent when and how to use the tool!

**Note**: For your own projects, you can integrate any weather API (OpenWeatherMap, WeatherAPI, etc.) by modifying the `get_live_weather_forecast()` function.

