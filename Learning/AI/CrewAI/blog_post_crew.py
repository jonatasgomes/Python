from crewai import Crew, Process, Agent, Task
import os

idea_developer_agent = Agent(
    role='Creative Idea Developer for Blog Posts',
    goal='Generate engaging and innovative blog post ideas based on a specific topic.',
    backstory=(
        'You are a creative writer always up to date with the latest trends. '
        'You have a impressive ability to transform concepts into innovative ideas. '
        'Your curiosity and energy help you create unique suggestions that effectively engage the target audience. '
    ),
    verbose=True,
)

content_planner_agent = Agent(
    role='Blog Content Strategist',
    goal='Planejar e estruturar o conteúdo de maneira eficaz, com base no briefing fornecido',
    backstory=(
        'You are a detail-oriented strategist, passionate about aligning objectives and data with content creation. '
        'You love creating well-structured plans that guide writers to achieve the best results. '
        'Your focus is always on ensuring that the content meets audience expectations and marketing goals.'
    ),
    verbose=True,
)

post_writer_agent = Agent(
    role='Creative Blog Post Writer',
    goal='Write engaging and high-quality blog posts, following the briefing and guidelines provided',
    backstory=(
        'You are a versatile writer, able to adapt your writing style to the desired tone and format. '
        'Your goal is always to create clear, interesting content that captures the reader\'s attention, '
        'transforming ideas and information into engaging and well-structured stories.'
    ),
    verbose=True,
)

post_reviewer_agent = Agent(
    role='Blog Post Reviewer',
    goal='Make sure the post is error-free and ready for publication',
    backstory=(
        'You are a meticulous and detail-oriented reviewer. Your mission is to correct spelling errors, '
        'improve the flow of the text, and ensure that the content is perfectly aligned with the briefing '
        'and quality standards. Your work is to ensure that each post is flawless before publication.'
    ),
    verbose=True,
)

create_idea_task = Task(
    description='Generate a list of 10 different blog post ideas on the topic: {topic}. The ideas should be creative, relevant, and diverse in format, focusing on engaging the target audience.',
    agent=idea_developer_agent,
    expected_output='A list of 10 blog post ideas, each with a creative title and a brief summary of what the content will cover.'
)

select_idea_task = Task(
    description='Select the best idea from the list generated, justifying your choice based on relevance and alignment with the blog\'s objectives.',
    agent=idea_developer_agent,
    expected_output='The selection of one idea with a clear and concise justification of its relevance and alignment with the content objectives.'
)

content_plan_task = Task(
    description='Create a detailed content plan for the blog post including information such as objectives, target audience, tone of voice, keywords, and format.',
    agent=content_planner_agent,
    expected_output='A structured content plan addressing all key points to guide the content creation.'
)

write_post_task = Task(
    description='Write the complete blog post content, following the guidelines of the briefing and the selected idea. Ensure that the post is engaging, well-structured, and suitable for the target audience.',
    agent=post_writer_agent,
    expected_output='A blog post with an introduction, body, and conclusion that is clear, interesting, and aligned with the briefing.'
)

review_post_task = Task(
    description='Review the blog post, correcting grammatical and punctuation errors, as well as improving the flow of the text. Ensure that the post is aligned with the tone and objectives defined in the briefing.',
    agent=post_reviewer_agent,
    expected_output='The reviewed post, free of grammatical errors and with good flow, ready to be published.'
)

post_crew = Crew(
    agents=[
        idea_developer_agent,
        content_planner_agent,
        post_writer_agent,
        post_reviewer_agent
    ],
    tasks=[
        create_idea_task,
        select_idea_task,
        content_plan_task,
        write_post_task,
        review_post_task
    ],
    process=Process.sequential
)

result = post_crew.kickoff({ 'topic': 'Artificial Intelligence in Everyday Life' })
print(result.raw)
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, 'result.md')

with open(output_path, 'w') as f:
    f.write(result.raw)
