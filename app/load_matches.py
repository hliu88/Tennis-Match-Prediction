import pandas as pd

def load_matches_csv():
    df = pd.read_csv('https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_qual_chall_2022.csv')
    dff = pd.read_csv('https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2022.csv')
    df = pd.concat([df, dff])

    #drop winner/loser entry, can replace with var later
    df = df.drop(columns = ['winner_entry', 'loser_entry', 'winner_rank_points', 'loser_rank_points', 'best_of', 'minutes', 'tourney_id', 'tourney_name', 'tourney_level', 'winner_ioc', 'loser_ioc', 'score', 'round', 'draw_size', 'tourney_date', 'match_num'])
    df = df.drop(columns = ['winner_seed', 'loser_seed'])

    #if winner_rank, loser_rank == null, then _rank = 2000
    df['winner_rank'] = df['winner_rank'].fillna(2000)
    df['loser_rank'] = df['loser_rank'].fillna(2000)
    #player height == null = 183cm
    df['winner_ht'] = df['winner_ht'].fillna(183)
    df['loser_ht'] = df['loser_ht'].fillna(183)

    df = df.dropna(axis = 0)

    #dropping for the simplicitty for future match data as surface is unknown
    df = df.drop(columns = ['surface'])
    # df.loc[df["surface"] == "Hard", "surface"] = 1.0
    # df.loc[df["surface"] == "Clay", "surface"] = 2.0
    # df.loc[df["surface"] == "Grass", "surface"] = 3.0
    # df.loc[df["surface"] == "Carpet", "surface"] = 3.0

    df.loc[df["winner_hand"] == "R", "winner_hand"] = 1.0
    df.loc[df["winner_hand"] == "L", "winner_hand"] = 2.0
    df.loc[df["winner_hand"] == "U", "winner_hand"] = 3.0
    df.loc[df["loser_hand"] == "R", "loser_hand"] = 1.0
    df.loc[df["loser_hand"] == "L", "loser_hand"] = 2.0
    df.loc[df["loser_hand"] == "U", "loser_hand"] = 3.0

    df2 = df.drop(columns=['winner_name', 'loser_name'])

    df2 = df.rename({'winner_id':'p1_id', 'winner_seed':'p1_seed', 'winner_hand':'p1_hand', 'winner_ht':'p1_ht', 'winner_ioc':'p1_ioc', 'winner_age':'p1_age', 'w_ace':'p1_ace', 'w_df':'p1_df', 'w_svpt':'p1_svpt', 'w_1stIn':'p1_1stIn', 'w_1stWon':'p1_1stWon', 'w_2ndWon':'p1_2ndWon', 'w_SvGms':'p1_SvGms', 'w_bpSaved':'p1_bpSaved', 'w_bpFaced':'p1_bpFaced', 'winner_rank':'p1_rank',
                    'loser_id':'p2_id', 'loser_seed':'p2_seed', 'loser_hand':'p2_hand', 'loser_ht':'p2_ht', 'loser_ioc':'p2_ioc', 'loser_age':'p2_age', 'l_ace':'p2_ace', 'l_df':'p2_df', 'l_svpt':'p2_svpt', 'l_1stIn':'p2_1stIn', 'l_1stWon':'p2_1stWon', 'l_2ndWon':'p2_2ndWon', 'l_SvGms':'p2_SvGms', 'l_bpSaved':'p2_bpSaved', 'l_bpFaced':'p2_bpFaced', 'loser_rank':'p2_rank'
                    }, axis='columns')
    df2['result'] = 1

    winner = ['p1_id', 'p1_hand', 'p1_ht', 'p1_age', 'p1_ace', 'p1_df', 'p1_svpt', 'p1_1stIn', 'p1_1stWon', 'p1_2ndWon', 'p1_SvGms', 'p1_bpSaved', 'p1_bpFaced', 'p1_rank']
    loser = ['p2_id', 'p2_hand', 'p2_ht', 'p2_age', 'p2_ace', 'p2_df', 'p2_svpt', 'p2_1stIn', 'p2_1stWon', 'p2_2ndWon', 'p2_SvGms', 'p2_bpSaved', 'p2_bpFaced', 'p2_rank']

    df2 = df2.dropna()
    df2 = df2.reset_index(drop=True)
    return df, df2