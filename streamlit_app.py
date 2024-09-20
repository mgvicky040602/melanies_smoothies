import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Set up Streamlit title and instructions
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruit you want in your custom smoothie!")

# User input for the smoothie name
Name_on_Order = st.text_input('Name on Smoothie:')
st.write("The name of your smoothie will be", Name_on_Order)

# Initialize the session
session = get_active_session()

# Retrieve the fruit options
try:
    my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name')).collect()
    fruit_names = [row['Fruit_Name'] for row in my_dataframe]
except Exception as e:
    st.error(f"Failed to retrieve fruit options: {e}")
    fruit_names = []

# Multi-select for ingredients
ingredients_list = st.multiselect("Choose up to 5 ingredients:", fruit_names, max_selections=5)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)
    st.write(ingredients_string)

    # Prepare the insert statement
    my_insert_stmt = f""" 
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{Name_on_Order}')
    """

    st.write(my_insert_stmt)

    # Button to submit the order
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        try:
            session.sql(my_insert_stmt).collect()
            st.success(f"Your Smoothie is ordered, {Name_on_Order}!", icon="✅")
        except Exception as e:
            st.error(f"Failed to submit order: {e}")
