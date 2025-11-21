from google.adk.agents.llm_agent import Agent


# Mock tool implementation
def respondHow() -> dict:
    """Returns the response when a user says HEY!"""
    return {"status": "success", "answer": "HOW!"}


root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="Everytime someone says to you HEY!, you respond HOW!",
    instruction="Everytime someone says to you HEY!, you respond HOW!. Use the 'respondHow' tool for this purpose.",
    tools=[respondHow],
)
