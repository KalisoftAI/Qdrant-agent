import os
from serpapi import GoogleSearch
from dotenv import load_dotenv
load_dotenv()

def get_api_key():
    """
    Retrieves the SerpApi key from an environment variable.
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise ValueError("SERPAPI_API_KEY environment variable not set. Please set it to your SerpApi key.")
    return api_key

def find_places(query, location, api_key):
    """
    Searches for places on Google Maps using SerpApi and extracts relevant details.
    
    Args:
        query (str): The type of place to search for (e.g., "diabetes hospitals").
        location (str): The location to search near.
        api_key (str): Your SerpApi API key.

    Returns:
        list: A list of dictionaries, where each dictionary contains details of a place.
    """
    params = {
        "engine": "google_maps",
        "q": f"{query} near {location}",
        "type": "search",
        "api_key": api_key,
        "hl": "en",
        "gl": "us"
    }

    print(f"\n🔎 Searching for '{query}' near '{location}'...")
    
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if "local_results" not in results:
            print(f"No results found for '{query}'.")
            return []

        place_details = []
        for result in results.get("local_results", []):
            details = {
                "name": result.get("title", "N/A"),
                "address": result.get("address", "N/A"),
                "phone": result.get("phone", "N/A"),
                "email": result.get("email", "N/A"),
                "rating": result.get("rating", 0.0),
                "reviews": result.get("reviews", 0)
            }
            place_details.append(details)
            
        return place_details
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def display_sorted_results(title, places, emoji="📍", limit=None):
    """
    Sorts places, prints them, highlights the best, and optionally limits the list size.
    """
    print("-" * 60)
    print(f"{emoji} {title.upper()} {emoji}")
    print("-" * 60)
    
    if not places:
        print("No information to display.")
        return

    # Sort places: primarily by rating (high to low), secondarily by reviews (high to low).
    sorted_places = sorted(places, key=lambda x: (x.get('rating', 0), x.get('reviews', 0)), reverse=True)

    # Highlight the top result as the best suggestion.
    best_suggestion = sorted_places[0]
    print("\n⭐ Best Suggestion (Based on Rating and Reviews) ⭐")
    print(f"   Name:    {best_suggestion['name']}")
    print(f"   Rating:  {best_suggestion['rating']} stars ({best_suggestion['reviews']} reviews)")
    print(f"   Address: {best_suggestion['address']}")
    print(f"   Phone:   {best_suggestion['phone']}")
    print("-" * 60)

    # Decide the list to display based on the limit
    list_to_display = sorted_places
    if limit:
        list_to_display = sorted_places[:limit]
        print(f"\n📋 Top {len(list_to_display)} Nearby Options:\n")
    else:
        print("\n📋 Full List of Nearby Options:\n")

    for i, place in enumerate(list_to_display, 1):
        print(f"{i}. Name:    {place['name']}")
        print(f"   Rating:  {place['rating']} stars ({place['reviews']} reviews)")
        print(f"   Address: {place['address']}")
        print(f"   Phone:   {place['phone']}\n")
    print("-" * 60)


if __name__ == "__main__":
    try:
        my_api_key = get_api_key()

        # Get user input for the location.
        user_location = input("Enter a location (e.g., 'Bhavnagar, Gujarat'): ")
        
        if not user_location.strip():
            print("Location cannot be empty.")
        else:
            hospital_query = "diabetes hospitals"
            lab_query = "blood laboratories"
            
            hospitals = find_places(hospital_query, user_location, my_api_key)
            labs = find_places(lab_query, user_location, my_api_key)
            
            if hospitals:
                # Call the display function with a limit of 10 for hospitals
                display_sorted_results("Diabetes Hospitals Found", hospitals, emoji="🏥", limit=10)
            
            if labs:
                # Call the display function with no limit for labs
                display_sorted_results("Blood Laboratories Found", labs, emoji="🔬")

    except ValueError as ve:
        print(f"Error: {ve}")