import pandas as pd 
from fuzzywuzzy import fuzz
import re

## load in theme data
themes_df = pd.read_csv('data/themes_raw.csv')

## sort by theme in ascending order
themes_df = themes_df.sort_values('theme', ascending=True)

## get length of themes_df
themes_df_len = len(themes_df)

## theme mapping 
def map_theme_to_category_combined_modified(theme):
    theme_lower = theme.lower()
    
    def fuzzy_match(keyword_list, threshold=85):
        return any(fuzz.partial_ratio(theme_lower, keyword) >= threshold for keyword in keyword_list)
    
    # Agriculture and Food
    if re.search(r'\b(agriculture|food)\b', theme_lower) or fuzzy_match(['agriculture', 'food', 'farm', 'farming', 'means', 'crops', 'livestock', 'produce', 'ranch', 'ranching', 'agricultural', 'agriculturally', 'agricultureal']):
        return "Agriculture and Food"
    
    # Education
    elif re.search(r'\b(edu|school|university|college)\b', theme_lower) or fuzzy_match(['edu', 'school', 'university', 'college', 'education', 'educational', 'learning', 'learn', 'teach', 'teaching', 'schooling']):
        return "Education"
    
    # Business, Economic, and Financial
    elif re.search(r'\b(econ|business|financial|commerce)\b', theme_lower) or fuzzy_match(['econ', 'business', 'financial', 'commerce', 'economic', 'economical', 'economically', 'businesses', 'small business', 'small businesses', 'large business', 'large businesses', 'financially', 'financials', 'financially']):
        return "Business, Economic, and Financial"
    
    # Health and Safety
    elif re.search(r'\b(health|safety|medical|hospital)\b', theme_lower) or fuzzy_match(['health', 'safety', 'medical', 'hospital', 'covid', 'covid-19', 'coronavirus', 'pandemic', 'healthcare', 'healthcare', 'medical', 'medically', 'hospital', 'hospitals', 'safety', 'safety', 'safely', 'safe', 'public safety', 'public health', 'public healthcare', 'public hospitals']):
        return "Health and Safety"
    
    # Infrastructure
    elif re.search(r'\b(infrastructure|construction|building)\b', theme_lower) or fuzzy_match(['infrastructure', 'construction', 'building']):
        return "Infrastructure"
    
    # Natural Resources, Energy, and the Environment
    elif re.search(r'\b(natural resource|energy|energies|environment|water)\b', theme_lower) or fuzzy_match(['natural resource', 'energy', 'environment', 'water']):
        return "Natural Resources, Energy, and the Environment"
    
    # Public Service, Politics, and Governance
    elif re.search(r'\b(public service|politic|governance|government)\b', theme_lower) or fuzzy_match(['public service', 'politic', 'governance', 'government']):
        return "Public Service, Politics, and Governance"
    
    # Transportation
    elif re.search(r'\b(transportation|transit|traffic)\b', theme_lower) or fuzzy_match(['transportation', 'transit', 'traffic']):
        return "Transportation"
    
    else:
        return None 

# Apply the mapping function to create a new 'Category' column
themes_df['dcat_theme_new'] = themes_df['theme'].apply(map_theme_to_category_combined_modified)

## Save themes_df to a csv as themes_mapped.csv 
themes_df.to_csv('data/themes_mapped.csv', index=False)