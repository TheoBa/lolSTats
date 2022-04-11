import pandas as pd


def get_patches(df):
    patches = list(df.patch.unique())
    return [patches[0]] + patches[2:]


def get_leagues(df):
    return list(df.league.unique())


def get_macro_db(df):
    macro_db = df[
        [
            'gameid', 'league', 'date', 'patch', 'playoffs', 'gamelength', 'teamname', 'side',
            'result', 'ban1', 'ban2', 'ban3', 'ban4', 'ban5'
        ]
    ].drop_duplicates()
    macro_db = macro_db.merge(
        macro_db[
            [
                'gameid', 'teamname', 'ban1', 'ban2', 'ban3', 'ban4', 'ban5'
            ]
        ],
        how='inner',
        on='gameid',
        suffixes=['', '_opp']
    )
    macro_db = macro_db[macro_db.teamname != macro_db.teamname_opp].reset_index(drop=True)
    return macro_db


def get_micro_db(df):
    micro_db = df[['gameid', 'result', 'side', 'position', 'playername', 'champion', 'kills', 'deaths', 'date',
                   'assists', 'damageshare', 'earnedgoldshare', 'cspm', 'golddiffat15', 'xpdiffat15', 'csdiffat15']]
    micro_db = micro_db[micro_db.position != 'team']
    micro_db = micro_db.merge(
        micro_db[['gameid', 'position', 'champion', 'playername']],
        how='inner', on=['gameid', 'position'], suffixes=['', '_opp']
    )
    micro_db = micro_db[micro_db.champion != micro_db.champion_opp].reset_index(drop=True)
    return micro_db


def transform_patch(df):
    df.patch = df.patch.map(lambda x: int(x[2:] + x[:2]))
    return df


def select_on_patch(df, min_patch, max_patch):
    return df[(df.patch >= min_patch) & (df.patch <= max_patch)]


def select_on_leagues(df, chosen_leagues):
    return df[df.league.isin(chosen_leagues)]


def select_on_league_macro(macro, chosen_leagues):
    return macro[macro.league.isin(chosen_leagues)]


def select_on_league_micro(micro, games):
    return micro.merge(games, how='inner', on='gameid')


def select_on_champion(df, champion_name):
    return df[df.champion == champion_name]


def select_on_position(df, selected_position):
    return df[df.position == selected_position]


def get_champion_presence(micro, macro, champion):
    total_games_played = len(macro.index) / 2
    cdt_pick = micro.champion == champion
    total_games_picked = len(micro[cdt_pick].index)
    cdt_ban = (macro['ban1'] == champion) | (macro['ban2'] == champion) | (macro['ban3'] == champion) | (
            macro['ban4'] == champion) | (macro['ban5'] == champion)
    total_games_banned = len(macro[cdt_ban].index)
    return round((total_games_picked + total_games_banned) / total_games_played, 3)


def get_champion_winrate(df, champion):
    cdt_pick = df.champion == champion
    cdt_win = df.result == 1
    games_played = len(df[cdt_pick].index)
    games_won = len(df[cdt_pick & cdt_win].index)
    return round(games_won / games_played, 3)


def get_df_champions_statistics(micro):
    stats = [
        'result', 'kills', 'deaths', 'assists', 'damageshare', 'earnedgoldshare',
        'cspm', 'golddiffat15', 'xpdiffat15', 'csdiffat15'
    ]
    return micro.groupby(['champion'], as_index=False).mean(stats).rename(columns={'result': 'winrate'})


def champs_dataframe(micro, macro, stats):
    df_list = []
    for champion in micro.champion.unique():
        df_list.append([champion,
                        get_champion_presence(micro, macro, champion)])
    return pd.DataFrame(df_list, columns=['champion', 'presence']).merge(stats, on='champion', how='inner')


def get_top_champs_per_position(micro):
    top_champs_per_position = {}
    for pos in micro.position.unique():
        considered_champions = list(
            micro[micro.position == pos].groupby(['champion']).size().reset_index(name='counts').sort_values(
                by='counts', ascending=False).head(15).champion)
        top_champs_per_position[pos] = considered_champions
    return top_champs_per_position
