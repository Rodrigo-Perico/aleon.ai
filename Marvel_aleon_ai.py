print("Baixando as bibliotecas necessárias")

import os
os.system("pip install requests pandas seaborn matplotlib")

import requests
import time
import hashlib
import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt

PUBLIC_KEY = "0b08b7e93738e4973b80ae94c2986e7d"
PRIVATE_KEY = "292deed8848488aa3574b5eae82f97b0f22da73c"

ts = int(time.time())

hash_md5 = hashlib.md5(f"{ts}{PRIVATE_KEY}{PUBLIC_KEY}".encode()).hexdigest()

url = "http://gateway.marvel.com/v1/public/creators"  

parametros = {
    "ts": ts,
    "apikey": PUBLIC_KEY,
    "hash": hash_md5,
    "limit": 100
    }

response = requests.get(url, params=parametros)

print(response)

features = [
        "id",
        "fullName",
        "modified",
        "comics.available",
        "comics.returned",
        "series.available",
        "series.returned",
        "stories.available",
        "stories.returned",
        "events.available",
        "events.returned"
    ]

dataset= []

for rounds in range(1, 2): 
  parametros["offset"] = rounds
  response = requests.get(url, params=parametros)
  dataset.extend(response.json()["data"]["results"])

df = pd.json_normalize(dataset)[features]
df = pd.DataFrame(df)


df.columns

df.head(4)

df["participations"] = (
    df["comics.available"] + df["series.available"] + df["stories.available"] + df["events.available"]
)

df["participations"].head(5)

top_criadores = df.groupby("fullName")["participations"].sum().nlargest(10)

plt.figure(figsize=(11, 6))
sns.barplot(x=top_criadores.values, y=top_criadores.index, palette="magma")

plt.title("Top 10 criadores com mais participações", fontsize=14)
plt.xlabel("Total de participações", fontsize=12)
plt.ylabel("Criador", fontsize=12)
plt.show()

print("\n\n/////////////////////////////////////////////////////////////////////////////\n\n")

PUBLIC_KEY="e767bc67663296ecb30c27d5bf7bc97e"
PRIVATE_KEY="5a17622262a47b8d355175e5c6ca63a03dacda50"

ts = int(time.time())

hash_md5 = hashlib.md5(f"{ts}{PRIVATE_KEY}{PUBLIC_KEY}".encode()).hexdigest()

url = "http://gateway.marvel.com/v1/public/comics"

parametros = {
    "ts": ts,
    "apikey": PUBLIC_KEY,
    "hash": hash_md5,
    "limit": 100
    }
response = requests.get(url, params=parametros)

print(response)

dataset= []
for rounds in range(1, 2):
  parametros["offset"] = rounds
  response = requests.get(url, params=parametros)
  dataset.extend(response.json()["data"]["results"])

df = pd.json_normalize(dataset)
df = pd.DataFrame(df)

response = requests.get(url, params=parametros)

df.columns.values

df.sample(3)

df= df[["id", "title", "prices", "issueNumber"]]

df_prices = df["prices"].apply(pd.Series)
df["printPrice"] = df_prices[0].apply(pd.Series)["price"]
df["digitalPurchasePrice"] = df_prices[1].apply(pd.Series)["price"]

df.drop(columns=["prices"], inplace=True)

df.head(8)

df['year'] = df["title"].str.findall(r"\d{4}").str.get(0)

df = df.dropna(subset=['year'])

df.head(4)

sns.heatmap(df[["year", "printPrice"]].corr(), annot=True)
plt.show() 

df = df[df["printPrice"] != 0]

sns.heatmap(df[["year", "printPrice"]].corr(), annot=True)
plt.show() 

df.head()

df = df.sort_values(by="year", ascending=True)

df["year"] = pd.to_numeric(df["year"], errors="coerce")
df["printPrice"] = pd.to_numeric(df["printPrice"], errors="coerce")

sns.regplot(data=df, x="year", y="printPrice")
plt.show()
