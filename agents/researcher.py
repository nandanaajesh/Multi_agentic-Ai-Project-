from phi.agent import Agent
from tools.search_tool import search_web

researcher = Agent(
    name="Research Agent",
    role="Searches the web and gathers information",
    tools=[search_web],
    instructions=[
        "Search for accurate information",
        "Provide factual data",
        "Include statistics if available"
    ],
    show_tool_calls=True,
    markdown=True,
)
