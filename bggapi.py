# written 2016
"""Module for accessing boardgamegeek's API
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from urllib.request import urlopen, HTTPError
from urllib.parse import quote
import xmltodict
import re
from codecs import encode
from time import sleep
from sys import argv, exit
from pprint import pprint
from bgg.bggdb import data_entry, create_table


def get_bgg_data(game=None):
    """function takes a string of a game title or game id """
    if isinstance(game, str):
        url = "http://www.boardgamegeek.com/xmlapi/search?"
        game = 'search=' + quote(game, safe='')
        url += game
        try:
            request = urlopen(url)
            raw_xml = request.read()
            print(url)
            return raw_xml
        except HTTPError as e:
            print(e, 'rest 20 secs')
            sleep(20)
            pass
    else:
        print('game must be type str')


def get_game_id(raw_xml):
    """ Function takes xml from the API and loads it to find the ID """
    game = {}
    game_list = []
    default = 'none'
    if raw_xml is None:
        game = {'game_id': default, 'title': default, 'year_published': 0}
        game_list.append(game)
        return game_list
    else:
        parsed = xmltodict.parse(raw_xml, dict_constructor=dict)
        boardgames = parsed['boardgames']['boardgame']

        for item in boardgames:
            if isinstance(item, str):
                item = boardgames
                pass

            game_id = item.get('@objectid', default)
            year_published = item.get('yearpublished', default)
            try:
                title = item.get('name', default)['#text']
            except TypeError as E:
                title = default
                pass

            #might need an error process here
            #print out the games to choose the matching title

            try:
                print(game_id, title, year_published)
                game = {
                    'game_id': game_id,
                    'title': title,
                    'year_published': year_published
                }
                game_list.append(game)
            except UnicodeEncodeError:
                pass
        return game_list


def get_bgg_data_with_id(game_id):
    """ This function uses the game ID to access the API and construct a dict"""
    # open xml with game id and url open
    game_id = str(game_id)
    default = []
    mechanics = []
    url = 'http://www.boardgamegeek.com/xmlapi/boardgame/' + game_id
    print(url)
    try:
        data_xml = urlopen(url)
        data_dict = xmltodict.parse(data_xml, dict_constructor=dict)
        game_dict = data_dict['boardgames']['boardgame']
        yearpublished = game_dict.get('yearpublished', default)
        minplayers = game_dict.get('minplayers', default)
        maxplayers = game_dict.get('maxplayers', default)
        minplaytime = game_dict.get('minplaytime', default)
        maxplaytime = game_dict.get('maxplaytime', default)
        publisher = game_dict.get('boardgamepublisher', default)
        recommendedage = game_dict.get('age', default)
        description = game_dict.get('description', default)
        description = re.sub('<[^<]+?>', ' ', description)
        description = re.sub('&[a-z]*;', ' ', description)
        description = encode(description, "ascii", errors="ignore")
        title = game_dict.get('name', default)

        try:

            title = title[0].get('#text', default)
        except KeyError:
            # dict(title)
            title = title.get('#text', default)
            pass

        # try:
        #     publisher = publisher[0].get('#text', default)
        # except KeyError:
        #     publisher = publisher['#text']
        publisher = [x['#text'] for x in publisher]
        publisher = str(publisher).strip('[]').replace(',', ' ')



        game = {
            'yearpublished': yearpublished,
            'publisher': publisher,
            'players': '{}-{}'.format(minplayers, maxplayers),
            'playtime': '{}-{}'.format(minplaytime, maxplaytime),
            'age': recommendedage,
            'description': description.decode("utf-8"),
            'title': title,
            'id': game_id
        }

        for k in game_dict.get('boardgamemechanic', default):
            if isinstance(k, str):
                items = list(game_dict.get('boardgamemechanic').items())
                if items[1][1] not in mechanics:
                    mechanics.append(items[1][1])
                else:
                    pass
                game['mechanics'] = mechanics

            else:
                mechanics.append(k.get('#text', k))
                game['mechanics'] = mechanics

        pprint(game)
        return game

    except HTTPError as e:
        sleep(20)
        print(game_id, e)
        pass
    except UnicodeEncodeError as e:
        print(e)
        return e
    except ConnectionResetError as e:
        sleep(5)
        print(game_id, e)
        return e


def main(argv):
    if argv.isdigit():
        x = get_bgg_data_with_id(argv)
        create_table()
        data_entry(x)
    else:
        listofgames = get_bgg_data(game=argv)
        game_list = get_game_id(listofgames)

        # for gid in game_list:
        #     x = get_bgg_data_with_id(gid.get('game_id', None))

    exit()


if __name__ == '__main__':
    main(argv[1])


