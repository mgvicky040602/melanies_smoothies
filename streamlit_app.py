# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruit you want in your custom smoothie!
    """
)

# Text input for smoothie name
Name_on_Order = st.text_input('Name on Smoothie:')
st.write("The name of your smoothie will be", Name_on_Order)

# Get the Snowflake connection session (using st.connection as per your version)
try:
    cnx = st.connection("snowflake")
    session = cnx.session
    
    # Query the fruit options table
    my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name')).collect()

    # Extract the fruit names into a list
    fruit_names = [row['Fruit_Name'] for row in my_dataframe]

    # Multiselect for ingredients with a max of 5 selections
    ingredients_list = st.multiselect("Choose up to 5 ingredients: ", fruit_names, max_selections=5)
    
    if ingredients_list:
        # Join the selected ingredients into a string
        ingredients_string = ', '.join(ingredients_list)
        
        # Display the selected ingredients
        st.write("Your selected ingredients: ", ingredients_string)
        
        # SQL statement to insert the order into the 'orders' table
        my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders (ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{Name_on_Order}')
        """
        
        # Display the SQL query for review
        st.write("SQL Query to be executed: ", my_insert_stmt)
        
        # Button to submit the order
        time_to_insert = st.button('Submit Order')
        
        if time_to_insert:
            # Execute the SQL insert statement
            session.sql(my_insert_stmt).collect()
            st.success(f"Your Smoothie is ordered, {Name_on_Order}!", icon="✅")
except Exception as e:
    st.error(f"Error querying the database: {e}")
