from crewai import Crew, Process
from agents import blog_researcher, blog_writer
from tasks import writer_task, researcher_task


crew = Crew(
    agents=[blog_researcher, blog_writer],
    tasks=[researcher_task, writer_task],
    process=Process.sequential,
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True
)

# start the task execution process 
result = crew.kickoff(inputs={"topic": "AI vs ML vs DL vs Generative Ai"})
print(result)