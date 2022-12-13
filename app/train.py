import pandas as pd
import numpy as np
# import json
from keras import metrics
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
import keras.backend as K
# from bs4 import BeautifulSoup as bs
from process_players import populate_df

stats = ['ace', 'df', 'svpt', '1stIn', '1stWon', '2ndWon', 'SvGms', 'bpSaved', 'bpFaced']

def get_f1(y_true, y_pred): 
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    recall = true_positives / (possible_positives + K.epsilon())
    f1_val = 2*(precision*recall)/(precision+recall+K.epsilon())
    return f1_val

def nn(x_train, y_train):
    model = Sequential()
    model.add(Dense(np.shape(x_train)[1], kernel_initializer='uniform', activation='relu'))
    model.add(Dense(37, activation='relu', name='dense2'))
    model.add(Dense(37, activation='relu', name='dense3'))
    model.add(Dense(units=1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam',
                  metrics=[get_f1])
    # model.compile(loss='binary_crossentropy', optimizer='adam',
    #               metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=20, batch_size=10, verbose=0)
    # model.fit(x_train, y_train, epochs=35, batch_size=10)
    # model.fit(x_train, y_train, epochs=100, batch_size=20)
    return model

def train_model():
    df = pd.read_csv('https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_qual_chall_2022.csv')
    dff = pd.read_csv('https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2022.csv')
    df = pd.concat([df, dff])

    # df = pd.read_csv('https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2022.csv')

    #dropping for the simplicitty for future match data as surface is unknown
    df = df.drop(columns = ['surface', 'winner_entry', 'loser_entry', 'winner_rank_points', 'loser_rank_points', 'best_of', 'minutes', 'tourney_id', 'tourney_name', 'tourney_level', 'winner_ioc', 'loser_ioc', 'score', 'round', 'draw_size', 'tourney_date', 'match_num', 'winner_seed', 'loser_seed'])

    #if winner_rank, loser_rank == null, then _rank = 2000
    df['winner_rank'] = df['winner_rank'].fillna(2000)
    df['loser_rank'] = df['loser_rank'].fillna(2000)
    #player height == null = 183cm
    df['winner_ht'] = df['winner_ht'].fillna(183)
    df['loser_ht'] = df['loser_ht'].fillna(183)
    df = df.dropna(axis = 0)
    df.loc[df["winner_hand"] == "R", "winner_hand"] = 1.0
    df.loc[df["winner_hand"] == "L", "winner_hand"] = 2.0
    df.loc[df["winner_hand"] == "U", "winner_hand"] = 3.0
    df.loc[df["loser_hand"] == "R", "loser_hand"] = 1.0
    df.loc[df["loser_hand"] == "L", "loser_hand"] = 2.0
    df.loc[df["loser_hand"] == "U", "loser_hand"] = 3.0
    df_with_names = df
    df = df.drop(columns=['winner_name', 'loser_name'])
    df2 = df.rename({'winner_id':'p1_id', 'winner_seed':'p1_seed', 'winner_hand':'p1_hand', 'winner_ht':'p1_ht', 'winner_ioc':'p1_ioc', 'winner_age':'p1_age', 'w_ace':'p1_ace', 'w_df':'p1_df', 'w_svpt':'p1_svpt', 'w_1stIn':'p1_1stIn', 'w_1stWon':'p1_1stWon', 'w_2ndWon':'p1_2ndWon', 'w_SvGms':'p1_SvGms', 'w_bpSaved':'p1_bpSaved', 'w_bpFaced':'p1_bpFaced', 'winner_rank':'p1_rank',
                    'loser_id':'p2_id', 'loser_seed':'p2_seed', 'loser_hand':'p2_hand', 'loser_ht':'p2_ht', 'loser_ioc':'p2_ioc', 'loser_age':'p2_age', 'l_ace':'p2_ace', 'l_df':'p2_df', 'l_svpt':'p2_svpt', 'l_1stIn':'p2_1stIn', 'l_1stWon':'p2_1stWon', 'l_2ndWon':'p2_2ndWon', 'l_SvGms':'p2_SvGms', 'l_bpSaved':'p2_bpSaved', 'l_bpFaced':'p2_bpFaced', 'loser_rank':'p2_rank'
                    }, axis='columns')
    df2['result'] = 1
    winner = ['p1_id', 'p1_hand', 'p1_ht', 'p1_age', 'p1_ace', 'p1_df', 'p1_svpt', 'p1_1stIn', 'p1_1stWon', 'p1_2ndWon', 'p1_SvGms', 'p1_bpSaved', 'p1_bpFaced', 'p1_rank']
    loser = ['p2_id', 'p2_hand', 'p2_ht', 'p2_age', 'p2_ace', 'p2_df', 'p2_svpt', 'p2_1stIn', 'p2_1stWon', 'p2_2ndWon', 'p2_SvGms', 'p2_bpSaved', 'p2_bpFaced', 'p2_rank']

    df2 = df2.dropna()
    df2 = df2.reset_index(drop=True)

    for ind in range(len(df2)):
        if np.random.randint(2) == 1:
            df2.loc[ind, 'result'] = 0
            df2.loc[ind, winner], df2.loc[ind, loser] = df2.loc[ind, loser].values, df2.loc[ind, winner].values

    # p = 0.9
    # idx = int(p * df2.shape[0]) + 1

    # x_train, x_test = np.split(df2, [idx])

    from sklearn.model_selection import train_test_split
    x_train, x_test = train_test_split(df2, random_state=42)

    for i in stats:
        x_test['p1_' + i] = 0
        x_test['p2_' + i] = 0

    x_test = populate_df(x_test, x_train)

    x_train = df2.values[:, :-2]
    y_train = df2.values[:, -1]
    y_test = x_test.values[:, -1]
    x_test = x_test.values[:, :-2]
    x_test = np.asarray(x_test).astype('float32')
    x_train = np.asarray(x_train).astype('float32')
    y_test = np.asarray(y_test).astype('float32')
    y_train = np.asarray(y_train).astype('float32')
    sc = StandardScaler()
    sc.fit(x_train)
    x_train = sc.transform(x_train)
    x_test = sc.transform(x_test)

    model = nn(x_train, y_train)

    yhat = (model.predict(x_test) > 0.5).astype(int)
    print(confusion_matrix(y_test, yhat))
    # print(classification_report(y_test, yhat))
    print(accuracy_score(y_test, yhat))
    print(f1_score(y_test,yhat))
    return

if __name__ == '__main__':
    train_model()