import pymongo
from pymongo import MongoClient
import streamlit as st 
import pandas as pd

st.set_page_config(
    page_title='Email Search Page'
)

# MongoDB connection string
db_uri = st.secrets["uri"]
client = MongoClient(db_uri)

# Connect to the specific database and collection
db = client["dbemail"]  
collection = db["email"]  

# Function to load data from MongoDB based on search input
def load_data(search_query):
    if search_query:
        # Using regex to perform a case-insensitive partial match search
        query = {"Email": {"$regex": f".*{search_query}.*", "$options": "i"}}
    else:
        # If no search query, return no data
        query = {}
    
    results = collection.find(query)
    # Convert the MongoDB cursor to DataFrame
    df = pd.DataFrame(list(results))
    if '_id' in df.columns:
        df.drop('_id', axis=1, inplace=True)  # Drop the _id column
    return df

# User input for search
search_variable = st.text_input("Enter text to search in email")

# Load data based on user input
df = load_data(search_variable)

# Display the DataFrame in Streamlit
if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.write("No results found.")
