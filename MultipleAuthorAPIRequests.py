# Dependencies
import requests
import json
import pandas as pd
import numpy as np
import re
import io
from config import api_key
from collections import OrderedDict
from pandas.io.json import json_normalize  

#The function "load_csv_author_ids" loads a CSV you have created that has columns called: last_name, scopus_author_id.
#This CSV may also contain other information helpful to your work. The function returns a pandas data frame called 
#"multiple_authors_df".

file_path = "radiation_oncology.csv"

def load_csv_author_ids(file_path):
    # File to Load
    multiple_authors_df = file_path

    # Read the CSV file and store into Pandas DataFrame with the column Scopus Author ID as a string
    multiple_authors_df = pd.read_csv(multiple_authors_df, encoding="utf-8", dtype ={'scopus_author_id': str})

    #Change the column names to lower case with underscore for spaces
    multiple_authors_df.columns =  multiple_authors_df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("(","").str.replace(")","")
    #radiation_oncology_df.head()
    return multiple_authors_df

multiple_authors_df = load_csv_author_ids(file_path)
load_csv_author_ids(file_path)

#The function "clean_author_id_list" takes in the multiple_authors_df and formats the "scopus_author_id" column 
#as a string, then uses the column to create a list, removes any of the "nan" values for authors that don't 
#have an ID, and finally returns a list called "cleaned_author_id_list"

def clean_author_id_list(multiple_authors_df):
    
    #Change the data type in the dataframe column called "scopus_author_id" from int64 to a string. 
    multiple_authors_df['scopus_author_id'] = multiple_authors_df['scopus_author_id'].astype(str)

    #Save the column called scopus_author_id to a list called Author_ID_List
    author_id_list = multiple_authors_df['scopus_author_id'].tolist()
    #print(author_ID_List)
    
    #Clean the Author_ID_List to remove nan
    cleaned_author_id_list = [x for x in author_id_list if str(x) != 'nan']
    #print(cleaned_author_id_list)
        
    return cleaned_author_id_list

cleaned_author_id_list = clean_author_id_list(multiple_authors_df)
clean_author_id_list(multiple_authors_df)

#The function "create_multiple_author_id_query" takes in the "cleaned_author_id_list" and adds the necessary syntax of
# "AU-ID(xxxxxxxxx)" that is required for searching Scopus Author IDs. The function returns 
#the "scopous_multiple_author_id_query".

def create_multiple_author_id_query(cleaned_author_id_list):

    #Add the necessary syntax to the cleaned_Author_ID_List
    scopus_mulitple_author_id_query = []
    for x in cleaned_author_id_list:
        authorID_string = "".join(("AU-ID(", x,")"))
        #print(authorID_string)
        scopus_mulitple_author_id_query.append(authorID_string)

    #print(scopus_mulitple_author_id_query)
    return scopus_mulitple_author_id_query

scopus_mulitple_author_id_query = create_multiple_author_id_query(cleaned_author_id_list)
create_multiple_author_id_query(cleaned_author_id_list)

#The function "get_scopus_articles" takes in the "scopus_multiple_author_id_query" and creates a necessary URL 
#for querying the Scopus API. The Scopus API key is passed in through the "headers" (see above Dependencies 
#"from config import api_key") and the config file is also referenced in the git ignore so it won't be exposed 
#on Github. The API is called and returns a response for each Scopus Author ID in the list Each response is 
#saved in a "single_author_article_dict". Each of the "single_author_article_dict" are then appended to the 
#"multiple_author_article_list". The function returns a list of dictionaries called 
#the "multiple_author_article_list". 

multiple_author_article_list = []
#multiple_author_article_dict = {}
single_author_article_dict = {}
date = "2002-2003"

def get_scopus_articles(scopus_mulitple_author_id_query):
    
    for authorid in scopus_mulitple_author_id_query:
        url = "http://api.elsevier.com/content/search/scopus?"
        fieldList = ["dc:identifier", "eid", "dc:title","prism:aggregationType", "subtype", "citedby-count",
                     "prism:publicationName","prism:volume","prism:issueIdentifier", "prism:pageRange", 
                     "prism:coverDate", "prism:doi","pubmed-id", "authid", "authname"]
                    
        headers = {
             "X-ELS-APIKey": api_key,
             'Accept':'application/json'
        }
        parameters = {
            "query": authorid,
            "field": ",".join(fieldList),
            "date": date
        }
        
        #Make the API request 
        single_author_article_response = requests.get(url, headers=headers, params=parameters)
        #print(single_author_article_response.url)
        #print(single_author_article_response.status_code)
        
              
        #Append each single_author_article_dict response to multiple_author_article_list to create a list of dictionaries
        single_author_article_dict = single_author_article_response.json()
        #print(type(single_author_article_dict)) 
        #print(single_author_article_dict)
        multiple_author_article_list.append(single_author_article_dict.copy())
    
    return multiple_author_article_list
       
