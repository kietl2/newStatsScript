import pandas as pd
import requests

FILENAME = "rawdata.csv"


RANKEDENDPOINT = "https://api.mcsrranked.com/"

with open("player.txt","r") as f:
    lines = f.readlines()

if len(lines) < 1:
    raise Exception("No username set in player.txt")
USERNAME = lines[0]
if len(lines) < 2:
    r = requests.get(RANKEDENDPOINT + "users/" + USERNAME)
    if r.status_code != 200:
        raise Exception(f"http error code: {r.status_code}")
    UUID = r.json().get("data",None).get("uuid",None)
    if UUID is None:
        raise Exception("something went wrong in the response: ", r.json())
    with open("player.txt","w") as f:
        f.writelines([USERNAME,"\n",UUID])
else:
    UUID = lines[1]

df = pd.read_csv(FILENAME)

# completion times
for i in df['completions']:
    print(i)
completions = df.loc[any((i.get("uuid",None) == UUID) for i in df['completions'])]
print(completions)