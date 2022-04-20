import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError



# Function(s) to be used later
def get_fruityvice_data(some_fruit_choice):
    """
    Function that retrieves data about a user-specified fruit from the Fruityvice API.
    """

    fruityvice_response = requests.get("https://www.fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())

    return fruityvice_normalized


def get_fruit_load_list():
    """
    Function that loads the "FRUIT_LOAD_LIST" table from Snowflake.
    """

    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
        return my_cur.fetchall()


def insert_fruit_into_snowflake(new_fruit):
    """
    Function that insert a new fruit (entered by user) into the "FRUIT_LOAD_LIST" table in Snowflake.
    """

    with my_cnx.cursor() as my_cur:
        my_cur.execute(f"INSERT INTO PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST VALUES ('{new_fruit}')")
        return "Thanks for adding " + new_fruit



# Initiate titles and text for the web app
streamlit.title("My Parents' New Healthy Diner")

streamlit.header("Breakfast Favorites")
streamlit.text("🥣 Omega 3 & Blueberry Oatmeal")
streamlit.text("🥗 Kale, Spinach & Rocket Smoothie")
streamlit.text("🐔 Hard-Boiled Free-Range Egg")
streamlit.text("🥑🍞 Avocado Toast")

streamlit.header("🍌🥭 Build Your Own Fruit Smoothie 🥝🍇")

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")



# Add list to allow users to pick the fruits they want in their smoothies
fruits_selected = streamlit.multiselect(label = "Pick some fruit:", 
                                        options = list(my_fruit_list.index),
                                        default = ["Avocado", "Strawberries"])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display table of fruit
streamlit.dataframe(fruits_to_show)



# Try-Except for the fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
    # Get Fruityvice API response
    fruit_choice = streamlit.text_input("What fruit would you like information about?")
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        # Get and normalize response from fruityvice API
        fruityvice_func_output = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(fruityvice_func_output)

except URLError as e:
    streamlit.error()



# Add button for loading fruit from Snowflake
streamlit.header("View Our Fruit List & Add Your Favorites!")
if streamlit.button("Get Fruit List"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)
    my_cnx.close()

# Option for user to add their own fruit to the list
fruit_to_add = streamlit.text_input("What fruit would you like to add to the list?")
if streamlit.button("Add Fruit To List"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    output_insert_fruit_into_snowflake = insert_fruit_into_snowflake(fruit_to_add)
    streamlit.write(output_insert_fruit_into_snowflake)
    my_cnx.close()
