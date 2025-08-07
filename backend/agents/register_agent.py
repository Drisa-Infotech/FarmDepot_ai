# backend/agents/register_agent.py
from crewai import Agent
from backend.tasks.register_tasks import register_user_task

register_agent = Agent(
    role="User Registration Agent",
    goal="Register users using basic profile information",
    backstory="Helps new users register using either voice or text instructions.",
    verbose=True,
    allow_delegation=False,
)
