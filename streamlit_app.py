import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
import requests

# Streamlit app setup
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruit you want in your custom smoothie!
    """
)

# Input for smoothie name
Name_on_Order = st.text_input('Name on Smoothie:')
st.write("The name of your smoothie will be", Name_on_Order)

# Snowflake connection setup using SQLAlchemy
engine = create_engine(URL(
    user='Vignesh',
    password='Lover_boy_of_life@040602',
    account='IFXMSBO-OW85605',
    warehouse='COMPUTE_WH',
    database='SMOOTHIES',
    schema='PUBLIC'
))

# Querying the available fruit options from Snowflake
query = "SELECT Fruit_Name FROM smoothies.public.fruit_options"
df = pd.read_sql(query, engine)

# Confirming the column names for troubleshooting
st.write("Available Columns in DataFrame:", df.columns)

# Check if 'Fruit_Name' is present in the dataframe
if 'FRUIT_NAME' in df.columns:
    fruit_names = df['FRUIT_NAME'].tolist()  # Extracting fruit names from the dataframe
else:
    st.error("Column 'FRUIT_NAME' not found in the table.")
    st.stop()  # Stop the app if the column is missing

# Let user select ingredients
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:", 
    fruit_names, 
    max_selections=5
)

# Processing the selected ingredients
if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)  # Create a string from the list
    
    # Display Nutrition Information for each selected ingredient
    for fruit_chosen in ingredients_list:
        st.subheader(f'{fruit_chosen} Nutrition Information')

        # Attempt to find the fruit in the dataframe
        try:
            search_on = df.loc[df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
            st.write(f'The search value for {fruit_chosen} is {search_on}')
        except IndexError:
            st.write(f'No data found for {fruit_chosen}')

        # Fetching nutrition information for the selected fruit
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_chosen.lower()}")
        if fruityvice_response.status_code == 200:
            fv_data = fruityvice_response.json()
            st.json(fv_data)
        else:
            st.error(f"Could not fetch nutrition info for {fruit_chosen}")
    
    st.write(f"Selected ingredients: {ingredients_string}")

    # Prepare SQL insert statement
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{Name_on_Order}')
    """

    st.write("SQL Query to be executed:")
    st.write(my_insert_stmt)

    # Button to submit the order
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        # Execute the insert statement using SQLAlchemy engine
        with engine.connect() as conn:
            conn.execute(my_insert_stmt)
            st.success(f"Your Smoothie is ordered, {Name_on_Order}!", icon="✅")

# Close the Snowflake connection (SQLAlchemy handles this automatically)
