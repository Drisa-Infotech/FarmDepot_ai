# backend/agents/search_agent.py
from crewai import Agent
from backend.tasks.voice_tasks import search_ad_task

search_agent = Agent(
    role="Ad Search Agent",
    goal="Help users find relevant agricultural products",
    backstory="Expert in interpreting user queries and finding relevant matches in the database.",
    verbose=True,
    allow_delegation=True,
)
