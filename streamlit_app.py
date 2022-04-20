import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

### Function(s) to be used later
def get_fruityvice_data(some_fruit_choice):
    fruityvice_response = requests.get("https://www.fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())

    return fruityvice_normalized


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

## Add a stop command to prevent the rest of the code from running while doing testing
streamlit.stop()

# Add connection to Snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

# Option for user to add their own fruit to the list
fruit_to_add = streamlit.text_input("What fruit would you like to add to the list?")
streamlit.write("Thanks for adding", fruit_to_add)

# Code below does not currently work properly
my_cur.execute("INSERT INTO PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST VALUES ('from streamlit')")