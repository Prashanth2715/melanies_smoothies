# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want to add in your smoothie!
    """
)



name_on_order=st.text_input("Name On the Smoothie:")
cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe=session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('search_on'))
#st.dataframe(my_dataframe,use_container_width=True)
pd_df=my_dataframe.to_pandas()


ingredients_list = st.multiselect(
    "You can choose any 5 fruits",my_dataframe,max_selections=5)


if ingredients_list and name_on_order:
    ingredients=''
    for i in ingredients_list:
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == i, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', i,' is ', search_on, '.')
        ingredients+=i+" "
        fruitvice_response=requests.get("https://fruityvice.com/api/fruit/"+search_on)
        st.write(i+'Nutrition Value')
        fv_df=st.dataframe(fruitvice_response.json(),use_container_width=True)
    st.write(ingredients)
    insert_stmt="""insert into smoothies.public.orders(ingredients,name_on_order) values ('"""+ingredients+"""','"""+name_on_order+"""')"""
    submit_order=st.button('Submit Order')
    
    if submit_order:
        session.sql(insert_stmt).collect()
        st.success('Smoothie Ordered '+name_on_order,icon="✅")
        
        


