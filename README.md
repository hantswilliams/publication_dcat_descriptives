# DCAT Descriptives: Code for the U.S. DCAT Descriptives Paper

This repository contains the code for the publication of the U.S. DCAT descriptives paper published in the Journal of Data Intelligence. 

The code is written in Python and uses the pymongo library to connect to the Atlas MongoDB database.

<div>
    <a href="https://www.loom.com/share/5ab2b726f9244ac799c40557f8157225">
      <p>DCAT Publication: Getting Setup to Replicate Code - Watch Video</p>
    </a>
    <a href="https://www.loom.com/share/5ab2b726f9244ac799c40557f8157225">
      <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/5ab2b726f9244ac799c40557f8157225-with-play.gif">
    </a>
  </div>


## About the data and scripts 

The baseline list of DCAT compliant data catalogs is found in data/list_enhanced.csv 

For simplicity, we have already uploaded and parsed the data from each dcat compliant source into MongoDB. The source code for this process is not included in this repository. The purpose of this repository is to provide the code for the analyses in the paper.

There are two main script files included in this analysis that relate to the analyses in the paper:
1. Descriptives: `descriptives.py`
2. Theme translation: `theme_translation.py`

The `analytics/descriptives.py` script contains the code for the analyses in the paper. The script connects to the Atlas MongoDB database and retrieves the data for the analyses. The script generates the results for the analyses in the paper.

The `analytics/theme_translation.py` script contains the code for the theme translation analysis. The script connects to the Atlas MongoDB database and retrieves the data for the theme translation analysis. The script generates the results for the theme translation analysis.

# Replication instructions for analysis: 

## Using Github Spaces: 

### Step 1 - Create a Github Space:
- Create a Github Space
    - Go into the repository and click on the "Code" button, then click on the "Spaces" tab.
    - Click on the "Create a Space" button.

### Step 2 - Create the .env file:
- Add the following files to the space:
    - `.env` file

- Add the following secrets to the space:

```
ATLAS_USERNAME = researcher 
ATLAS_PASSWORD = Dcat2024!!
ATLAS_DB_NAME = Cluster0
```

### Step 3 - Install the python plugin for VS Code:
- Install the Python plugin for VS Code.
    - Go to the extensions tab on the left side of the screen.
    - Search for the Python plugin and install it.

### Step 4 - Open the /analytics/descriptives.py file and test the connection:
- Open the `analytics/descriptives.py` file.
- Highlight the first 17 lines of code, and right click on the highlighted code and select "Run Selection/Line in Python Terminal"; or press `Shift + Enter`.
- The code will connect to the Atlas MongoDB database and retrieve the data for the analyses, you can then highlight `doc_count` and run it to see the number of documents in the collection; or type `doc_count` in the terminal and you should see approximately 142k documents.


## Creating on your own machine: 
### Step 1 - Create a virtual environment:
- Create a virtual environment using the following command:
```
python3 -m venv venv
```
- Activate the virtual environment using the following command:
```
source venv/bin/activate
```
- Install the required libraries using the following command:
```
pip install -r requirements.txt
```

### Step 2 - .ENV file structure:

The results.py script requires a .env file in the root directory with the following structure:

```
ATLAS_USERNAME = researcher 
ATLAS_PASSWORD = Dcat2024!!
ATLAS_DB_NAME = Cluster0
```

To connect to the Atlas MongoDB database, the script uses the pymongo library. The .env file is used to store the credentials for the database connection. The .env file should not be pushed to the repository, as it contains sensitive information.

The provided credentials are read-only credentials to the specific db and cluster. 