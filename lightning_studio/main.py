import os
from crewai import Agent, Task, Crew, Process
from textwrap import dedent
from tools.scraper_tools import ScraperTool

# Set the OpenAI API key environment variable
os.environ["OPENAI_API_KEY"] = "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"

# Define the ScraperTool class if not already defined in scraper_tools.py
class ScraperTool:
    def scrape(self, url: str) -> str:
        # Placeholder for the actual scraping logic
        # This should return the scraped content from the given URL as a string
        return f"Scraped content from {url}"

class NewsletterCrew:
    def __init__(self, urls):
        self.urls = urls

    def run(self):
        # Initialize the scraper Agent with the scraping tool
        scraper = Agent(
            role='Summarizer of Websites',
            goal='Ask the user for a list of URLs, then use the WebsiteSearchTool to scrape the content, and provide the full content to the writer agent so it can then be summarized',
            backstory="""You work at a leading tech think tank. Your expertise is taking URLs and getting just the text-based content of them.""",
            verbose=True,
            allow_delegation=False,
            tools=[ScraperTool().scrape]  # Ensure this matches the method signature and exists in scraper_tools.py
        )

        # Initialize the writer Agent, assuming no specific tools are required for writing
        writer = Agent(
            role='Tech Content Summarizer and Writer',
            goal='Craft compelling short-form content on AI advancements based on long-form text passed to you',
            backstory="""You are a renowned Content Creator, known for your insightful and engaging articles. You transform complex concepts into compelling narratives.""",
            verbose=True,
            allow_delegation=True,
            tools=[]  # Even if no tools are used, define tools as an empty list to avoid errors
        )

        # Define the tasks for each agent
        task1 = Task(
            description=f"Take a list of websites that contain AI content, read/scrape the content, and then pass it to the writer agent. Here are the URLs from the user that you need to scrape: {self.urls}",
            agent=scraper
        )

        task2 = Task(
            description="Using the text provided by the scraper agent, develop a short and compelling/interesting short-form summary of the text provided to you about AI",
            agent=writer
        )

        # Define the crew and assign the tasks
        newsletterCrew = Crew(
            agents=[scraper, writer],
            tasks=[task1, task2],
            verbose=2  # Adjust logging level as needed
        )

        # Start the crew process
        newsletterCrew.kickoff()

if __name__ == "__main__":
    print("## Welcome to Newsletter Writer")
    print('-------------------------------')
    urls = input(dedent("What is the URL you want to summarize? "))
  
    # Instantiate NewsletterCrew with the provided URL(s) and run the process
    newsletter_crew = NewsletterCrew(urls)
    newsletter_crew.run()

