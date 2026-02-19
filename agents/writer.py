from phi.agent import Agent

writer = Agent(
    name="Writer Agent",
    role="Writes structured content",
    instructions=[
        "Write detailed explanation",
        "Use headings",
        "Make content easy to understand"
    ],
    markdown=True,
)
