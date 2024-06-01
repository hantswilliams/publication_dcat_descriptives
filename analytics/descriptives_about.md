# Analyses for Paper 1

## 0. Value counts of compliant and non-compliant records
- Show the counts of 'dcat_compliant' field
- Create a pivot by 'type' field: Federal, State, County, City

## 1. Value counts of the different URLs (unique)
- Count the occurrences of each unique URL

## 2. Value counts of the different types (unique)
- Count the occurrences of each unique 'type'

## 3. Value counts of data volume within each data catalog
- Generate overall descriptive statistics
- Generate descriptives by 'type' field: Federal, State, County, City
- Perform 1-way ANOVA to test for differences in data volume by 'type' field

## 4. Value counts of metadata fields within each data catalog
- Generate overall descriptive statistics
- Generate descriptives by 'type' field: Federal, State, County, City
- Perform 1-way ANOVA to test for differences in metadata volume by 'type' field

## 5. Frequencies of the different themes
- Calculate the total count of themes
- Generate overall counts of each unique theme
- Generate counts of each unique theme by 'type'

## 6. Frequencies of the different keywords
- Calculate the total count of keywords
- Generate overall counts of each unique keyword
- Generate counts of each unique keyword by 'type'

## 7. Theme translation (transformation) anlysis
- Translate themes using specified methods
    - Note: theme translation is done as a separate process, which can be found in the `theme_translation.py` script in the analytics folder
- Perform frequency analysis on translated themes
- Calculate the percentage of themes successfully mapped
- Generate counts of the newly mapped themes by 'type'

## 8. Meta data attribute frequency
- Calculate the frequency of meta data attributes
- Generate summary statistics for meta data attributes
