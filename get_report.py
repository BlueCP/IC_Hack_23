import numpy as np
import sys
import pandas as pd

from WebScraping.wiki_page_scrape import wiki_page_scrape
import get_transparency_score

def get_report(brand_name):
    score_map = {'name' : brand_name }
    
    transparency_score = get_transparency_score(brand_name)
    wiki_score = wiki_page_scrape(brand_name)

    scores = [transparency_score, wiki_score]
    score_map['trans_score'] = transparency_score
    score_map['wiki_score'] = wiki_score

    # remove Nones from scores
    existingScores = [x for x in scores if x is not None]

    if len(existingScores) > 0:
        score_map['mean_score'] = np.mean(existingScores)
    else:
        score_map['mean_score'] = None
    return (score_map)