get_scopus_articles(scopus_mulitple_author_id_query)

#References
#https://dev.elsevier.com/guides/ScopusSearchViews.htm
#https://stackoverflow.com/questions/53558837/python-loop-to-pull-api-data-for-iterating-urls
#https://stackoverflow.com/questions/36410800/python-3-parse-json-from-multiple-api-requests-into-a-list-and-output-to-a-fil
#https://www.pluralsight.com/guides/web-scraping-with-request-python

#The function "make_scopus_articles_df" takes in the "multiple_author_article_list" and uses json_normalize to
#flatten the json contained in the "entry" field. The function returns a dataframe called the "scopus_articles_df".

def make_scopus_articles_df(multiple_author_article_list):
    #final_list = json_normalize(multiple_author_list, meta=["search-results"], record_path=["search-results", "entry"])
    scopus_articles_df = pd.DataFrame.from_dict(json_normalize(multiple_author_article_list, meta=["search-results"], record_path=["search-results", "entry"]),orient="columns")
    
    return scopus_articles_df

scopus_articles_df = make_scopus_articles_df(multiple_author_article_list)
make_scopus_articles_df(multiple_author_article_list)

#References
#https://stackoverflow.com/questions/48177934/flatten-or-unpack-list-of-nested-dicts-in-dataframe
#https://stackoverflow.com/questions/50161070/convert-list-of-dicts-of-dict-into-dataframe
#https://stackoverflow.com/questions/43984865/python-having-trouble-returning-a-pandas-data-frame-from-a-user-defined-functio
#https://stackoverflow.com/questions/37668291/flatten-double-nested-json

#The function "flatten_search_results" takes in the "scopus_articles_df" and flattens the json contained in the
#"search results" field and creates series then columns of the content. The funciton returns a pandas dataframe
#called "remove_opensearchQuery_nest" which is renamed "scopus_flattened_search_results_df". 

def flatten_search_results(scopus_articles_df):
    remove_searchresults_nest = pd.concat([scopus_articles_df.drop(['search-results'], axis=1), scopus_articles_df['search-results'].apply(pd.Series)], axis=1, join="outer")
    remove_opensearchQuery_nest = pd.concat([remove_searchresults_nest.drop(['opensearch:Query'], axis=1), remove_searchresults_nest['opensearch:Query'].apply(pd.Series)], axis=1, join="outer")
    remove_opensearchQuery_nest = pd.concat([remove_searchresults_nest.drop(['opensearch:Query'], axis=1), remove_searchresults_nest['opensearch:Query'].apply(pd.Series)], axis=1, join="outer")
    return remove_opensearchQuery_nest

scopus_flatten_search_results_df = flatten_search_results(scopus_articles_df)
flatten_search_results(scopus_articles_df)

#References
#https://stackoverflow.com/questions/29325458/dictionary-column-in-pandas-dataframe/29330853

#The function "fix_empty_author" takes in the "scopus_flattened_search_results_df" and uses a for loop
# to add an empty list to any column in the "author" column that is empty (i.e. contains nan). The function
#returns a pandas dataframe called the "scopus_flattened_search_results_df" which is renamed 
#to "scopus_fix_empty_author_df". 

def fix_empty_author(scopus_flatten_search_results_df):

    for row in scopus_flatten_search_results_df.loc[scopus_flatten_search_results_df.author.isnull(), 'author'].index:
        scopus_flatten_search_results_df.at[row, 'author'] = []
    
    return scopus_flatten_search_results_df

scopus_fix_empty_author_df = fix_empty_author(scopus_flatten_search_results_df)
fix_empty_author(scopus_flatten_search_results_df)

#The function "flatten_author" takes in the "scopus_fix_empty_author_df" and loops through the "author" column which 
#is currently a list of dictionaries which contain the authname and authid for each author listed on the article. 
#The function loops through each item in the cell of the "author" column, saves each of the authids to a list and 
#each of the the authnames to a list. The funciton then appends the authid list to an ordered dicitonary 
#called "authorid_dict" and the authname list to an ordered dictionary called "authname_dict". Once appended, the 
#function empties the lists and moves on to the next cell in the "author" column. The function
#returns the authid and authname dictionaries. 

