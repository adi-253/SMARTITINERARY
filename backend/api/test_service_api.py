import asyncio
import os
import sys
from datetime import datetime, timedelta

sys.path.append('') 

from backend.models.api_models import Sights, FlightSchedule, HotelDetails
from backend.api.Service_Api import flight_schedules, hotel_list, tourist_attractions


# Calculate dates for the tests - using future dates
today = datetime.now()
check_in_date = (today + timedelta(days=30)).strftime("%Y-%m-%d")
check_out_date = (today + timedelta(days=37)).strftime("%Y-%m-%d")


async def test_flight_schedules():
    """Test the flight_schedules function."""
    print("\n--- Testing Flight Schedules API ---")
    flight_request = FlightSchedule(
        departure_airport_code="JFK",
        arrival_airport_code="LAX",
        outbound_date=check_in_date,
        return_date=check_out_date
    )
    
    result = await flight_schedules(flight_request)
    
    print(f"Flight results: {result}")
    print(f"Number of flights found: {len(result)}")
    return result


async def test_hotel_list():
    """Test the hotel_list function."""
    print("\n--- Testing Hotel List API ---")
    hotel_request = HotelDetails(
        city="New York",
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        hotel_class="4,5"  # 4 and 5 star hotels
    )
    
    result = await hotel_list(hotel_request)
    
    print(f"Hotel results: {result}")
    print(f"Number of hotels found: {len(result)}")
    return result


async def test_tourist_attractions():
    """Test the tourist_attractions function."""
    print("\n--- Testing Tourist Attractions API ---")
    attractions_request = Sights(
        query="New York popular attractions"
    )
    
    result = await tourist_attractions(attractions_request)
    
    print(f"Attractions results: {result}")
    print(f"Number of attractions found: {len(result)}")
    return result


# Simple runner functions for each test
def run_flight_test():
    """Run the flight schedules test."""
    if not os.getenv("SERP_API_KEY"):
        print("WARNING: SERP_API_KEY environment variable is not set.")
        return
    return asyncio.run(test_flight_schedules())


def run_hotel_test():
    """Run the hotel list test."""
    if not os.getenv("SERP_API_KEY"):
        print("WARNING: SERP_API_KEY environment variable is not set.")
        return
    return asyncio.run(test_hotel_list())


def run_attractions_test():
    """Run the tourist attractions test."""
    if not os.getenv("SERP_API_KEY"):
        print("WARNING: SERP_API_KEY environment variable is not set.")
        return
    return asyncio.run(test_tourist_attractions())


def run_all_tests():
    """Run all tests sequentially."""
    print("Running all API tests...")
    
    if not os.getenv("SERP_API_KEY"):
        print("WARNING: SERP_API_KEY environment variable is not set.")
        print("Tests may fail if the API key is required.")
        return
    
    # Run all tests in sequence
    flights = asyncio.run(test_flight_schedules())
    hotels = asyncio.run(test_hotel_list())
    attractions = asyncio.run(test_tourist_attractions())
    
    print("\n--- Test Summary ---")
    print(f"Flights found: {len(flights)}")
    print(f"Hotels found: {len(hotels)}")
    print(f"Attractions found: {len(attractions)}")


if __name__ == "__main__":
    # If no arguments, run all tests
    if len(sys.argv) == 1:
        run_all_tests()
    else:
        # Check command line arguments to run specific tests
        test_name = sys.argv[1].lower() if len(sys.argv) > 1 else ""
        
        if test_name == "flights":
            run_flight_test()
        elif test_name == "hotels":
            run_hotel_test() 
        elif test_name == "attractions":
            run_attractions_test()
        else:
            print("Unknown test. Available tests: flights, hotels, attractions")
            print("Example usage: python test_service_api.py flights")