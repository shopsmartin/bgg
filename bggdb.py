#from sqlite3 import connect
from psycopg2 import connect
connect_string="dbname='boardgame' user='postgres' host='localhost'"

def create_table():
    connect_string="dbname='boardgame' user='postgres' host='localhost'"
    conn = connect(connect_string)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS games
    (gameid INTEGER PRIMARY KEY,
    title TEXT,
    published TEXT,
    players TEXT,
    playtime TEXT,
    age INTEGER,
    description TEXT,
    mechanics TEXT,
    publisher TEXT)''')

    conn.commit()
    c.close()
    conn.close()


def data_entry(dict):
    connect_string="dbname='boardgame' user='postgres' host='localhost'"
    conn = connect(connect_string)
    c = conn.cursor()
    game_field_list = [dict.get('id'), dict.get('title'), dict.get('yearpublished'),
                       dict.get('players'), dict.get('playtime'), dict.get('age'),
                       dict.get('description'), str(dict.get('mechanics', 'None')).strip('[]').replace(',', ' '),
                       dict.get('publisher')]

    c.execute("SELECT gameid FROM {tn} WHERE {idf}={my_id}".format(
        tn='games', idf='gameid', my_id=game_field_list[0]))
    id_exists = c.fetchone()
    if id_exists:
        print('Unique ID: {} already in games database'.format(id_exists))
    else:
        print('{} does not exist in database'.format(game_field_list[0]))
        c.execute('''INSERT INTO
                      games
                      (gameid, title, published, players, playtime, age, description, mechanics, publisher)
                      VALUES
                      (%s, %s, %s, %s, %s, %s, %s, %s, %s);''', (tuple(game_field_list)))
        print('entered into database')
        conn.commit()
        c.close()
        conn.close()




