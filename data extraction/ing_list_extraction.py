import pandas as pd
from tqdm import tqdm
import ast
data = pd.read_csv("./backend/data.csv")

parsed = data.ingredients


print(parsed.head())

print(parsed.shape)
print(parsed.shape[0])

m_cus = []
cusine = data.cuisine
for i in tqdm(range(cusine.shape[0])):
    for cus in cusine:
        m_cus.append(cus)

print(list(set(m_cus)))



master= []
for i in tqdm(range(parsed.shape[0])):
    if any(char.isalpha() for string in parsed[i] for char in string):
        # print(parsed[i])
        # print(type(parsed[i]))
        # print(ast.literal_eval(parsed[i]))
        # print(type(ast.literal_eval(parsed[i])))
        # break
        for ing in ast.literal_eval(parsed[i]):
            # print(ing)
            master.append(ing.strip())
final = list(set(master))
# print(final)
print(len(final))

with open('ing_list.txt', 'w', encoding="utf-8") as f:
    for ing in final:
        f.write("%s\n" % ing)