from fastapi import FastAPI
import json
import pandas as pd
from urllib.request import urlopen
import json

app = FastAPI()

data = []

url = 'https://itunes.apple.com/search?term=NCT&limit=200'
res = urlopen(url)
data.extend(json.load(res)['results'])
df = pd.json_normalize(data)
df['release_year'] = df['releaseDate'].str[:4].astype('int64')

@app.get("/")
def read_root():
	return data

#menampilkan jumlah trakcs setiap unit
@app.get("/countUnitSong")
def read_countUnitSong():
	api = df.groupby(['artistName'])[['trackName']].count().rename(columns={'trackName':'count'}).sort_values(['count'], ascending=False)
	return api.to_dict(orient='dict')

#menampilkan 5 album dengan jumlah lagu terbanyak
@app.get("/albumTracks")
def read_countUnitSong():
	api = result_2 = df.groupby(['collectionName'])[['trackName']].count().rename(columns={'trackName':'count'}).sort_values(['count'], ascending=False).head(5)
	return api.to_dict(orient='dict')

#menampilkan 5 rata-rata tertinggi harga album
@app.get("/albumPrice")
def read_countUnitSong():
	api = df.groupby(['artistName'])[['collectionPrice']].mean().rename(columns={'collectionPrice':'mean'}).sort_values(['mean'], ascending=False).head(5)
	return api.to_dict(orient='dict')

