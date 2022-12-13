import pandas as pd
import numpy as np
stats = ['ace', 'df', 'svpt', '1stIn', '1stWon', '2ndWon', 'SvGms', 'bpSaved', 'bpFaced']

def process_df(df, playerA, playerA_num, playerA_count, col, rate = 0.4): 
    playerA["ace"] += df[col[playerA_num + '_ace']]
    playerA["df"] += df[col[playerA_num + '_df']]
    playerA["svpt"] += df[col[playerA_num + '_svpt']]
    playerA["1stIn"] += df[col[playerA_num + '_1stIn']]
    playerA["1stWon"] += df[col[playerA_num + '_1stWon']]
    playerA["2ndWon"] += df[col[playerA_num + '_2ndWon']]
    playerA["SvGms"] += df[col[playerA_num + '_SvGms']]
    playerA["bpSaved"] += df[col[playerA_num + '_bpSaved']]
    playerA["bpFaced"] += df[col[playerA_num + '_bpFaced']]
    playerA_count += rate
    return playerA, playerA_count

def populate_df(df, df2):
    p1_id = df2.columns.tolist().index('p1_id')
    p2_id = df2.columns.tolist().index('p2_id')

    columns = df2.columns.tolist()
    col_indx = {
        "p1_ace": columns.index('p1_ace'),
        "p1_df": columns.index('p1_df'),
        "p1_svpt": columns.index('p1_svpt'),
        "p1_1stIn": columns.index('p1_1stIn'),
        "p1_1stWon": columns.index('p1_1stWon'),
        "p1_2ndWon": columns.index('p1_2ndWon'),
        "p1_SvGms": columns.index('p1_SvGms'),
        "p1_bpSaved": columns.index('p1_bpSaved'),
        "p1_bpFaced": columns.index('p1_bpFaced'),
        "p2_ace": columns.index('p2_ace'),
        "p2_df": columns.index('p2_df'),
        "p2_svpt": columns.index('p2_svpt'),
        "p2_1stIn": columns.index('p2_1stIn'),
        "p2_1stWon": columns.index('p2_1stWon'),
        "p2_2ndWon": columns.index('p2_2ndWon'),
        "p2_SvGms": columns.index('p2_SvGms'),
        "p2_bpSaved": columns.index('p2_bpSaved'),
        "p2_bpFaced": columns.index('p2_bpFaced')
    }

    indx = 0
    df.reset_index(drop=True, inplace=True)

    for row in df.to_numpy():
        p1_stats = dict.fromkeys(stats, 0)
        p2_stats = dict.fromkeys(stats, 0)
        p1_count = 0
        p2_count = 0
        player1 = row[df.columns.tolist().index('p1_id')]
        player2 = row[df.columns.tolist().index('p2_id')]
        for r in df2.to_numpy():
            if(r[p1_id] == player1 and r[p2_id] != player2):
                p1_stats, p1_count = process_df(r, p1_stats, 'p1', p1_count, col_indx)
            elif(r[p2_id] == player1 and r[p1_id] != player2):
                p1_stats, p1_count = process_df(r, p1_stats, 'p2', p1_count, col_indx)
            if(r[p1_id] == player2 and r[p2_id] != player1):
                p2_stats, p2_count = process_df(r, p2_stats, 'p1', p2_count, col_indx)
            elif(r[p2_id] == player2 and r[p1_id] != player1):
                p2_stats, p2_count = process_df(r, p2_stats, 'p2', p2_count, col_indx)
            if(r[p1_id] == player1 and r[p2_id] == player2):
                p1_stats, p1_count = process_df(r, p1_stats, 'p1', p1_count, col_indx, 0.6)
                p2_stats, p2_count = process_df(r, p2_stats, 'p2', p2_count, col_indx, 0.6)
            elif(r[p1_id] == player2 and r[p2_id] == player1):
                p1_stats, p1_count = process_df(r, p1_stats, 'p2', p1_count, col_indx, 0.6)
                p2_stats, p2_count = process_df(r, p2_stats, 'p1', p2_count, col_indx, 0.6)
        for i in stats:
            if p1_count == 0:
                p1_count += 1
            if p2_count == 0:
                p2_count += 1
            df.loc[indx, ('p1_' + i)] = p1_stats[i]/p1_count
            df.loc[indx, ('p2_' + i)] = p2_stats[i]/p2_count
        indx += 1
    return df