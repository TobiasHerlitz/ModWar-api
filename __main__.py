import funcs_user
import funcs_async
import asyncio


# player_list = user_funcs.create_player_list('3164339122446119171')
# player_list = [i.replace('#', '%23') for i in player_list]
# player_list = [(i, user_funcs.fetch_player_kd('uno', i)) for i in player_list]
# print(player_list)


def example1(match_id):
    '''Example function that takes in an official match ID and returns a
    dictionary of all participating players and their all-time kd
    return_dict = {'player1': kd1, 'player2': kd2, ...}'''

    # Get list of all participating players in specified match
    players = funcs_user.create_player_list(match_id)

    # No pound signs. This should really be replaced by general htmlify
    players = [i.replace('#', '%23') for i in players]

    # Makes async calls for each player in the list and assembles list of kd
    x = asyncio.get_event_loop().run_until_complete(funcs_async.aiohttp_handler(players))


    # my_dict = dict(zip(og_player_list, x))
    # return my_dict

print(
    example1('3164339122446119171')
)
