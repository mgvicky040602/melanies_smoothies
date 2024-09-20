# Import python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruit you want in your custom smoothie!
    """
)

# Input for the name of the smoothie
Name_on_Order = st.text_input('Name on Smoothie:')
st.write("The name of your smoothie will be", Name_on_Order)

# Manual Snowflake connection setup (replace with your actual connection details)
connection_parameters = {
    account: "IFXMSBO-OW85605",
    user: "Vignesh",
    password: "Lover_boy_of_life@040602",
    role: "SYSADMIN",
    warehouse: "COMPUTE_WH",
    database: "smoothies",
    schema: "public"
}

try:
    session = Session.builder.configs(connection_parameters).create()

    # Fetch the available fruits
    my_dataframe = session.table("fruit_options").select(col('Fruit_Name')).collect()
    fruit_options = [row.Fruit_Name for row in my_dataframe]  # Extract fruit names

except Exception as e:
    st.error(f"Error connecting to Snowflake: {e}")
    fruit_options = []

# Multiselect input for ingredients
ingredients_list = st.multiselect("Choose up to 5 ingredients: ", fruit_options, max_selections=5)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)  # Clean up list of ingredients for insertion
    st.write(ingredients_string)

    # Prepare the SQL insert statement
    my_insert_stmt = f""" 
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{Name_on_Order}')
    """

    st.write(my_insert_stmt)

    # Button to submit order
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        try:
            session.sql(my_insert_stmt).collect()
            st.success(f"Your Smoothie is ordered, {Name_on_Order}!", icon="✅")
        except Exception as e:
            st.error(f"Error inserting order: {e}")
