# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session

from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruit you want in your custom smoothie!
    """
)




Name_on_Order = st.text_input('Name on Smoothie:')
st.write("The name of your smoothie will be", Name_on_Order)


#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'))
#st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect("Choose upto 5 ingrediants: ",my_dataframe,max_selections =5)

if ingredients_list:
    
    ingredients_string = ' '.join(ingredients_list)  # Use join for a cleaner approach

    st.write(ingredients_string)

    # Adjust the INSERT statement to match column list
    my_insert_stmt = f""" 
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{Name_on_Order}')
    """

    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {Name_on_Order}!", icon="✅")



    


