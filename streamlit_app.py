import streamlit as st
import snowflake.connector
import requests
import pandas as pd

# Title and intro text
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruit you want in your custom smoothie!")

# Input for smoothie name
name_on_order = st.text_input('Name on Smoothie:')
st.write("The name of your smoothie will be", name_on_order)

# Snowflake connection setup
conn = snowflake.connector.connect(
    user='Vignesh',
    password='Lover_boy_of_life@040602',
    account='IFXMSBO-OW85605',
    warehouse='COMPUTE_WH',
    database='SMOOTHIES',
    schema='PUBLIC'
)
try:
    # Querying available fruits
    query = "SELECT Fruit_Name FROM public.fruit_options"
    df = pd.read_sql(query, conn)

    # Multiselect for ingredients
    ingredients_list = st.multiselect(
        "Choose up to 5 ingredients:", df['Fruit_Name'].tolist(), max_selections=5
    )

    if ingredients_list:
        # Displaying nutrition information
        for fruit in ingredients_list:
            st.subheader(f'{fruit} Nutrition Information')
            response = requests.get(f"https://fruityvice.com/api/fruit/{fruit.lower()}")
            if response.status_code == 200:
                nutrition_info = response.json()
                st.json(nutrition_info)
            else:
                st.error(f"Failed to fetch nutrition info for {fruit}")

        # Prepare SQL insert statement
        ingredients_string = ', '.join(ingredients_list)
        insert_query = f"""
            INSERT INTO public.orders (ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """
        if st.button('Submit Order'):
            with conn.cursor() as cursor:
                cursor.execute(insert_query)
                conn.commit()
                st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")

finally:
    conn.close()
