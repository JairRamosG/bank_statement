from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent


@CrewBase
class BankStatement():
    """BankStatement crew"""

# Agentes -----------------------------------------------------------------------------
    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def extractor(self) -> Agent:
        return Agent(
            config=self.agents_config['extractor'],
        )

    @agent
    def analista(self) -> Agent:
        return Agent(
            config=self.agents_config['analista'], 
            verbose=True
        )


# Tareas ------------------------------------------------------------------------------
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], 
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'], 
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the BankStatement crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
