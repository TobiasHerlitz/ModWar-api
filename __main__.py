import funcs_user
import funcs_async
import asyncio


def example1(match_id):
    '''Example function that takes in an official match ID and returns a
    dictionary of all participating players and their all-time kd
    return_dict = {'player1': kd1, 'player2': kd2, ...}'''

    # Get list of all participating players in specified match
    players = funcs_user.create_player_list(match_id)

    # No pound signs. This should really be replaced by general htmlify
    players = [i.replace('#', '%23') for i in players]

    # Makes async calls for each player in the list and assembles list of kd
    kd_list = asyncio.get_event_loop().run_until_complete(funcs_async.aiohttp_handler(players))

    # Combines player list and kd list into dictionary
    kd_dict = dict(zip(players, kd_list))

    return kd_dict


# print(example1('3164339122446119171'))
