import sys
sys.path.append('')
import asyncio
from crewai import Agent,Task,Process,Crew
from agents.llm import llm_model
from datetime import datetime
from utils.logger import get_logger

logger = get_logger(__name__)


async def generate_itinerary(must_visit_locations:str, flights_text:str, hotels_text:str, check_in_date, check_out_date):
    """Generate a detailed travel itinerary based on flight and hotel information."""
    try:
        # Convert the string dates to datetime objects
        check_in = datetime.strptime(check_in_date, "%Y-%m-%d")
        check_out = datetime.strptime(check_out_date, "%Y-%m-%d")

        # Calculate the difference in days
        days = (check_out - check_in).days

        model = llm_model

        analyze_agent = Agent(
            role="AI Travel Planner",
            goal="Create a detailed itinerary for the user based on flight and hotel information",
            backstory="AI travel expert generating a day-by-day itinerary including flight details, hotel stays, and must-visit locations in the destination.",
            llm=model,
            verbose=False
        )

        analyze_task = Task(
            description=f"""
            Based on the following details, create a {days}-day itinerary for the user:

            **Flight Details**:
            {flights_text}

            **Hotel Details**:
            {hotels_text}

            **Must-visit locations**: {must_visit_locations}

            **Travel Dates**: {check_in_date} to {check_out_date} ({days} days)

            The itinerary should include:
            - Flight arrival and departure information
            - Hotel check-in and check-out details
            - Day-by-day breakdown of activities
            - Must-visit attractions and estimated visit times
            - Restaurant recommendations for meals
            - Tips for local transportation
            - Do not include all the options for hotels,flights and sights. Only the best ones to be included.

            📝 **Format Requirements**:
            - Use markdown formatting with clear headings (# for main headings, ## for days, ### for sections)
            - Include emojis for different types of activities (🏛️ for landmarks, 🍽️ for restaurants, etc.)
            - Use bullet points for listing activities
            - Include estimated timings for each activity
            - Format the itinerary to be visually appealing and easy to read
            """,
            agent=analyze_agent,
            expected_output="A well-structured, visually appealing itinerary in markdown format, including flight, hotel, and day-wise breakdown with emojis, headers, and bullet points."
        )

        itinerary_planner_crew = Crew(
            agents=[analyze_agent],
            tasks=[analyze_task],
            process=Process.sequential,
            verbose=False
        )

        crew_results = await asyncio.to_thread(itinerary_planner_crew.kickoff)

        # Handle different possible return types from CrewAI
        if hasattr(crew_results, 'outputs') and crew_results.outputs:
            return crew_results.outputs[0]
        elif hasattr(crew_results, 'get'):
            return crew_results.get("AI Travel Planner", "No itinerary available.")
        else:
            return str(crew_results)

    except Exception as e:
        logger.exception(f"Error generating itinerary: {str(e)}")
        return "Unable to generate itinerary due to an error. Please try again later."