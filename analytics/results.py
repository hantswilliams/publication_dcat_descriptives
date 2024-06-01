import pandas as pd 
from database.mongoConnect import mongodbconnection
import math
from itertools import chain
import numpy as np
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multicomp import MultiComparison
import ast

listEnhanced = pd.read_csv('data/list_enhanced.csv')
listEnhanced.columns

db = mongodbconnection()

## Mongo Section
collection = db["dcat"]
collection.count_documents({}) ## get a count of the number of records in the collection

### Analyses to conduct for paper 1: 
# 0. Value counts of compliant and non-compliant records
    # 0b. Also show this as a pivot by 'type' field: Federal, State, County, City
# 1. Value counts of the different URLs (unique)
# 2. Value counts of the different types (unique)
# 3. Value counts of data volume within each data catalog 
    # 3b. Generate overall descriptives 
    # 3c. Generate descriptives by 'type' field: Federal, State, County, City
    # 3d. Perform 1-way ANOVA to test for differences in data volume by 'type' field
# 4. Value counts of meta data fields within each data catalog
    # 4b. Generate overall descriptives
    # 4c. Generate descriptives by 'type' field: Federal, State, County, City
    # 4d. Perform 1-way ANOVA to test for differences in metadata volume by 'type' field
# 5. Frequencies of the different themes (without any modification to theme text) - most frequent, least frequent
    # - 5b. Also show this as a pivot by 'type' field: Federal, State, County, City 
# 6. Frequencies of the different keywords (without any modification to keyword text) - most frequent, least frequent
    # - 6b. Also show this as a pivot by 'type' field: Federal, State, County, City
# 7. Theme translation (transformation) with RegEx, FuzzyWuzzy, and/or other methods
    # - Then perform frequency analysis on the translated themes
    # - Get a percentage of themes that were successfully mapped versus not mapped 
    # - Also show this as a pivot by 'type' field: Federal, State, County, City
# 8. Keyword translation (transformation) with RegEx, FuzzyWuzzy, and/or other methods
    # - Then perform frequency analysis on the translated keywords
    # - Also show this as a pivot by 'type' field: Federal, State, County, City

##### # 0. Value counts of compliant and non-compliant records
## get counts of the 'dcat_compliant' field
complaint_noncompliant = listEnhanced['dcat_compliant'].value_counts()

## group by 'type' field, and get counts of dcat_compliant field 
complaint_noncompliant_pivot = listEnhanced.groupby('type')['dcat_compliant'].value_counts().unstack().fillna(0)
## create percentage columns
complaint_noncompliant_pivot['total'] = complaint_noncompliant_pivot[False] + complaint_noncompliant_pivot[True]
complaint_noncompliant_pivot['percent_compliant'] = (complaint_noncompliant_pivot[True] / complaint_noncompliant_pivot['total']) * 100
complaint_noncompliant_pivot['percent_noncompliant'] = (complaint_noncompliant_pivot[False] / complaint_noncompliant_pivot['total']) * 100

##### # 1. Value counts of the different URLs (unique)
## get counts of the 'url' field

results = collection.find({}, {'site': 1, '_id': 0})
## get a list of the urls
urls = []
for result in results:
    value = result.get('site', 'No url found')
    if value != 'No url found':
        urls.append(value)
    else:
        continue
## keep only unique urls
urls = pd.Series(urls)
## get counts of each unique url
urls_count = urls.value_counts()
## get length of unique urls
total_urls_unique = len(urls_count)



##### # 2. Value counts of the different types (unique)
## get counts of the 'type' field
results = collection.find({}, {'type': 1, '_id': 0})
## get a list of the types
types = []
for result in results:
    value = result.get('type', 'No type found')
    if value != 'No type found':
        types.append(value)
    else:
        continue
## get a count of the types
types = pd.Series(types)
types_count = types.value_counts()
## create sum of types
total_types_unique = types_count.sum()



##### # 3. Value counts of data volume within each data catalog that is DCAT compliant
## get counts of each unique url
cataog_volume = urls.value_counts()
type(cataog_volume)
## generate descriptive statistics, overall 
cataog_volume.describe()
cataog_volume.median()

