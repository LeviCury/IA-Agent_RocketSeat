from pathlib import Path

import yaml
from crewai import Agent, Crew, Process, Task
from crewai_tools import DallETool, SerperDevTool


CONFIG_DIR = Path(__file__).parent / "config"


def _load_yaml(filename: str) -> dict:
    with open(CONFIG_DIR / filename, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_crew(query: str) -> Crew:
    """Build and return the video-production crew ready to kick off."""

    agents_cfg = _load_yaml("agents.yaml")
    tasks_cfg = _load_yaml("tasks.yaml")

    serper = SerperDevTool()
    dalle = DallETool(model="dall-e-3", size="1792x1024", quality="standard", n=1)

    def _interpolate(text: str) -> str:
        return text.replace("{query}", query)

    # --- Agents -----------------------------------------------------------

    roteirista = Agent(
        role=_interpolate(agents_cfg["roteirista"]["role"]),
        goal=_interpolate(agents_cfg["roteirista"]["goal"]),
        backstory=_interpolate(agents_cfg["roteirista"]["backstory"]),
        tools=[serper],
        verbose=True,
        allow_delegation=False,
    )

    criador_thumbnail = Agent(
        role=_interpolate(agents_cfg["criador_thumbnail"]["role"]),
        goal=_interpolate(agents_cfg["criador_thumbnail"]["goal"]),
        backstory=_interpolate(agents_cfg["criador_thumbnail"]["backstory"]),
        tools=[dalle],
        verbose=True,
        allow_delegation=False,
    )

    revisor = Agent(
        role=_interpolate(agents_cfg["revisor"]["role"]),
        goal=_interpolate(agents_cfg["revisor"]["goal"]),
        backstory=_interpolate(agents_cfg["revisor"]["backstory"]),
        tools=[],
        verbose=True,
        allow_delegation=False,
    )

    # --- Tasks -------------------------------------------------------------

    t_cfg = tasks_cfg["pesquisa_e_roteiro"]
    pesquisa_e_roteiro = Task(
        description=_interpolate(t_cfg["description"]),
        expected_output=_interpolate(t_cfg["expected_output"]),
        agent=roteirista,
    )

    t_cfg = tasks_cfg["criacao_thumbnails"]
    criacao_thumbnails = Task(
        description=_interpolate(t_cfg["description"]),
        expected_output=_interpolate(t_cfg["expected_output"]),
        agent=criador_thumbnail,
        context=[pesquisa_e_roteiro],
    )

    t_cfg = tasks_cfg["revisao_final"]
    revisao_final = Task(
        description=_interpolate(t_cfg["description"]),
        expected_output=_interpolate(t_cfg["expected_output"]),
        agent=revisor,
        context=[pesquisa_e_roteiro, criacao_thumbnails],
        output_file="output/resultado_final.md",
    )

    # --- Crew --------------------------------------------------------------

    return Crew(
        agents=[roteirista, criador_thumbnail, revisor],
        tasks=[pesquisa_e_roteiro, criacao_thumbnails, revisao_final],
        process=Process.sequential,
        verbose=True,
    )
