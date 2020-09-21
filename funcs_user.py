from sqlite3 import IntegrityError
from funcs_db import add_matches, insert_prepper, get_latest_match
from funcs_base import get_player, get_matches, get_match_players


# Returns all-time kd-ratio for one player
def fetch_player_kd(platform, username):
    kd = get_player(platform, username)['lifetime']['all']['properties']['kdRatio']

    return round(kd, 4)


# Returns list of unique username for all players in specific match
def create_player_list(match_id):
    player_list = []
    resp = get_match_players(match_id)

    for x in resp['teams'][0] + resp['teams'][1]:
        player_list.append(x['unoUsername'])

    return player_list


# Uses the fetch_matches method to chain calls for 20 matches and add to db.
def add_new_matches(platform, username):
    latest = get_latest_match()
    end_time = 0
    added_matches = 0

    while True:
        json_data = get_matches(
            platform, username, end=end_time * 1000, details='details')
        try:
            match_list = insert_prepper(json_data, latest)
            if len(match_list) != 0:
                add_matches(match_list)
        except IntegrityError as er:
            print('sqlite3 error: {}'.format(er.args))
            break

        if len(match_list) == 20:
            added_matches += 20
            end_time = json_data['matches'][-1]['utcEndSeconds']
            continue
        else:
            added_matches += len(match_list)
            print('Reached finishing line. {} matches added'
                  .format(added_matches))
            break
