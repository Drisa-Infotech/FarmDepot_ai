# backend/agents/voice_agent.py
from crewai import Agent
from backend.tasks.voice_tasks import transcribe_audio_task

voice_agent = Agent(
    role="Voice Interaction Specialist",
    goal="Transcribe and process voice commands from users",
    backstory="Expert in handling voice-to-text and understanding user queries.",
    verbose=True,
    allow_delegation=False,
)