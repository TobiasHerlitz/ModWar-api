import requests
import time
from definitions import game_mode


class GetMPMatches():
    url = ''

    def __init__(self, platform, username):
        self.platform = platform
        self.username = username

        with requests.Session():
            self.cj = requests.cookies.RequestsCookieJar()
            self.cj.set('ACT_SSO_COOKIE',
                        'MTM4OTgyNDg3OTU3MTA1ODE3Mzc6MTU5MDE0NzI0OTA2ND'
                        'plMjIzOTczZWQ3OWE5YmY0ODc4NGRkYWU1YTZkOWRjOA')

    def make_url(self, start='0', end='0', details=''):

        self.url = 'https://my.callofduty.com/api/papi-client/'\
                   'crm/cod/v2/title/mw/platform/{}/gamer/{}/'\
                   'matches/mp/start/{}/end/{}/{}'.format(self.platform,
                                                          self.username,
                                                          start,
                                                          end,
                                                          details)

        return self.url

    def fetch_matches(self, start='0', end='0', details=''):
        '''
        Makes an API-call and returns a range of matches as dictionary.
        COD restricts to latest 20 matches if details='details'.
        Sets response object to None if API-call fails
        '''

        with requests.Session() as s:
            get_response = s.get(self.make_url(start, end, details),
                                 cookies=self.cj)

        response = get_response.json()

        try:
            assert response['status'] == 'success'
            self.resp_data = response['data']
            return self.resp_data
        except AssertionError:
            self.resp_data = None
            return self.resp_data

    def fetch_match(self, start):
        '''
        Makes an API-call and returns a single match as dictionary.
        Start parameter refers to end time of desired match. Specified in
        milliseconds since epoch.
        Sets response object to None if API-call fails
        '''
        # Setting end time to start plus one second to get one match
        end = start + 1000

        with requests.Session() as s:
            get_response = s.get(self.make_url(start, end, 'details'),
                                 cookies=self.cj)

            response = get_response.json()

        try:
            assert response['status'] == 'success'
            self.resp_data = response['data']
            return self.resp_data
        except AssertionError:
            self.resp_data = None
            return self.resp_data

    def match_index(self):
        '''
        Iterates over matches in fetched object and returns
        list with nested tuples representing each match.
        Has to be run on object where details=''
        '''
        if self.resp_data is None:
            return 'No data found'

        all_matches = self.resp_data
        summary_list = []

        for i in range(len(all_matches)):
            # Timestamp
            timestamp = all_matches[i]['timestamp']

            # Time
            unix_sec = int(timestamp / 1000)
            my_time = time.strftime('%e-%b %R', time.gmtime(unix_sec))

            # Game mode string
            try:
                game_mode_str = game_mode[all_matches[i]['type']]
            except KeyError:
                game_mode_str = all_matches[i]['type']

            # Map name
            map_name = all_matches[i]['map']

            summary_list.append((timestamp, my_time, game_mode_str, map_name))

        return summary_list

    def username_list(self):
        '''Creates and returns a list of players in one specific match'''
        try:
            assert len(self.resp_data['matches']) == 1
        except AssertionError:
            print('No. of matches in resp_data is not 1')
        except TypeError:
            print('TypeError, did you use "details"')
        else:
            username_list = []
            match = self.resp_data['matches'][0]

            all_players = match['allPlayers']['allies'] + match['allPlayers']['axis']

            for i in range(len(all_players)):
                username_list.append(all_players[i]['username'])

            return username_list

    def five_game_kd(self, match_timestamp='0'):
        '''
        Fetches the combined kd-ratio from the 5 previous matches
        (Excluding latest match)
        '''
        if match_timestamp != '0':
            match_timestamp += 1000

        match_index = self.fetch_matches(end=match_timestamp)

        if self.resp_data is None:
            return 'No data found'

        match_range = [match_index[1]['timestamp'], match_index[5]['timestamp']]
        five_earlier = self.fetch_matches(start=match_range[1], end=(match_range[0] + 1000), details='details')
        kd_five = round(five_earlier['summary']['all']['kdRatio'], 4)

        return kd_five


class GetMPUser():
    url = ''

    def __init__(self, platform, username):
        self.platform = platform
        self.username = username

        with requests.Session():
            self.cj = requests.cookies.RequestsCookieJar()
            self.cj.set('ACT_SSO_COOKIE',
                        'MTM4OTgyNDg3OTU3MTA1ODE3Mzc6MTU5MDE0NzI0OTA2ND'
                        'plMjIzOTczZWQ3OWE5YmY0ODc4NGRkYWU1YTZkOWRjOA')

    def make_url(self):

        self.url = 'https://my.callofduty.com/api/papi-client/stats/cod/v1/'\
                   'title/mw/platform/{}/gamer/{}/profile/type/mp'\
                    .format(self.platform,
                            self.username,
                            )

        return self.url

    def fetch_user(self):
        '''
        Makes an API-call and returns user stats as dictionary
        '''
        with requests.Session() as s:
            get_response = s.get(self.make_url(), cookies=self.cj)

        response = get_response.json()

        try:
            assert response['status'] == 'success'
            self.resp_data = response['data']
            return self.resp_data
        except AssertionError:
            self.resp_data = None
            return self.resp_data

    def get_kd(self):
        '''
        Returns all time kdratio
        '''
        if self.resp_data is None:
            return 'No data found'

        kd_ratio = self.resp_data['lifetime']['all']['properties']['kdRatio']
        kd_ratio = round(kd_ratio, 4)

        return kd_ratio
