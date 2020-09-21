import sqlite3


# Takes in list of nested tuples containing match info and insert into db
def add_matches(match_list):
    conn = sqlite3.connect('matches.db')
    c = conn.cursor()

    try:
        c.executemany(
        "INSERT INTO matches "
        "(activision_id, start_time, end_time, map_name, result, kills, deaths) "
        "VALUES (?,?,?,?,?,?,?)", match_list)
    finally:
        conn.commit()
        conn.close()


# Create list of nested tuples containing match information
def insert_prepper(json_data, latest_match=0):
    match_list = []

    for x in json_data['matches']:
        if x['utcEndSeconds'] != latest_match:
            if x['result'] == 'win':
                result = 1
            else:
                result = 0

            match_list.append((
                x['matchID'],
                x['utcStartSeconds'],
                x['utcEndSeconds'],
                x['map'],
                result,
                int(x['playerStats']['kills']),
                int(x['playerStats']['deaths'])
            ))
        else:
            return match_list
    return match_list

# Returns epoch time in seconds of latest stored match in db
def get_latest_match():
    conn = sqlite3.connect('matches.db')
    c = conn.cursor()

    try:
        c.execute('SELECT * FROM matches ORDER BY end_time DESC LIMIT 1')
        resp = c.fetchone()
        if resp is None:
            end_epoch = 0
        else:
            end_epoch = resp[2]
    finally:
        conn.close()

    return end_epoch
