import streamlit
import pandas as pd
import requests

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

fruityvice_response = requests.get("https://www.fruityvice.com/api/fruit/watermelon")
streamlit.text(fruityvice_response.json())