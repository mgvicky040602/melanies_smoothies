# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import pandas as pd
import requests  # Assuming you'll use this for API calls as shown in your screenshot

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruit you want in your custom smoothie!
    """
)

Name_on_Order = st.text_input('Name on Smoothie:')
st.write("The name of your smoothie will be", Name_on_Order)

# Get the active Snowflake session
session = get_active_session()

# Fetch the fruit options with the columns 'FRUIT_NAME' and 'SEARCH_ON'
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

# Convert the Snowpark Dataframe to a Pandas Dataframe
pd_df = my_dataframe.to_pandas()

# Display the dataframe for debugging
st.dataframe(pd_df)

# Let users select ingredients for their smoothie
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    pd_df['FRUIT_NAME'],  # Use the column from the pandas dataframe
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    # Loop through the selected ingredients
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        # Find the corresponding 'SEARCH_ON' value using .loc in Pandas
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write(f"The search value for {fruit_chosen} is {search_on}.")

        # Optionally, call the API for nutrition information
        st.subheader(f"{fruit_chosen} + Nutrition Information")
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_chosen}")
        # You could display the response or handle it accordingly here

    # Adjust the INSERT statement to match column list
    my_insert_stmt = f""" 
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string.strip()}', '{Name_on_Order}')
    """

    st.write(my_insert_stmt)

    # Button to submit the order
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {Name_on_Order}!", icon="✅")
