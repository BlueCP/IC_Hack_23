from transparency_score import transparency_score_for_brands
from WebScraping.wiki_page_scrape import transformed_brand_name

def get_transparency_score(_brand_name):
    brand_name = transformed_brand_name(_brand_name)
    dict = transparency_score_for_brands()
    if brand_name in dict:
        return dict[brand_name]
    else:
        return -1
