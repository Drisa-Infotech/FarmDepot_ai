
from crewai import Agent
from backend.tasks.voice_tasks import post_ad_task

post_agent = Agent(
    role="Ad Posting Agent",
    goal="Help users post agricultural products for sale",
    backstory="Experienced in creating structured classified ads from raw voice or text input.",
    verbose=True,
    allow_delegation=True,
)
