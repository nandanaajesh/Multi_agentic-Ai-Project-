from phi.agent import Agent

analyst = Agent(
    name="Analysis Agent",
    role="Analyzes research data",
    instructions=[
        "Analyze the research",
        "Identify key insights",
        "Summarize findings clearly"
    ],
    markdown=True,
)
