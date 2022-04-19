import streamlit
import pandas as pd

streamlit.title("My Parents' New Healthy Diner")

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')



streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")

# Add list to allow users to pick the fruits they want in their smoothies
streamlit.multiselect(label = "Pick some fruit:", 
                      options = list(my_fruit_list.index),
                      default = ["Avocado", "Strawberries"])

# Display table of fruit
streamlit.dataframe(my_fruit_list)
