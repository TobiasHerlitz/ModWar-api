import requests
from funcs_helper import cookie_getter

with requests.Session():
    cj = requests.cookies.RequestsCookieJar()
    cj.set('ACT_SSO_COOKIE', cookie_getter())


def getter(url):
    with requests.Session() as s:
        get_response = s.get(url, cookies=cj)

    response = get_response.json()

    assert response['status'] == 'success'
    resp_data = response['data']
    return resp_data


def get_player(platform, username):
    url = 'https://my.callofduty.com/api/papi-client/stats/cod/v1/'\
          'title/mw/platform/{}/gamer/{}/profile/type/mp'\
          .format(platform, username)

    return getter(url)


# For single match, set single=True and start param to end time of match
# For details, set details=details. This limits response to 20 matches
def get_matches(platform, username, single=False, start=0, end=0, details=''):
    # Setting end time to start plus one second to get one match
    if single:
        end = start + 1000

    url = 'https://my.callofduty.com/api/papi-client/'\
          'crm/cod/v2/title/mw/platform/{}/gamer/{}/'\
          'matches/mp/start/{}/end/{}/{}'\
          .format(platform, username, start, end, details)

    return getter(url)


def get_match_players(match_id):
    url = 'https://my.callofduty.com/api/papi-client/ce/'\
          'v1/title/mw/platform/psn/match/{}/matchMapEvents/'\
          .format(match_id)

    return getter(url)