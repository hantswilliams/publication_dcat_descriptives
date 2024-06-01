import pandas as pd 
from database.mongoConnect import mongodbconnection
import math
from itertools import chain
import numpy as np
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd, MultiComparison
import ast

# Load the enhanced list of DCAT records
listEnhanced = pd.read_csv('data/list_enhanced.csv')

# Connect to MongoDB
## in order for this to work, you must have the .env file with the appropriate credentials
## please read the README.md file for more information
db = mongodbconnection()
collection = db["dcat"]

# MongoDB: Get the count of documents
doc_count = collection.count_documents({})

# 0. Value counts of compliant and non-compliant records
complaint_noncompliant = listEnhanced['dcat_compliant'].value_counts()

# Group by 'type' field and get counts of dcat_compliant field
complaint_noncompliant_pivot = listEnhanced.groupby('type')['dcat_compliant'].value_counts().unstack().fillna(0)
complaint_noncompliant_pivot['total'] = complaint_noncompliant_pivot[False] + complaint_noncompliant_pivot[True]
complaint_noncompliant_pivot['percent_compliant'] = (complaint_noncompliant_pivot[True] / complaint_noncompliant_pivot['total']) * 100
complaint_noncompliant_pivot['percent_noncompliant'] = (complaint_noncompliant_pivot[False] / complaint_noncompliant_pivot['total']) * 100

# 1. Value counts of the different URLs (unique)
results = collection.find({}, {'site': 1, '_id': 0})
urls = [result.get('site', 'No url found') for result in results if result.get('site', 'No url found') != 'No url found']
urls = pd.Series(urls)
urls_count = urls.value_counts()
total_urls_unique = len(urls_count)

# 2. Value counts of the different types (unique)
results = collection.find({}, {'type': 1, '_id': 0})
types = [result.get('type', 'No type found') for result in results if result.get('type', 'No type found') != 'No type found']
types = pd.Series(types)
types_count = types.value_counts()
total_types_unique = types_count.sum()

# 3. Value counts of data volume within each data catalog
catalog_vol_df = listEnhanced[['url', 'type', 'dcat_compliant', 'data_assets']]
catalog_vol_df = catalog_vol_df[(catalog_vol_df['dcat_compliant'] == True) & (catalog_vol_df['data_assets'] > 0)]
cat_type = catalog_vol_df.groupby('type')['data_assets'].describe()

# Perform 1-way ANOVA to test for differences in data volume by 'type' field
federal_data = catalog_vol_df[catalog_vol_df['type'] == 'Federal']['data_assets']
state_data = catalog_vol_df[catalog_vol_df['type'] == 'State']['data_assets']
county_data = catalog_vol_df[catalog_vol_df['type'] == 'County']['data_assets']
city_data = catalog_vol_df[catalog_vol_df['type'] == 'City']['data_assets']
f_val, p_val = stats.f_oneway(federal_data, state_data, county_data, city_data)

# Post-hoc tests
mc = MultiComparison(catalog_vol_df['data_assets'], catalog_vol_df['type'])
result = mc.tukeyhsd()
print(result)

# 4. Value counts of metadata fields within each data catalog
catalog_metadata_df = listEnhanced[['url', 'type', 'dcat_compliant', 'metavariable_count']]
catalog_metadata_df = catalog_metadata_df[(catalog_metadata_df['dcat_compliant'] == True) & (catalog_metadata_df['metavariable_count'] > 0)]
catalog_metadata_df.groupby('type')['metavariable_count'].describe()

# Perform 1-way ANOVA to test for differences in metadata volume by 'type' field
federal_metadata = catalog_metadata_df[catalog_metadata_df['type'] == 'Federal']['metavariable_count']
state_metadata = catalog_metadata_df[catalog_metadata_df['type'] == 'State']['metavariable_count']
county_metadata = catalog_metadata_df[catalog_metadata_df['type'] == 'County']['metavariable_count']
city_metadata = catalog_metadata_df[catalog_metadata_df['type'] == 'City']['metavariable_count']
f_val, p_val = stats.f_oneway(federal_metadata, state_metadata, county_metadata, city_metadata)

# Post-hoc tests
mc = MultiComparison(catalog_metadata_df['metavariable_count'], catalog_metadata_df['type'])
result = mc.tukeyhsd()
print(result)

# 5. Frequencies of the different themes
results = collection.find({}, {'theme': 1, 'site': 1, 'type': 1, '_id': 0})
themes = [{'site': result.get('site'), 'theme': result.get('theme'), 'type': result.get('type')} for result in results if isinstance(result.get('theme'), list)]

cleaned_data = [(item['site'], theme, item['type']) for item in themes for theme in item['theme']]
themes_df = pd.DataFrame(cleaned_data, columns=['site', 'theme', 'type'])
total_themes_unique = themes_df.shape[0]

themes_df['count'] = 1

# Overall counts of each unique theme
themes_df_all = themes_df.groupby(['theme']).count().reset_index().sort_values('count', ascending=False)
themes_df_all = themes_df_all[['theme', 'count']]

# Counts of each unique theme by 'type'
themes_df_type = themes_df.groupby(['type', 'theme']).count().reset_index().sort_values('count', ascending=False)
themes_df_type = themes_df_type[['type', 'theme', 'count']]

# Calculate the percentage of themes by type
themes_df_type = themes_df_type.merge(themes_df_type.groupby('type')['count'].sum().rename('total'), on='type')
themes_df_type['percent'] = themes_df_type['count'] / themes_df_type['total'] * 100
themes_df_type['percent_count'] = themes_df_type['percent'].map('{:,.2f}%'.format) + ' (' + themes_df_type['count'].map(str) + ')'

