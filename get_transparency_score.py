
def get_transparency_score(brand_name):
    df = pd.read_csv('transparency-scores.csv')
    entry = df[df['Brand Name'].str.replace(' ', '_').str.replace('&', '-').str.lower() == brand_name]
    score = None
    if len(entry) > 0:
        score = float(entry['2020 Final scores']) / df['2020 Final scores'].values.max()
    return score