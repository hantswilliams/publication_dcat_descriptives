# DCAT Descriptives: Code for the U.S. DCAT Descriptives Paper

This repository contains the code for the publication of the U.S. DCAT descriptives paper published in the Journal of Data Intelligence. 

The code is written in Python and uses the pymongo library to connect to the Atlas MongoDB database.

## Notes to self: 
- perhaps have recommended way of running this code, is using a `github space` 
- should perhaps also state the code for cleaning and pulling the data from each DCAT source is not included, that this repo just focuses on the reproducibility of the results in the paper

## Step 1 - Create a virtual environment:
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


## Step 2 - .ENV file structure:

The results.py script requires a .env file in the root directory with the following structure:

```
ATLAS_USERNAME = 
ATLAS_PASSWORD = 
ATLAS_DB_NAME = 
```

To connect to the Atlas MongoDB database, the script uses the pymongo library. The .env file is used to store the credentials for the database connection. The .env file should not be pushed to the repository, as it contains sensitive information.

To get the credentials, please create a issue with the title "Request for MongoDB credentials" and the credentials will be provided to you.