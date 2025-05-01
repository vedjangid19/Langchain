from crewai_tools import YoutubeChannelSearchTool, YoutubeVideoSearchTool
import os
from dotenv import load_dotenv

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['OPENAI_MODEL_NAME'] = "gpt-4-0125-preview"

youtube_tool = YoutubeChannelSearchTool(youtube_channel_handle="@krishnaik06")