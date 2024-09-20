# Import python packages
import streamlit as st
import snowflake.connector
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruit you want in your custom smoothie!
    """
)

# Input for smoothie name
Name_on_Order = st.text_input('Name on Smoothie:')
st.write("The name of your smoothie will be", Name_on_Order)

# Snowflake connection setup
# Replace with your Snowflake credentials or connection method
cnx = snowflake.connector.connect(
    user='Vignesh',
    password='Lover_boy_of_life@040602',
    account='IFXMSBO-OW85605',
    warehouse='COMPUTE_WH',
    database='SMOOTHIES',
    schema='PUBLIC'
)
session = cnx.cursor()

# Querying the available fruit options from the Snowflake table
query = "SELECT Fruit_Name FROM smoothies.public.fruit_options"
session.execute(query)
fruit_data = session.fetchall()
fruit_names = [row[0] for row in fruit_data]  # Extracting fruit names from query result

# Let user select ingredients
ingredients_list = st.multiselect("Choose up to 5 ingredients:", fruit_names, max_selections=5)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)  # Create a string from the list
    
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
    fv_df = st.dataframe(data =fruityvice_response.json(),use_container_width = True )

    st.write(ingredients_string)

    # Prepare SQL insert statement
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{Name_on_Order}')
    """

    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.execute(my_insert_stmt)
        cnx.commit()
        st.success(f"Your Smoothie is ordered, {Name_on_Order}!", icon="✅")

# Close the Snowflake connection
session.close()
cnx.close()



