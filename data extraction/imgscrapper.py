import requests 
from bs4 import BeautifulSoup 
import pandas as pd
# data = [x[:-1] for x in data]
df = pd.read_csv("traindata.csv")
from tqdm import tqdm
def getdata(url): 
    r = requests.get(url) 
    return r.text 
base = "https://www.archanaskitchen.com"
# url = "https://www.archanaskitchen.com/masala-karela-recipe"

img_srcs = []
unpicked_url = []
for url in tqdm(df["URL"]):
    img_lst = []
    try:
        htmldata = getdata(url) 
        soup = BeautifulSoup(htmldata, 'html.parser') 
        for item in soup.find_all('img'):
            # print(item['src'])
            if "image" in item['src'][1:7]:
                img_lst.append(base+item['src'])
    except:
        unpicked_url.append(url)
        continue
    img_srcs.append(img_lst)
print(len(unpicked_url))
df["imgs"] = img_srcs

print(df["URL"].shape)
print(len(img_srcs))
df.to_csv("traindataimgsrc.csv",index =  False)
# https://www.archanaskitchen.com/masala-karela-recipe/images/archanaskitchen/1-Author/Pooja_Thakur/Karela_Masala_Recipe-4_1600.jpg

# https://www.archanaskitchen.com/images/archanaskitchen/1-Author/Pooja_Thakur/Karela_Masala_Recipe-4_1600.jpg
    