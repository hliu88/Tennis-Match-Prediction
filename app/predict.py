import pandas as pd
import numpy as np
import keras
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from joblib import load
import json
import pickle
from .load_matches import load_matches_csv
from .process_players import populate_df
from sklearn.metrics import f1_score
from datetime import date, timedelta
import requests

columns = ['p1_id', 'p1_hand', 'p1_ht', 'p1_age', 'p2_id', 'p2_hand', 'p2_ht',
           'p2_age', 'p1_ace', 'p1_df', 'p1_svpt', 'p1_1stIn', 'p1_1stWon',
           'p1_2ndWon', 'p1_SvGms', 'p1_bpSaved', 'p1_bpFaced', 'p2_ace', 'p2_df',
           'p2_svpt', 'p2_1stIn', 'p2_1stWon', 'p2_2ndWon', 'p2_SvGms',
           'p2_bpSaved', 'p2_bpFaced', 'p1_rank', 'p2_rank', 'result']

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def predict_m(day=None):
    model = keras.models.load_model(os.path.join(BASE_DIR, 'app/tennis_model_big'))
    df_with_names, df = load_matches_csv()
    today = date.today()
    if not day:
        f = open(os.path.join(BASE_DIR, 'app/match_predict.json'))
        data = json.load(f)
        f.close()
        # print(type(data))
    elif(day == "today"):
        today = today.strftime("%Y-%m-%d")
        url = 'https://tnnz.io/api_web?mode=matches_daily&date={}&timezone=America%2FNew_York&language=en&platform=web&version=100&subscribed=%7B%7D&favorites=%7B%7D&theme_settings=%7B%7D'.format(today)
        data = requests.get(url).json()
    elif(day == "yesterday"):
        yesterday = (today - timedelta(days=1)).strftime("%Y-%m-%d")
        url = 'https://tnnz.io/api_web?date={}&mode=matches_daily&timezone=America%2FNew_York&language=en&platform=web&version=100&subscribed=%7B%7D&favorites=%7B%7D&theme_settings=%7B%7D'.format(yesterday)
        data = requests.get(url).json()
        # print(data)
    elif(day == "tomorrow"):
        tomorrow = (today + timedelta(days=1)).strftime("%Y-%m-%d")
        url = 'https://tnnz.io/api_web?date={}&mode=matches_daily&timezone=America%2FNew_York&language=en&platform=web&version=100&subscribed=%7B%7D&favorites=%7B%7D&theme_settings=%7B%7D'.format(tomorrow)
        data = requests.get(url).json()
        # print(data)
    df_event = pd.DataFrame(columns=['p1', 'p2', 'result', 'event'])
    for i in range(len(data["_"]["0"]["1"])):
        for j in range(len(data["_"]["0"]["1"][i]["0"])):
            try:
                p1 = data["_"]["0"]["1"][i]["0"][j]["7"][0]['8']
                p2 = data["_"]["0"]["1"][i]["0"][j]["7"][1]['8']
                if(data["_"]["0"]["1"][i]["0"][j]["j"]=='scheduled'):
                    result = -1
                elif(not data["_"]["0"]["1"][i]["0"][j]["d"]):
                    pass
                else:
                    a, b = 0, 0
                    for z in range(len(data["_"]["0"]["1"][i]["0"][j]["d"])):
                        if(data["_"]["0"]["1"][i]["0"][j]["d"][z][0]['e'] > data["_"]["0"]["1"][i]["0"][j]["d"][z][1]['e']):
                            a += 1
                        else:
                            b += 1
                    if(a > b):
                        result = 1
                    else:
                        result = 0
                event = data["_"]["0"]["1"][i]["2"]
                if("Doubles" in event):
                    continue
                df_event.loc[len(df_event.index)] = [p1, p2, result, event] 
            except:
                continue

    df_event['p1'] = df_event['p1'].apply(lambda x: data["P"][int(x[2:], 36)] if x[0]=='p' else x)
    df_event['p2'] = df_event['p2'].apply(lambda x: data["P"][int(x[2:], 36)] if x[0]=='p' else x)

    pd_columns = columns
    df_future = pd.DataFrame(columns=pd_columns)

    full_columns = df_with_names.columns.tolist()
    winner_name = full_columns.index('winner_name')
    winner_id = full_columns.index('winner_id')
    winner_hand = full_columns.index('winner_hand')
    winner_ht = full_columns.index('winner_ht')
    winner_age = full_columns.index('winner_age')
    winner_rank = full_columns.index('winner_rank')
    loser_name = full_columns.index('loser_name')
    loser_id = full_columns.index('loser_id')
    loser_hand = full_columns.index('loser_hand')
    loser_ht = full_columns.index('loser_ht')
    loser_age = full_columns.index('loser_age')
    loser_rank = full_columns.index('loser_rank')


    df_player_name_id = pd.DataFrame(columns=['first', 'last', 'id'])
    for i, row in df_event.iterrows():
        p1_first = row['p1'].split(" ")[0]
        p1_last = row['p1'].split(" ")[-1]
        p2_first = row['p2'].split(" ")[0]
        p2_last = row['p2'].split(" ")[-1]
        match_result = row['result']
        def id_search(first, last):
            for r in df_with_names[::-1].to_numpy():
                playerid, hand, ht, age, rank = '', '', '', '', ''
                if first in r[winner_name] and last in r[winner_name]:
                    playerid = r[winner_id]
                    hand = r[winner_hand]
                    ht = r[winner_ht]
                    age = r[winner_age]
                    rank = r[winner_rank]
                    break
                elif first in r[loser_name] and last in r[loser_name]:
                    playerid = r[loser_id]
                    hand = r[loser_hand]
                    ht = r[loser_ht]
                    age = r[loser_age]
                    rank = r[loser_rank]
                    break
            df_player_name_id.loc[len(df_player_name_id)] = [first, last, playerid]
            return [playerid, hand, ht, age, rank]
        p1_info, p2_info = id_search(p1_first, p1_last), id_search(p2_first, p2_last)
        if(p1_info[0] != '' and p2_info[0] != ''):
            new_row = pd.DataFrame({'p1_id': p1_info[0], 'p1_hand': p1_info[1], 'p1_ht': p1_info[2], 'p1_age': p1_info[3], 'p1_rank': p1_info[4], 'p2_id': p2_info[0], 'p2_hand': p2_info[1], 'p2_ht': p2_info[2], 'p2_age': p2_info[3], 'p2_rank': p2_info[4], 'result': match_result}, index=[0])
            df_future = pd.concat([new_row,df_future.loc[:]]).reset_index(drop=True)
            df_future = df_future[pd_columns]

    df_future = populate_df(df_future, df)

    df_future_no_result = df_future.loc[(df_future['result'] == -1)]
    df_future = df_future[df_future['result'] != -1]

    def split_x_y_and_predict(df, noresult=False):
        x_pred = df.values[:, :-2]
        y_pred = df.values[:, -1]
        x_pred = np.asarray(x_pred).astype('float32')
        y_pred = np.asarray(y_pred).astype('float32')
        sc = pickle.load(open(os.path.join(BASE_DIR, 'app/scaler.pkl'),'rb'))
        x_pred = sc.transform(x_pred)
        yhat_pred = (model.predict(x_pred) > 0.5).astype(int)
        # print(confusion_matrix(y_pred, yhat_pred))
        # print(f1_score(y_pred,yhat_pred))
        y_pred = np.reshape(y_pred, (len(y_pred), 1))
        result = np.concatenate((df[['p1_id', 'p2_id', 'result']].to_numpy(), yhat_pred), axis=1)
        if(noresult==True):
            return result
        return result, f1_score(y_pred,yhat_pred)

    if(not df_future.empty):
        result1 = split_x_y_and_predict(df_future)
        for i in result1[0]:
            i[0] = df_player_name_id.loc[df_player_name_id['id'] == i[0]][['first', 'last']].to_string(header=False, index=False, index_names=False).split('\n')[0]
            i[1] = df_player_name_id.loc[df_player_name_id['id'] == i[1]][['first', 'last']].to_string(header=False, index=False, index_names=False).split('\n')[0]
    if(not df_future_no_result.empty):
        result2 = split_x_y_and_predict(df_future_no_result, True)
        for i in result2:
            i[0] = df_player_name_id.loc[df_player_name_id['id'] == i[0]][['first', 'last']].to_string(header=False, index=False, index_names=False).split('\n')[0]
            i[1] = df_player_name_id.loc[df_player_name_id['id'] == i[1]][['first', 'last']].to_string(header=False, index=False, index_names=False).split('\n')[0]
        result2[:,2] = None
        return np.concatenate((result1[0], result2)), -1
    if(df_future.empty and df_future_no_result.empty):
        return "No Matches Avaliable"
    return result1
    
    


if __name__ == '__main__':
    # print(predict_m('today'))
    # predict_m()
    print(predict_m())