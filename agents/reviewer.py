from phi.agent import Agent

reviewer = Agent(
    name="Reviewer Agent",
    role="Reviews and improves content",
    instructions=[
        "Fix grammar",
        "Improve clarity",
        "Ensure professional tone"
    ],
    markdown=True,
)
