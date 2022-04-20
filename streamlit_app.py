import streamlit
import pandas as pd
import requests
import snowflake.connector

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

# Get Fruityvice API response
streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input("What fruit would you like information about?", "Kiwi")
streamlit.write("The user entered", fruit_choice)

fruityvice_response = requests.get("https://www.fruityvice.com/api/fruit/" + fruit_choice)

# Normalize the API response
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)

# Add connection to Snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)