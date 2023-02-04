from app import handle_request
from WebScraping.wiki_page_scrape import wiki_page_scrape

def get_report(brand_name):
    score_map = {}
    
    wiki_score = wiki_page_scrape(brand_name)
    if (wiki_score != -1): # -1 means we failed to get data from this category
        score_map["wiki_score"] = wiki_score # Wikipedia store
    
    transparency_score = get_transparency_score(brand_name)
    if (transparency_score != -1):
        score_map["transparency_score"] = transparency_score

    footprint_score = get_footprint_score(brand_name)
    if (footprint_score != -1):
        score_map["footprint_score"] = footprint_score

    handle_request(score_map)