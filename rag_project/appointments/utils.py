# appointments/utils.py
import os
from serpapi import GoogleSearch
from django.conf import settings

def find_hospitals(location):
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise ValueError("SERPAPI_API_KEY environment variable not set.")

    params = {
        "engine": "google_maps",
        "q": f"diabetes hospitals near {location}",
        "type": "search",
        "api_key": api_key,
        "hl": "en",
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    
    if "local_results" not in results:
        return []

    hospital_details = []
    for result in results.get("local_results", []):
        details = {
            "name": result.get("title", "N/A"),
            "address": result.get("address", "N/A"),
            "phone": result.get("phone", "N/A"),
            "rating": result.get("rating", 0.0),
            "reviews": result.get("reviews", 0)
        }
        hospital_details.append(details)
    
    # Sort by rating and reviews
    sorted_hospitals = sorted(hospital_details, key=lambda x: (x.get('rating', 0), x.get('reviews', 0)), reverse=True)
    return sorted_hospitals[:10] # Return top 10