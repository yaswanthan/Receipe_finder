from msilib import gen_uuid
import streamlit as st
import pandas as pd
import ast
from PIL import Image
import requests 
from bs4 import BeautifulSoup 
from backend import recepie_finder
    
logo = Image.open("img/flogo.png").resize((200, 100))
oops = Image.open("img/oops.png").resize((400, 400))
inf = Image.open("img/inf.png").resize((400, 400))

with open('ing_list.txt', 'r') as f:
    data = f.readlines()
data = [x[:-1] for x in data]
df = pd.read_csv("traindataimgsrcurl.csv")
st.sidebar.image(logo)
menu = st.sidebar.selectbox("Menu",["About Flavourology","Flavourology"],index =0)
cusines = ['North East India Recipes', 'Nepalese', 'Fusion', 'Coastal Karnataka', 'Mediterranean', 'Malvani', 'Cantonese', 'Indonesian', 'Mexican', 'Continental', 'Brunch', 'Gujarati Recipes\ufeff', 'Mughlai', 'Greek', 'Tamil Nadu', 'Italian Recipes', 'Uttar Pradesh', 'Udupi', 'Karnataka', 'Sri Lankan', 'Goan Recipes', 'Assamese', 'Mangalorean', 'Coorg', 'South Karnataka', 'Chinese', 'American', 'Konkan', 'Chettinad', 'Jharkhand', 'Appetizer', 'Andhra', 'Lunch', 'Middle Eastern', 'Jewish', 'Shandong', 'Korean', 'Kerala Recipes', 'Burmese', 'Thai', 'Uttarakhand-North Kumaon', 'Indian', 'Dinner', 'Haryana', 'Punjabi', 'African', 'Kashmiri', 'Parsi Recipes', 'Japanese', 'Vietnamese', 'Asian', 'Caribbean', 'European', 'Maharashtrian Recipes', 'Pakistani', 'Lucknowi', 'Side Dish', 'Afghan', 'Oriya Recipes', 'Sindhi', 'Nagaland', 'Arab', 'Dessert', 'Sichuan', 'World Breakfast', 'Bengali Recipes', 'Hyderabadi', 'Hunan', 'Indo Chinese', 'South Indian Recipes', 'British', 'Malabar', 'Kongunadu', 'Snack', 'North Karnataka', 'Rajasthani', 'Bihari', 'Awadhi', 'Malaysian', 'North Indian Recipes', 'French', 'Himachal']

if menu == "About Flavourology":
    var1 = st.empty()
    var2 = st.empty()
    var3 = st.empty()
    var4 = st.empty()
    var5 = st.empty()
    col1, col2, col3 = var1.columns(3)
    with col1:
        st.write(' ')


    with col2:
        st.image(logo)

    with col3:
        st.write(' ')


    var2.markdown("<h1 style='text-align: center; color: white;'>Welcome to Flavourology </h1>", unsafe_allow_html=True)
    var3.markdown("<h2 style='text-align: center; color: white;'> A recipe has no soul, one must bring soul to the recipe. Go check out for jarring recipes by augmenting the ingredients to cook!</h2>", unsafe_allow_html=True)
    var4.markdown("<h2 style='text-align: center; color: white;'> Developed By</h2>", unsafe_allow_html=True)
    col4,col5 = var5.columns(2)
    with col4:
        st.subheader("Sai Sujay Chilla  160120737048")
    with col5:
        st.subheader("Sai Teja Krithik Putcha  160120737050")
    



if menu == "Flavourology":
    st.title("Flavourology")
    ingrediant = st.sidebar.multiselect('Ingredient',data)
    if len(ingrediant) == 0:
        st.info("Please enter some ingrediants")
    else:
        out = recepie_finder.main(ingrediant)
        if len(out) == 0:
            st.image(oops)
        else:
            cusine = st.sidebar.selectbox('Cusines',out.keys())
            cus_data = df[df["Cuisine"] == cusine]
            cus_data["temp_flag"] = cus_data['Parsed_ing'].apply(lambda ing: 1 if set(ingrediant).issubset(set(ast.literal_eval(ing))) else 0)
            ing_data = cus_data[cus_data["temp_flag"] == 1]
            recipe_list = out[cusine]
            recipe = st.sidebar.selectbox("Receipe's",recipe_list)
            gen = st.sidebar.button('Generate Receipe')
            if gen:
                recipe_data = cus_data[cus_data["TranslatedRecipeName"] == recipe]
                if recipe_data.shape[0] == 0:
                    st.image(oops)
                    st.title("Unable to find any receipes")
                else:
                    img_url = list(recipe_data.img_url)
                    # print(img_url[0])
                    img_src = img_url[0]
                    st.subheader("Recipe Name: {}".format(recipe))
                    if img_src == "404":
                        st.image(inf)
                    else:
                        st.image(img_src)
                    col1,col2 = st.columns(2)
                    prep_time = list(recipe_data["PrepTimeInMins"])
                    cook_time = list(recipe_data["CookTimeInMins"])
                    tot_time = list(recipe_data["TotalTimeInMins"])
                    serv = list(recipe_data["Servings"])
                    col1.text("Preparation Time (in Mins): {}".format(prep_time[0]))
                    col2.text("Cook Time (in Mins): {}".format(cook_time[0]))
                    col3,col4 = st.columns(2)
                    col3.text("Total Time (in Mins): {}".format(tot_time[0]))
                    col4.text("No. of Servings: {}".format(serv[0]))
                    st.subheader("Ingredient's List: ")
                    ing_list = list(set(ast.literal_eval(list(recipe_data["ing_list"])[0])))
                    mid = round(len(ing_list)/2)
                    col5,col6 = st.columns(2)
                    for ing in range(mid):
                        col5.markdown("- {}".format(ing_list[ing]))
                    for ing in range(mid,len(ing_list)):
                        col6.markdown("- {}".format(ing_list[ing]))
                    st.subheader("Instructions: ")
                    instruction = list(recipe_data["TranslatedInstructions"])[0]
                    # print(instruction)
                    # print(instruction.split("."))
                    for instr in instruction.split("."):
                        if len(instr) > 10:
                            st.markdown("- {}.".format(instr))


                




