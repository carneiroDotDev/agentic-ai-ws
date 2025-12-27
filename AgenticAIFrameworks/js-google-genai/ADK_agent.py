from google.adk.agents.llm_agent import Agent

def respondWhereAmI() -> dict:
    """Returns the response when a user says Where am I?"""
    return {"status": "success", "answer": "DevFest Armenia"}


root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="Everytime someone says to you Where am I?, you respond DevFest Armenia!",
    instruction="Everytime someone says to you Where am I?, you respond DevFest Armenia!. Use the 'respondWhereAmI' tool for this purpose.",
    tools=[respondWhereAmI],
)
