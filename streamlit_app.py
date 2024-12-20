# Import python packages
import streamlit as st
import requests
import pandas as pd
#from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title("Customize Your Smoothie! :cup_with_straw:")
st.write(
    """ Choose the fruits you want in your custom Smoothie!\n
    check out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)
from snowflake.snowpark.functions import col


#Add a Name Box for Smoothie Orders
name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your Smoothie will be: ', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('SEARCH_ON'))
#st.dataframe(data = my_dataframe, use_container_width=True)
#st.stop()

#convert the Snowpark Dataframe to a Pandas dataframe so wer can use the LOC function
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

#Add a Multiselect
ingredients_list = st.multiselect('Choose up 5 ingredients: ', 
                                  my_dataframe,
                                 max_selections = 5)

#Dislay the list 
if ingredients_list:
    
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen +' '
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen, ' is ', search_on, '.')
        
        st.subheader(fruit_chosen + ' Nutrition Information')
        # New section to display smoothifroot nutrition information
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        #st.text(smoothiefroot_response.json()) 
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    #st.write(ingredients_string)
    #Build a SQL Insert Statement & Test It

    my_insert_stmt = """ insert into SMOOTHIES.PUBLIC.ORDERS(ingredients, name_on_order) 
    values ('""" + ingredients_string + """', '""" +name_on_order+ """')"""
    st.write(my_insert_stmt)
    #st.stop()
    #Add a Submit Button
    time_to_insert = st.button('Submit Order')
    
    #Insert the Order into Snowflake
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon ="✅")


    
    





"""
# Get the current credentials
session = get_active_session()

# Use an interactive slider to get user input
hifives_val = st.slider(
    "Number of high-fives in Q3",
    min_value=0,
    max_value=90,
    value=60,
    help="Use this to enter the number of high-fives you gave in Q3",
)

#  Create an example dataframe
#  Note: this is just some dummy data, but you can easily connect to your Snowflake data
#  It is also possible to query data using raw SQL using session.sql() e.g. session.sql("select * from table")
created_dataframe = session.create_dataframe(
    [[50, 25, "Q1"], [20, 35, "Q2"], [hifives_val, 30, "Q3"]],
    schema=["HIGH_FIVES", "FIST_BUMPS", "QUARTER"],
)

# Execute the query and convert it into a Pandas dataframe
queried_data = created_dataframe.to_pandas()

# Create a simple bar chart
# See docs.streamlit.io for more types of charts
st.subheader("Number of high-fives")
st.bar_chart(data=queried_data, x="QUARTER", y="HIGH_FIVES")

st.subheader("Underlying data")
st.dataframe(queried_data, use_container_width=True)

#selectBox
option = st.selectbox(
    "What is your favourite fruits ? ",
    ("Banana", "Strawberries", "Peaches"),
)

st.write("You favorite fruit is :", option)
"""
