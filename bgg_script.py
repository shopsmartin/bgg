__author__ = 'Shopsmartin'
import bgg.bggapi
from bgg.bggdb import data_entry, create_table
import codecs

with codecs.open('games.txt', 'r', 'utf8') as fh:
    data = fh.readlines()
    for line in data:
        print("getting ", line)
        try:
            listofgames = bgg.bggapi.get_bgg_data(line.strip(line[-1]))
            game_list = bgg.bggapi.get_game_id(listofgames)
            for gid in game_list:
                x = bgg.bggapi.get_bgg_data_with_id(gid.get('game_id', None))
                if isinstance(x, dict):
                    data_entry(x)
                else:
                    print(x, 'passing to next')
                    pass
        except KeyError as e:
            print(e, "no boardgame")

fh.close()
