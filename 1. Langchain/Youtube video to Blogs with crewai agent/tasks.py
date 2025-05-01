from crewai import Task
from tool import youtube_tool
from agents import blog_researcher, blog_writer


# CREATE RESEARCHER TASK
researcher_task = Task(
    description=(
        "identify the video {topic}."
        "get details information about the video from the channel"
    ),
    expected_output="a comprehsive 3 paragraph long report based on the {topic} of the video content and each pargraph have relevant heading.",
    tools=[youtube_tool],
    agent=blog_researcher
)

# WRITING TASK WIN LANGUAGE MODEL CONFIGURATION
writer_task = Task(
    description=("get the info from the youtube channel video on the topic {topic}"),
    expected_output="summarize the info from the youtube channel video on the topic {topic} and create the content for the blog",
    tools=[youtube_tool],
    agent=blog_writer,
    async_execution=False,
    output_file="new_blog_post.md"
)

