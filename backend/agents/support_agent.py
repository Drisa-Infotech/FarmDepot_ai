
from crewai import Agent
from sqlalchemy import create_engine
from config import settings

engine = create_engine(settings.DB_URL)

support_agent = Agent(
    role="Customer Support Agent",
    goal="Answer questions and help users navigate the AgricVoice app",
    backstory="Knows how the platform works and provides assistance in multiple languages.",
    verbose=True,
    allow_delegation=True,
)
