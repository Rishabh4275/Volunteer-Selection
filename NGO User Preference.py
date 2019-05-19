import pandas as pd
import json
import math
from collections import defaultdict
from operator import itemgetter

def userpreference(NGO_Data, User_Data):
    ngo_pd = pd.read_excel(NGO_Data, index_col = 0, sheetname = "Sheet1")
    user_pd = pd.read_excel(User_Data, index_col = 0, sheetname = "Sheet1")
    ngojson = defaultdict(list)
    json_final= {}
    for user_row in user_pd.iterrows():
        for ngo_row in ngo_pd.iterrows():
            total_score=0
            distance_score = cal_dis_score(user_row[1][0],ngo_row[1][1])
            day_score = cal_score(user_row[1][1],ngo_row[1][3])
            cat_score = cal_score(user_row[1][2],ngo_row[1][2])
            total_score = distance_score + cat_score + day_score
            ngojson[ngo_row[0]].append({"name" : user_row[0], "score" : total_score})
    for x,y  in ngojson.items():
        json_final[x] = sorted(y, key=itemgetter('score', 'name'), reverse=True)
    print (json_final)
    with open('data1.json', 'w') as outfile:
        json.dump(json_final, outfile)

def cal_dis_score(user, ngo):
    user= list(map(int,user.split(",")))
    ngo = list(map(int,ngo.split(",")))
    score = math.sqrt( ((user[0]-ngo[0])**2)+((user[1]-ngo[1])**2) )
    return int(50/(int(score)==0 and 1 or int(score)))

def cal_score(user, ngo):
    user = user.split(",")
    user = [x.strip(' ') for x in user]
    ngo = ngo.split(",")
    ngo = [x.strip(' ') for x in ngo]
    for x in user:
        if x in ngo:
            return 5
    return 0

if __name__ == "__main__":
    userpreference("NGO Data.xlsx","User Data.xlsx")
