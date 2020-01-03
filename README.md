# Scopus API Requests Repository
repository of python code for making API requests for the Elsevier Scopus API

## What is the Scopus API Requests Repository

The Scopus API Requests Repository is a code base for my own work in Scopus. The repository has two main files of code: 

1. SingleAuthorAPIRequests.ipynb
This file demonstrates how to make a request for articles by a single author using the Scopus API. 

2. MultipleAuthorAPIRequests.ipynb or MultipleAuthorAPIRequests.py
These files demonstrate how to make a request for articles by mulitple authors using the Scopus API. Further more, the code creates a final CSV (called merged_df) that contains a list of articles for each author, which can help with creating final publication lists. 

## How to use this repository

For the very beginners, let's start at the beginning. 
1. Download Python 3 (or higher). <https://www.anaconda.com/distribution/>
2. Install Jupyter Notebook. <https://jupyter.readthedocs.io/en/latest/install.html>
3. See instructions for running Jupyter Notebook. <https://jupyter.readthedocs.io/en/latest/running.html#running>
4. Register for a Scopus API through your academic institution. <https://dev.elsevier.com/>
5. Fork this repository. <https://help.github.com/en/github/getting-started-with-github/fork-a-repo>
6. Make a config.py file to hold your API key. Consider installing Visual Studio Code <https://code.visualstudio.com/>. In Visual Studio Code, open the same folder in which you've saved this repository, make a new file called: config.py . In the config.py file type: api_key = "YOURKEYBETWEENTHESEQUOTES" and save the file. This api_key variable is imported at the top of the Jupyter Notebook file (see: Dependencies: from config import api_key). 
7. Make a CSV that has two columns (at least) called: author_name, scopus_author_id . Save this CSV file in the same folder in which you've saved the this repository. 
8. Open the "MultipleAuthorAPIRequests.ipynb" file in a jupyter notebook.  
9. In the cell containing the function called "def load_csv_auhtor_ids" change the file_path value to where your file lives, such as: file_path = "YOURFILENAMEHERE.csv" if the file lives in the same folder as the "MultipleAuthorAPIRequests.ipynb" jupyter notebook. 
10. In the cell containing the function called "def export_to_csv(merged_df, save_path)" change the save_path value to where you want the final CSV to live, such as: save_path = "save_path = "C:\\Users\\karen\\Documents\\scopusAPIrequests\\merged_dataframe_final.csv" . The double backslashes are needed so that python doesn't interpret them as special characters. 
11. Run all the cells in the Jupyter Notebook!

If you prefer not using Jupyter Notebooks, then consider using the "MultipleAuthorAPIRequests.py" file instead. 

## What is the output of this repository?

The final CSV contains a list of each author and their publications. Below are the columns you can expect to see. 

The final CSV has these columns from your original CSV:
author_name	
scopus_author_id	

The final dataframe has these columns from the Scopus API (some you may not need):
See the Scopus documentation for more information <https://dev.elsevier.com/guides/ScopusSearchViews.htm>
@_fa
author
citedby-count	
dc:identifier	
dc:title	
eid	
error	
prism:aggregationType	
prism:coverDate	
prism:doi	
prism:issueIdentifier	
prism:pageRange	
prism:publicationName	
prism:url	
prism:volume	
pubmed-id	
subtype	
subtypeDescription	
opensearch:totalResults	
opensearch:startIndex	
opensearch:itemsPerPage	
link	
entry	
@role	
@searchTerms	
@startPage	
author_names	
author_ids	
scopus_author_id_api				


