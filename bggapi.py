__author__ = 'Shopsmartin'
#program need to have web site handle for API
#take params
#get params from user - title
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
from urllib.request import urlopen, HTTPError
from urllib.parse import urlencode, quote
import xmltodict
from time import sleep
from sys import argv, exit
from pprint import pprint
from bgg.bggdb import data_entry


def get_bgg_data(game=None):
    if isinstance(game, str):
        url = "http://www.boardgamegeek.com/xmlapi/search?"
        game = 'search=' + quote(game, safe='')
        url = url + game
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
    #open xml with game id and url open
    game_id = str(game_id)
    default = []
    mechanics = []
    url = 'http://www.boardgamegeek.com/xmlapi/boardgame/' + game_id
    print(url)
    try:
        data_xml = urlopen(url)
        data_dict = xmltodict.parse(data_xml)
        game_dict = data_dict['boardgames']['boardgame']
        yearpublished = game_dict.get('yearpublished', default)
        minplayers = game_dict.get('minplayers', default)
        maxplayers = game_dict.get('maxplayers', default)
        minplaytime = game_dict.get('minplaytime', default)
        maxplaytime = game_dict.get('maxplaytime', default)
        recommendedage = game_dict.get('age', default)
        description = game_dict.get('description', default)
        description = re.sub('<[^<]+?>', ' ', description)
        description = re.sub('&[a-z]*;', ' ', description)
        title = game_dict.get('name', default)

        try:
            title = title[1].get('#text', default)
        except KeyError:
            dict(title)
            title = title.get('#text', default)
            pass

        game = {
            'yearpublished': yearpublished,
            'players': '{}-{}'.format(minplayers, maxplayers),
            'playtime': '{}-{}'.format(minplaytime, maxplaytime),
            'age': recommendedage,
            'description': description,
            'title': title,
            'id': game_id
        }

        #print(u"Game: {}, age: {}, players: {} - {}, published: {}, time: {} - {} minutes, description: {}".format(title, recommendedage, minplayers, maxplayers, yearpublished, minplaytime, maxplaytime, description))
        for k in game_dict.get('boardgamemechanic', default):
            if isinstance(k, str):
                items = list(game_dict.get('boardgamemechanic').items())
                #print('mechanic: ', items[1][1])
                if items[1][1] not in mechanics:
                    mechanics.append(items[1][1])
                else:
                    pass
                game['mechanics'] = mechanics
                #k = dict(k)
                #print('mechanic: ', k.get('#text', k))
            else:
                #print('mechanic: ', k.get('#text', k))
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
        data_entry(x)
    else:
        listofgames = get_bgg_data(game=argv)
        game_list = get_game_id(listofgames)

        for gid in game_list:
            x = get_bgg_data_with_id(gid.get('game_id', None))

            data_entry(x)

    exit()


if __name__ == '__main__':
    main(argv[1])


