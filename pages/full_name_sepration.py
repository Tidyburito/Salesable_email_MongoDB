# import pymongo
# from pymongo import MongoClient
# import streamlit as st
# import pandas as pd

# # st.set_page_config(
# #     page_title='Email Search Page'
# # )

# # MongoDB connection string
# db_uri2 = st.secrets["uri"]
# client = MongoClient(db_uri2)

# # Connect to the specific database and collection
# db = client["dbemail"]
# collection = db["contact"]

# # Function to load data from MongoDB based on search input
# def load_data(search_query):
#     if search_query:
#         # Using regex to perform a case-insensitive partial match search across multiple fields
#         query = {"$or": [
#             {"First Name": {"$regex": f"{search_query}", "$options": "i"}},
#             {"Last Name": {"$regex": f"{search_query}", "$options": "i"}},
#             {"Website": {"$regex": f"{search_query}", "$options": "i"}},
#             {"Account Name": {"$regex": f"{search_query}", "$options": "i"}}
#         ]}
#     else:
#         # If no search query, return no data
#         query = {}
    
#     results = collection.find(query, {"_id": 0})  # Exclude the '_id' field from the results
#     # Convert the MongoDB cursor to DataFrame
#     df = pd.DataFrame(list(results))
#     return df

# # User input for search
# search_variable = st.text_input("Enter text to search in contacts")

# # Load data based on user input
# df = load_data(search_variable)

# # Display the DataFrame in Streamlit
# if not df.empty:
#     st.dataframe(df, use_container_width=True)
# else:
#     st.write("No results found.")



import pymongo
from pymongo import MongoClient
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title='Detailed Email Search Page'
)

# MongoDB connection string
db_uri = st.secrets["uri"]
client = MongoClient(db_uri)

# Connect to the specific database and collection
db = client["dbemail"]
collection = db["contact"]

def load_data(search_query):
    # This dictionary will hold data frames for each field
    data_frames = {}
    
    fields = ["First Name", "Last Name", "Website", "Account Name"]
    for field in fields:
        if search_query:
            # Case-insensitive partial match search for each field
            query = {field: {"$regex": f"{search_query}", "$options": "i"}}
        else:
            query = {}
        
        results = collection.find(query, {"_id": 0})
        df = pd.DataFrame(list(results))
        if not df.empty:
            data_frames[field] = df

    return data_frames

# User input for search
search_variable = st.text_input("Enter text to search in contacts")

# Load data based on user input
data_frames = load_data(search_variable)

# Display each DataFrame in Streamlit
if data_frames:
    for field, df in data_frames.items():
        st.subheader(f'Matches in {field}')
        st.dataframe(df, use_container_width=True)
else:
    st.write("No results found.")