## generate descriptive statistics by 'type' field: Federal, State, County, City
catalog_vol_df = listEnhanced[['url', 'type', 'dcat_compliant', 'data_assets']]
## keep only where dcat_compliant is True and data_assets is greater than 0
catalog_vol_df = catalog_vol_df[(catalog_vol_df['dcat_compliant'] == True) & (catalog_vol_df['data_assets'] > 0)]
cat_type = catalog_vol_df.groupby('type')['data_assets'].describe() ## group by type and get descriptive statistics

## conduct 1-way ANOVA to test for differences in 'mean' in cat_type
federal_data = catalog_vol_df[(catalog_vol_df['type'] == 'Federal') & (catalog_vol_df['dcat_compliant'] == True) & (catalog_vol_df['data_assets'] > 0)]['data_assets']
state_data = catalog_vol_df[(catalog_vol_df['type'] == 'State') & (catalog_vol_df['dcat_compliant'] == True) & (catalog_vol_df['data_assets'] > 0)]['data_assets']
county_data = catalog_vol_df[(catalog_vol_df['type'] == 'County') & (catalog_vol_df['dcat_compliant'] == True) & (catalog_vol_df['data_assets'] > 0)]['data_assets']
city_data = catalog_vol_df[(catalog_vol_df['type'] == 'City') & (catalog_vol_df['dcat_compliant'] == True) & (catalog_vol_df['data_assets'] > 0)]['data_assets']
f_val, p_val = stats.f_oneway(federal_data, state_data, county_data, city_data)

## conduct post-hoc tests to determine which groups are different from each other
mc = MultiComparison(catalog_vol_df['data_assets'], catalog_vol_df['type'])
result = mc.tukeyhsd()
print(result)

##### # 4. Value counts of meta data fields within each data catalog
## get counts of the 'metadata' field
catalog_metadata_sizes = listEnhanced[['metavariable_count']]
## generate descriptive statistics, overall
catalog_metadata_sizes.describe()
catalog_metadata_sizes.median()

## generate descriptive statistics by 'type' field: Federal, State, County, City
catalog_metadata_df = listEnhanced[['url', 'type', 'dcat_compliant', 'metavariable_count']]
## keep only where dcat_compliant is True and metavariable_count is greater than 0
catalog_metadata_df = catalog_metadata_df[(catalog_metadata_df['dcat_compliant'] == True) & (catalog_metadata_df['metavariable_count'] > 0)]
catalog_metadata_df.groupby('type')['metavariable_count'].describe() ## group by type and get descriptive statistics

## conduct 1-way ANOVA to test for differences in 'mean' in catalog_metadata_df
federal_metadata = catalog_metadata_df[(catalog_metadata_df['type'] == 'Federal') & (catalog_metadata_df['dcat_compliant'] == True) & (catalog_metadata_df['metavariable_count'] > 0)]['metavariable_count']
state_metadata = catalog_metadata_df[(catalog_metadata_df['type'] == 'State') & (catalog_metadata_df['dcat_compliant'] == True) & (catalog_metadata_df['metavariable_count'] > 0)]['metavariable_count']
county_metadata = catalog_metadata_df[(catalog_metadata_df['type'] == 'County') & (catalog_metadata_df['dcat_compliant'] == True) & (catalog_metadata_df['metavariable_count'] > 0)]['metavariable_count']
city_metadata = catalog_metadata_df[(catalog_metadata_df['type'] == 'City') & (catalog_metadata_df['dcat_compliant'] == True) & (catalog_metadata_df['metavariable_count'] > 0)]['metavariable_count']
f_val, p_val = stats.f_oneway(federal_metadata, state_metadata, county_metadata, city_metadata)
## conduct post-hoc tests to determine which groups are different from each other
mc = MultiComparison(catalog_metadata_df['metavariable_count'], catalog_metadata_df['type'])
result = mc.tukeyhsd()
print(result)


###### # 5. Frequencies of the different themes (without any modification to theme text) - most frequent, least frequent

###### THEMES ############ THEMES ############ THEMES ######
###### THEMES ############ THEMES ############ THEMES ######
###### THEMES ############ THEMES ############ THEMES ######

