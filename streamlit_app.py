import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
streamlit.title('My Mom''s New Healthy Diner')

streamlit.header('Breakfast Favorites - :first_quarter_moon_with_face:')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥬 Kale, Spinach and Rocket Smoothie')
streamlit.text('🥚 Hard-boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.text('Bacon, Eggs and Hashbrowns')

streamlit.header('🍌🍓 Build Your Own Fruit Smoothie 🫐🍍')
fruits_selected = streamlit.multiselect('Pick some fruits:', list(my_fruit_list.index),[])
streamlit.error("Please select a fruit to get information.")
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
  
  fruit_choice = streamlit.text_input('What fruit would you like information about?')

  if not fruit_choice:
    streamlit.error('Please select a fruit to get information.')
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()

streamlit.header("The fruit load list contains:")

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
      my_cur.execute("select * from fruit_load_list")
  return my_cur.fetchall()

if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
  return "Thanks for adding " + new_fruit


fruit_add = streamlit.text_input('What fruit would you like to add?','jackfruit')
if streamlit.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(fruit_add)
  my_cnx.close()
  streamlit.text(back_from_function)


