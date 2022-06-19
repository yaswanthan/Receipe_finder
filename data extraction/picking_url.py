import pandas as pd
import ast

data = pd.read_csv("traindataimgsrc.csv")

imagesurl = list(data.imgs)
from tqdm import tqdm
images = []
patterns =[]
for urls in tqdm(imagesurl):

    noicon = [url for url in ast.literal_eval(urls) if "icon" not in str(url)]
    nouser = [url for url in noicon if "userprofiles" not in str(url)]
    nopopup = [url for url in nouser if "popup" not in str(url)]
    if len(nopopup) == 1:
        images.append(nopopup[0])
    elif len(nopopup) >1:
        images.append(nopopup[len(nopopup)-1])
    else:
        images.append('404')

data["img_url"] = images
data.to_csv("traindataimgsrcurl.csv",index=False)