# Create a list of all the themes
themes = []
results = collection.find({}, {'theme': 1, 'site': 1, 'type': 1, '_id': 0})
for result in results:
    value = result.get('theme', 'No theme found')
    site = result.get('site')
    type_value = result.get('type', 'No type found')  # Assuming a default value for missing 'type'
    output = {
        'site': site,
        'theme': value,
        'type': type_value
    }
    if value != 'No theme found':
        themes.append(output)
    else:
        continue

cleaned_data = [(item['site'], theme, item['type']) for item in themes if isinstance(item['theme'], list) for theme in item['theme']]


themes_df = pd.DataFrame(cleaned_data, columns=['site', 'theme', 'type'])
## calculate total count of themes
total_themes_unique = themes_df.shape[0]
print('Total count of themes: ', total_themes_unique)

themes_df['count'] = 1

## calculate distinct count of themes
distinct_themes = themes_df['theme'].nunique()

## 5a. get counts overall of each unique theme
themes_df_all = themes_df.groupby(['theme']).count().reset_index()
themes_df_all = themes_df_all.sort_values('count', ascending=False)
themes_df_all = themes_df_all[['theme', 'count']]
themes_df_all.head(20)

## 5b. get counts of each unique theme
themes_df_type = themes_df.groupby(['type','theme']).count().reset_index()
themes_df_type = themes_df_type.sort_values('count', ascending=False)
themes_df_type = themes_df_type[['type', 'theme', 'count']]
## generate total count of Federal themes
total_federal_themes = themes_df_type[themes_df_type['type'] == 'Federal']['count'].sum()
## generate total count of State themes
total_state_themes = themes_df_type[themes_df_type['type'] == 'State']['count'].sum()
## generate total count of County themes
total_county_themes = themes_df_type[themes_df_type['type'] == 'County']['count'].sum()
## generate total count of City themes
total_city_themes = themes_df_type[themes_df_type['type'] == 'City']['count'].sum()
## for each row that has a federal theme, calculate the percentage of the total federal themes
themes_df_type['percent'] = themes_df_type.apply(lambda row: (row['count'] / total_federal_themes) * 100 if row['type'] == 'Federal' else ((row['count'] / total_state_themes) * 100 if row['type'] == 'State' else ((row['count'] / total_county_themes) * 100 if row['type'] == 'County' else ((row['count'] / total_city_themes) * 100 if row['type'] == 'City' else 0))), axis=1)
## then create new percent_count column that gives the percentage with 2 decmil places, then has the count in parentheses
themes_df_type['percent_count'] = themes_df_type['percent'].map('{:,.2f}%'.format) + ' (' + themes_df_type['count'].map(str) + ')'

## Get top 10 Federal themes
themes_df_type[themes_df_type['type'] == 'Federal'].head(10)
## Get top 10 State themes
themes_df_type[themes_df_type['type'] == 'State'].head(10)
## Get top 10 County themes
themes_df_type[themes_df_type['type'] == 'County'].head(10)
## Get top 10 City themes
themes_df_type[themes_df_type['type'] == 'City'].head(10)
# themes_df_type.to_csv('data/outputs/analysis/themes.csv', index=False)


###### KEYWORDS ############ KEYWORDS ############ KEYWORDS ######
###### KEYWORDS ############ KEYWORDS ############ KEYWORDS ######
###### KEYWORDS ############ KEYWORDS ############ KEYWORDS ######

# Create a list of all the keywords
keywords = []
results = collection.find({}, {'keyword': 1, 'site': 1, 'type': 1, '_id': 0})
for result in results:
    value = result.get('keyword', 'No keyword found')
    site = result.get('site')
    type_value = result.get('type', 'No type found')  # Assuming a default value for missing 'type'
    output = {
        'site': site,
        'keyword': value,
        'type': type_value
    }
    if value != 'No keyword found':
        keywords.append(output)
    else:
        continue

cleaned_data = [(item['site'], keyword, item['type']) for item in keywords if isinstance(item['keyword'], list) for keyword in item['keyword']]

keywords_df = pd.DataFrame(cleaned_data, columns=['site', 'keyword', 'type'])
## calculate total count of keywords
total_keywords_unique = keywords_df.shape[0]
print('Total unique keywords: ', total_keywords_unique)

