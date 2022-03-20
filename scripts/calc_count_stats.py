'''
Takes in dataframe with _embedded dictionary with information on tags and categories.

Generates a dataframe with tags/categories with their id, name and counts for further analysis
'''

from ast import literal_eval
import pandas as pd
from collections import Counter



def generate(df, index):
    
    # calculate how often a tag or category appears in the articles
    # first column in a df is a column with tags or categories
    input = df.iloc[:, 0].fillna('[]').tolist()
    flat_input =  [item for sublist in  input  for item in literal_eval(sublist)]
    counts_df = pd.DataFrame(dict(Counter(flat_input)).items(), columns = [ 'id', 'counts'])
    
    def get_values(string):
        '''
        This function returns a list of dictionaries with all possible techcrunch categories
        '''
        # add check if there are no tags/categories, i.e. list index out of range
        data = literal_eval(string)['wp:term'][index]  if len(literal_eval(string)['wp:term']) > 1 else []
    
        # keys that we need from categories
        keys = ['id', 'name', 'slug']
   
         # all categories/tags

        result = [ {x: cat[x] for x in keys}  for cat in data]
    
        return result


    list_values = df['_embedded'].apply(get_values)
    new_values_df = list_values.explode().drop_duplicates().apply(pd.Series)

    # merge dataframe with id names and id counts

    values = pd.merge( new_values_df,  counts_df, on="id")

    return values
    
    


     