# 6. Frequencies of the different keywords
results = collection.find({}, {'keyword': 1, 'site': 1, 'type': 1, '_id': 0})
keywords = [{'site': result.get('site'), 'keyword': result.get('keyword'), 'type': result.get('type')} for result in results if isinstance(result.get('keyword'), list)]

cleaned_data = [(item['site'], keyword, item['type']) for item in keywords for keyword in item['keyword']]
keywords_df = pd.DataFrame(cleaned_data, columns=['site', 'keyword', 'type'])
total_keywords_unique = keywords_df.shape[0]

keywords_df['count'] = 1

# Overall counts of each unique keyword
keywords_df_all = keywords_df.groupby(['keyword']).count().reset_index().sort_values('type', ascending=False)
keywords_df_all = keywords_df_all[['keyword', 'type']]

# Counts of each unique keyword by 'type'
keywords_df_type = keywords_df.groupby(['type', 'keyword']).count().reset_index().sort_values('site', ascending=False)
keywords_df_type = keywords_df_type[['type', 'keyword', 'site']]

# 7. Theme translation (transformation) with RegEx, FuzzyWuzzy, and/or other methods
results = collection.find({}, {'dcat_id': 1, 'theme': 1, 'site': 1, 'type': 1, '_id': 0})

themes = []
for result in results:
    dcat_id = result.get('dcat_id')
    value = result.get('theme', 'No theme found')
    site = result.get('site')
    type_value = result.get('type', 'No type found')  # Assuming a default value for missing 'type'
    output = {
        'dcat_id': dcat_id,
        'site': site,
        'theme': value,
        'type': type_value
    }
    if value != 'No theme found':
        themes.append(output)
    else:
        continue

cleaned_data = [(item['dcat_id'], item['site'], theme, item['type']) for item in themes if isinstance(item['theme'], list) for theme in item['theme']]
themes_df = pd.DataFrame(cleaned_data, columns=['dcat_id', 'site', 'theme', 'type'])

### Load in mapping data
themes_df_mapping = pd.read_csv('data/themes_mapped.csv')
themes_df_mapping = themes_df_mapping[['theme', 'dcat_theme_new']].dropna(subset=['dcat_theme_new']).drop_duplicates(subset=['theme'])

### Merge themes_df with themes_df_mapping on 'theme' field
themes_df_combined = themes_df.merge(themes_df_mapping, how='left', left_on='theme', right_on='theme')

### Now get a count of nan and not nan for dcat_theme_new
themes_df_combined['dcat_theme_new'].isna().sum()
themes_df_combined['dcat_theme_new'].notna().sum()

## Calculate the percentage of themes that were successfully mapped
themes_df_len = len(themes_df_combined)
mapping_success = pd.DataFrame(themes_df_combined['dcat_theme_new'].value_counts())
total_count = mapping_success['count'].sum()
successfully_map_percent = (total_count / themes_df_len) * 100 # about 30% coverage right now

## Get counts of the newly mapped themes by type
themes_df_combined_type = themes_df_combined.groupby(['type','dcat_theme_new']).count().reset_index()

## Keep only type, dcat_theme_new, and theme columns
themes_df_combined_type = themes_df_combined_type[['type', 'dcat_theme_new', 'theme']]
themes_df_combined_type = themes_df_combined_type.rename(columns={'theme': 'count'})
themes_df_combined_type = themes_df_combined_type.sort_values(['type', 'count'], ascending=[True, False]) ## sort by type and count

## Generate total count of Federal themes
total_federal_themes = themes_df_combined_type[themes_df_combined_type['type'] == 'Federal']['count'].sum()

## Generate total count of State themes
total_state_themes = themes_df_combined_type[themes_df_combined_type['type'] == 'State']['count'].sum()

## Generate total count of County themes
total_county_themes = themes_df_combined_type[themes_df_combined_type['type'] == 'County']['count'].sum()

## Generate total count of City themes
total_city_themes = themes_df_combined_type[themes_df_combined_type['type'] == 'City']['count'].sum()

## For each row that has a federal theme, calculate the percentage of the total federal themes
themes_df_combined_type['percent'] = themes_df_combined_type.apply(lambda row: (row['count'] / total_federal_themes) * 100 if row['type'] == 'Federal' else ((row['count'] / total_state_themes) * 100 if row['type'] == 'State' else ((row['count'] / total_county_themes) * 100 if row['type'] == 'County' else ((row['count'] / total_city_themes) * 100 if row['type'] == 'City' else 0))), axis=1)

## Create new percent_count column that gives the percentage with 2 decmil places, then has the count in parentheses
themes_df_combined_type['percent_count'] = themes_df_combined_type['percent'].map('{:,.2f}%'.format) + ' (' + themes_df_combined_type['count'].map(str) + ')'

## Look at meta data attribute frequency: listEnhanced : site_keys 
site_keys = listEnhanced[['url', 'dcat_compliant', 'type', 'site_keys', 'data_assets']]

## keep only rows that are dcat_compliant with a non-null site_keys
site_keys = site_keys[(site_keys['dcat_compliant'] == True) & (site_keys['data_assets'] > 0)]

## Loop through each value in the list for column site_keys and get a value_count across the 'type' field
site_keys = site_keys[['type', 'site_keys']]
site_keys['site_keys'] = site_keys['site_keys'].apply(ast.literal_eval)
site_keys_explode = site_keys.explode('site_keys')

## Get a count of each unique site_keys
summary_keys = site_keys_explode['site_keys'].value_counts()
summary_keys = summary_keys.reset_index()

## Create a new column that gives the percentage of the total count, dividing count by 256
summary_keys['percent'] = (summary_keys['count'] / 256) * 100