from phi.agent import Agent
from agents.researcher import researcher
from agents.analyst import analyst
from agents.writer import writer
from agents.reviewer import reviewer

manager = Agent(
    name="Manager Agent",
    team=[researcher, analyst, writer, reviewer],
    instructions=[
        "Coordinate all agents",
        "Ensure proper workflow",
        "Return final refined output"
    ],
    markdown=True,
)
