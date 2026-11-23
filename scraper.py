import pandas as pd
import requests
import os

RANKEDENDPOINT = "https://api.mcsrranked.com/"

USERNAME = "kietl"
UUID = requests.get(RANKEDENDPOINT + "users/" + USERNAME).json().get("data").get("uuid")

FILENAME = "rawdata.csv"


class Match():
    def __init__(self, matchData) -> None:
        self.id = matchData.get("id", None)
        self.date = matchData.get("date", None)
        self.matchType = self.parseMatchType(matchData.get("type", None))
        self.seed = matchData.get("seed", None)
        self.category = matchData.get("category", None)
        self.gameMode = matchData.get("gameMode", None)
        self.players = matchData.get("players", None)
        self.spectators = matchData.get("spectators", None)
        self.result = matchData.get("result", None)
        self.forfeited = matchData.get("forfeited", None)
        self.decayed = matchData.get("decayed", None)
        self.rank = matchData.get("rank", None)
        self.vod = self.parseVods(matchData.get("vod", None))
        self.changes = matchData.get("changes", None)
        self.completions = matchData.get("completions", None)
        self.timelines = self.parseTimelines(matchData.get("timelines", None))
        self.beginner = matchData.get("beginner", None)
        self.botSource = matchData.get("botSource", None)
        self.replaySize = matchData.get("replaySize", None)
        self.season = matchData.get("season", None)
        self.replayExists = matchData.get("tag", None)
        self.tag = matchData.get("tag", None)
        self.overworld = matchData.get("seedType", None)
        self.bastion = matchData.get("bastionType", None)

        self.values = [
            self.id,        self.date,      self.matchType, 
            self.seed,      self.category,  self.gameMode, 
            self.players,   self.spectators,self.result, 
            self.forfeited, self.decayed,   self.rank, 
            self.vod,       self.changes,   self.completions, 
            self.timelines, self.beginner,  self.botSource, 
            self.replaySize,self.season,    self.replayExists, 
            self.tag,       self.overworld, self.bastion,
        ]


    def parseMatchType(self,matchType):
        return {1: "Casual", 2: "Ranked", 3: "Private room", 4: "Event Mode"}.get(matchType, "Unknown")

    def parseVods(self,vods):
        vodData = {}
        for vod in vods:
            timestamp = self.date-vod["startsAt"]-self.result["time"]//1000
            link = vod["url"] + "?t=" + str(timestamp) + "s"
            vodData[vod["uuid"]] = link
        return vodData

    def parseTimelines(self,timelines):
        times = {}
        for timeline in timelines:
            uuid = timeline.get("uuid")
            if times.get(uuid,None) is None:
                times[uuid] = {}
            times[uuid][timeline.get("type")] = timeline.get("time")
        return times


# Gather all my match data from ranked api
response = requests.get(
    RANKEDENDPOINT + "users/" + USERNAME + "/matches", 
    params = {
        "count": 100
    }
)
json = response.json()

if json.get("status", None) != "success":
    raise Exception("failed to get match data")
data = json.get("data",None)


if not os.path.exists(FILENAME):
    df = pd.DataFrame(columns=[
        "matchID",      "date",         "matchType", 
        "seed",         "category",     "gameMode", 
        "players",      "spectators",   "result", 
        "forfeited",    "decayed",      "rank", 
        "vod",          "changes",      "completions", 
        "timelines",    "beginner",     "botSource", 
        "replaySize",   "season",       "replayExists", 
        "tag",          "overworld",    "bastion"
        ])
    df.to_csv(FILENAME,index=False)

df = pd.read_csv(FILENAME)

# Parse into match class which puts data into pandas df
# and then into data.csv
for m in data:
    matchId = m.get("id", None)
    knownIds = df.get("matchID")
    if knownIds is None or matchId not in [int(k) for k in knownIds]:
        response = requests.get(RANKEDENDPOINT + "matches/" + str(matchId))
        matchData = response.json().get("data")
        values = Match(matchData).values
        df.loc[len(df)] = values
df.to_csv(FILENAME,index=False)