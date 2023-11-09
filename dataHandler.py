import pandas as pd
import os

def get_data():
    current_directory = os.getcwd()
    file_path= os.path.join(current_directory, 'data.csv')
    df= None
    if df==None:
        df= pd.read_csv(file_path)
    return df