authorid_dict = OrderedDict()
authorname_dict = OrderedDict() 

def flatten_author(scopus_fix_empty_author_df):
    authorids = []
    #authorid_dict = OrderedDict()
    authornames = []
    #authorname_dict= OrderedDict() 
    for i in range(len(scopus_fix_empty_author_df)):
        #print(scopus_fix_empty_author_df.loc[i, "author"]) 
        column = scopus_fix_empty_author_df.loc[i, "author"]
        #print(i)
        #print(column)

        for item in column:
            #print(item)
            #print(item["authid"])
            #print(column)
            authorids.append(item["authid"])
            authornames.append(item["authname"])
            #print(authorids)
         
        #print(i)
        authorid_dict[i] = authorids
        authorname_dict[i]= authornames
        authorids=[]
        authornames=[]
        
    return authorid_dict, authorname_dict

#print(authorid_dict)
#print(authorname_dict)
flatten_author(scopus_fix_empty_author_df)

#The "add_author_info" function takes in the "scopus_fix_empty_author_df", the "authorname_dict" 
#and the "authorid_dict". It creates two new columns in the dataframe called "author_names" and "author_ids". 
#The function adds the "authorname_dict" and the "authorid_dict" to the columns. The function returns
#the "scopus_fix_empty_author_df" which is renamed to the "scopus_added_author_info_df". 

def add_author_info(scopus_fix_empty_author_df, authorname_dict, authorid_dict):
    scopus_fix_empty_author_df["author_names"] = pd.Series(authorname_dict)
    scopus_fix_empty_author_df["author_ids"] = pd.Series(authorid_dict)
    return scopus_fix_empty_author_df

scopus_added_author_info_df = add_author_info(scopus_fix_empty_author_df, authorname_dict, authorid_dict)
add_author_info(scopus_fix_empty_author_df, authorname_dict, authorid_dict)

#The function "fix_search_term" takes in the "scopus_add_author_info_df" and creates a new column 
#called "scopus_author_id_api" which contains the same data as the "@searchTerms" column. 
#The funciton then uses regex to remove everything around the parenthesis and leave
#what was in between the parentesis in the "scopus_author_id_api" column. The function returns
#the "scopus_fix_empty_author_df" which is renamed to the "scopus_fixed_search_term_df"

def fix_search_term(scopus_added_author_info_df):
    scopus_added_author_info_df['scopus_author_id_api'] = scopus_added_author_info_df['@searchTerms']
    scopus_added_author_info_df["scopus_author_id_api"].replace(r'[^(]*\(|\)[^)]*', '', inplace=True,regex=True)
    return scopus_fix_empty_author_df

scopus_fixed_search_term_df = fix_search_term(scopus_added_author_info_df)
fix_search_term(scopus_added_author_info_df)

#References
#https://stackoverflow.com/questions/32913960/python-regex-remove-a-pattern-at-the-end-of-string
#https://stackoverflow.com/questions/16842001/copy-text-between-parentheses-in-pandas-dataframe-column-into-another-column
#https://stackoverflow.com/questions/37593550/pandas-replacing-elements-not-working

#The function "merge_csv_to_final" takes in the "muliple_authors_df" and the "scopus_fixed_search_term_df" and
#merges the two dataframes using an "inner" merge on the "scopus author id" which means any person without a 
# Scopus Author ID is removed from the final dataframe. The function returns the "merged_df". 

def merge_csv_to_final(multiple_authors_df, scopus_fixed_search_term_df):
    merged_df = pd.merge(multiple_authors_df, scopus_fixed_search_term_df, how='inner', left_on='scopus_author_id', right_on='scopus_author_id_api',  )    
    return merged_df

merged_df = merge_csv_to_final(multiple_authors_df, scopus_fixed_search_term_df)
merge_csv_to_final(multiple_authors_df, scopus_fixed_search_term_df)

#References
#https://stackoverflow.com/questions/20375561/joining-pandas-dataframes-by-column-names

#The function "export_to_csv" takes in the merged_df, and a save_path which indicates where the merged_df
#will be saved. Use double back slashes in the save path to escape the backslash or otherwise it will be
#interpreted as a special character and won't work. The function does not return anything. 

save_path = "C:\\Users\\keg827\\Documents\\10. WorkStuff_KEG\\scopusAPIrequests\\merged_dataframe_final_final.csv"

def export_to_csv(merged_df, save_path):
    merged_df.to_csv (save_path, index = None, header=True, encoding="utf-8")
    

export_to_csv(merged_df, save_path)