keywords_df['count'] = 1

## 6a. get counts overall of each unique keyword
keywords_df_all = keywords_df.groupby(['keyword']).count().reset_index()
keywords_df_all = keywords_df_all.sort_values('type', ascending=False)
keywords_df_all = keywords_df_all[['keyword', 'type']]

## 6b. get counts of each unique keyword
keywords_df_type = keywords_df.groupby(['type','keyword']).count().reset_index()
keywords_df_type = keywords_df_type.sort_values('site', ascending=False)
keywords_df_type = keywords_df_type[['type', 'keyword', 'site']]
# keywords_df_type.to_csv('data/outputs/analysis/keywords.csv', index=False)


###### # 7 Theme translation (transformation) with RegEx, FuzzyWuzzy, and/or other methods

### query mongodb and retrieve the 'theme' field, in addition to type and site
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

## 6a. Caclulate the percentage of themes that were successfully mapped
themes_df_len = len(themes_df_combined)
mapping_success = pd.DataFrame(themes_df_combined['dcat_theme_new'].value_counts())
total_count = mapping_success['count'].sum()
successfully_map_percent = (total_count / themes_df_len) * 100 # about 30% coverage right now

## 6b. Get counts of the newly mapped themes by type
themes_df_combined_type = themes_df_combined.groupby(['type','dcat_theme_new']).count().reset_index()
## keep only type, dcat_theme_new, and theme columns
themes_df_combined_type = themes_df_combined_type[['type', 'dcat_theme_new', 'theme']]
themes_df_combined_type = themes_df_combined_type.rename(columns={'theme': 'count'})
themes_df_combined_type = themes_df_combined_type.sort_values(['type', 'count'], ascending=[True, False]) ## sort by type and count
## generate total count of Federal themes
total_federal_themes = themes_df_combined_type[themes_df_combined_type['type'] == 'Federal']['count'].sum()
## generate total count of State themes
total_state_themes = themes_df_combined_type[themes_df_combined_type['type'] == 'State']['count'].sum()
## generate total count of County themes
total_county_themes = themes_df_combined_type[themes_df_combined_type['type'] == 'County']['count'].sum()
## generate total count of City themes
total_city_themes = themes_df_combined_type[themes_df_combined_type['type'] == 'City']['count'].sum()
## for each row that has a federal theme, calculate the percentage of the total federal themes
themes_df_combined_type['percent'] = themes_df_combined_type.apply(lambda row: (row['count'] / total_federal_themes) * 100 if row['type'] == 'Federal' else ((row['count'] / total_state_themes) * 100 if row['type'] == 'State' else ((row['count'] / total_county_themes) * 100 if row['type'] == 'County' else ((row['count'] / total_city_themes) * 100 if row['type'] == 'City' else 0))), axis=1)

## then create new percent_count column that gives the percentage with 2 decmil places, then has the count in parentheses
themes_df_combined_type['percent_count'] = themes_df_combined_type['percent'].map('{:,.2f}%'.format) + ' (' + themes_df_combined_type['count'].map(str) + ')'

## save to csv
# themes_df_combined_type.to_csv('data/outputs/analysis/themes_mapped.csv', index=False)



###### Look at meta data attribute frequency: listEnhanced : site_keys 
site_keys = listEnhanced[['url', 'dcat_compliant', 'type', 'site_keys', 'data_assets']]
## keep only rows that are dcat_compliant with a non-null site_keys
site_keys = site_keys[(site_keys['dcat_compliant'] == True) & (site_keys['data_assets'] > 0)]
## loop through each value in the list for column site_keys and get a value_count across the 'type' field
# site_keys = site_keys.explode('site_keys')
site_keys = site_keys[['type', 'site_keys']]
site_keys['site_keys'] = site_keys['site_keys'].apply(ast.literal_eval)
site_keys_explode = site_keys.explode('site_keys')
## get a count of each unique site_keys
summary_keys = site_keys_explode['site_keys'].value_counts()
summary_keys = summary_keys.reset_index()
## create a new column that gives the percentage of the total count, dividing count by 256
summary_keys['percent'] = (summary_keys['count'] / 256) * 100


