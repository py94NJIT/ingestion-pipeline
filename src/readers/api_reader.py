import time
import requests
import logging

logger = logging.getLogger("pipeline.readers.api")

def extract_manga_by_genre(genre_id: int, max_pages: int = 2) -> list:
    """Queries Jikan API endpoints dynamically across sequential pages."""
    base_url = "https://api.jikan.moe/v4/manga"
    all_manga_records = []
    
    params = {
        "genres": genre_id,
        "order_by": "score",
        "sort": "desc",
        "page": 1,
    }
    
    while params["page"] <= max_pages:
        logger.info(f"Fetching Jikan Manga API Page {params['page']}...")
        response = requests.get(base_url, params=params)
        
        if response.status_code == 429:
            logger.warning("Rate limit hit! Throttling stream for 2 seconds...")
            time.sleep(2)
            continue
            
        if response.status_code != 200:
            logger.error(f"API Error on page {params['page']}: Status {response.status_code}")
            break
            
        payload = response.json()
        page_data = payload.get("data", [])
        
        if not page_data:
            break
            
        all_manga_records.extend(page_data)
        
        pagination = payload.get("pagination", {})
        if not pagination.get("has_next_page", False):
            break
            
        params["page"] += 1
        time.sleep(1) # Safe spacing courtesy window for Jikan limits
        
    return all_manga_records