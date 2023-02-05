import numpy as np
import sys
import pandas as pd

from WebScraping.wiki_page_scrape import wiki_page_scrape

def get_report(brand_name):
    score_map = {'name' : brand_name }

    transparency_score = get_transparency_score(brand_name)
    wiki_score = wiki_page_scrape(brand_name)

    scores = [transparency_score, wiki_score]
    if transparency_score is not None:
        score_map['trans_score'] = transparency_score
    if wiki_score is not None:
        score_map['wiki_score'] = wiki_score

    print(wiki_score, file=sys.stdout)

    # remove Nones from scores
    existingScores = [x for x in scores if x is not None]

    if len(existingScores) > 0:
        score_map['mean_score'] = np.mean(existingScores)
    else:
        score_map['mean_score'] = None
    return (score_map)

def get_transparency_score(brand_name):
    df = pd.read_csv('transparency-scores.csv')
    entry = df[df['Brand Name'].str.replace(' ', '_').str.replace('&', '-').str.lower() == brand_name]
    score = None
    if len(entry) > 0:
        score = float(entry['2020 Final scores']) / df['2020 Final scores'].values.max()
    return score
