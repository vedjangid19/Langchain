from crewai import Agent
import os
from dotenv import load_dotenv

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['OPENAI_MODEL_NAME'] = "gpt-4-0125-preview"


# from dotenv import load_dotenv
# import os

# load_dotenv()

# if not os.getenv("OPENAI_API_KEY"):
#     raise EnvironmentError("OPENAI_API_KEY not found in environment variables or .env file.")

print(f"openai api key : {[[os.getenv('OPENAI_API_KEY')]]}")
from tool import youtube_tool
# CREATE A SENIOR BLOG CONTENT RESEARCHER
blog_researcher = Agent(
    role="Blog Researcher from youtube video",
    goal="get the relevant video content for the topic {topic} from youtube channel",
    backstory="expert in understanding the videos in AI Data science, machine learning, genai and providing suggesion",
    verbose=True,
    allow_delegation=True,
    tools=[youtube_tool],
    memory=True
)

# CREATE A SENIOR BLOG WRITER AGENT WITH YOUTUBE TOOL
blog_writer = Agent(
    role="Blog Writer",
    goal="Narrate compelling tech stories about the video {topic} from youtube channel",
    backstory= (
        "with a flair fro simplifing complex topic you craft"
        "engaging narratives that captivate and educate bring new"
        "discoveries to light in an accessible manner"
    ),
    tools=[youtube_tool],
    verbose=True,
    allow_delegation=False,
    memory=True
)

