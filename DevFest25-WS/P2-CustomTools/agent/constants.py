"""
Constants for the Weather-Aware Trip Planner Agent

This module contains location data and mock weather responses used by the agent.
"""

# Location coordinates lookup
# Note: NWS API only works for US locations. For international locations, we return mock data.
LOCATION_COORDINATES = {
    # Germany - Bavaria region (mock data for demo)
    "munich": {"lat": 48.1351, "lon": 11.5820, "mock": True},
    "bavaria": {"lat": 48.7904, "lon": 11.4979, "mock": True},
    "königsee": {"lat": 47.5947, "lon": 12.9755, "mock": True},
    "konigsee": {"lat": 47.5947, "lon": 12.9755, "mock": True},
    "neuschwanstein": {"lat": 47.5576, "lon": 10.7498, "mock": True},
    "berlin": {"lat": 52.5200, "lon": 13.4050, "mock": True},
    "nuremberg": {"lat": 49.4521, "lon": 11.0767, "mock": True},
    # Brazil (mock data for demo)
    "rio de janeiro": {"lat": -22.9068, "lon": -43.1729, "mock": True},
    "rio": {"lat": -22.9068, "lon": -43.1729, "mock": True},
    "copacabana": {"lat": -22.9711, "lon": -43.1822, "mock": True},
    "ipanema": {"lat": -22.9838, "lon": -43.2096, "mock": True},
    # US locations (work with real NWS API)
    "sunnyvale": {"coords": "37.3688,-122.0363", "mock": False},
    "san francisco": {"coords": "37.7749,-122.4194", "mock": False},
    "lake tahoe": {"coords": "39.0968,-120.0324", "mock": False},
}

# Mock weather responses for international locations
MOCK_WEATHER = {
    "munich": {
        "temp": 18,
        "unit": "C",
        "forecast": "Partly cloudy with a chance of afternoon showers. Perfect weather for exploring the city's beer gardens!"
    },
    "bavaria": {
        "temp": 16,
        "unit": "C",
        "forecast": "Clear skies and mild temperatures. Excellent conditions for mountain hiking in the Alps."
    },
    "königsee": {
        "temp": 14,
        "unit": "C",
        "forecast": "Cool and clear. Ideal for boat tours on the lake with stunning mountain views."
    },
    "konigsee": {
        "temp": 14,
        "unit": "C",
        "forecast": "Cool and clear. Ideal for boat tours on the lake with stunning mountain views."
    },
    "neuschwanstein": {
        "temp": 12,
        "unit": "C",
        "forecast": "Crisp mountain air with excellent visibility for castle tours."
    },
    "berlin": {
        "temp": 17,
        "unit": "C",
        "forecast": "Mild and breezy. Great weather for exploring museums and outdoor attractions."
    },
    "nuremberg": {
        "temp": 16,
        "unit": "C",
        "forecast": "Pleasant conditions for walking the historic old town."
    },
    "rio de janeiro": {
        "temp": 28,
        "unit": "C",
        "forecast": "Sunny and hot with occasional sea breeze. Perfect beach weather!"
    },
    "rio": {
        "temp": 28,
        "unit": "C",
        "forecast": "Sunny and hot with occasional sea breeze. Perfect beach weather!"
    },
    "copacabana": {
        "temp": 29,
        "unit": "C",
        "forecast": "Hot and sunny. Ideal for beach activities and swimming."
    },
    "ipanema": {
        "temp": 28,
        "unit": "C",
        "forecast": "Beautiful beach weather with light ocean breeze."
    },
}

