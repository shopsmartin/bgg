from sqlite3 import connect


conn = connect('game.db')
c = conn.cursor()


def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS games
    (gameid INTEGER PRIMARY KEY,
    title TEXT,
    published TEXT,
    players TEXT,
    playtime TEXT,
    age INTEGER,
    description TEXT)''')


def data_entry(dict):
    conn = connect('game.db')
    c = conn.cursor()
    game_field_list = [dict.get('id'), dict.get('title'), dict.get('yearpublished'),
                       dict.get('players'), dict.get('playtime'), dict.get('age'),
                       dict.get('description')]

    c.execute("SELECT gameid FROM {tn} WHERE {idf}={my_id}".format(
        tn='games', idf='gameid', my_id=game_field_list[0]))
    id_exists = c.fetchone()
    if id_exists:
        print('Unique ID: {} already in games database'.format(id_exists))
    else:
        print('{} does not exist, entered into database'.format(game_field_list[0]))
        c.execute('''INSERT INTO
                      games
                      (gameid, title, published, players, playtime, age, description)
                      VALUES
                      (?,?,?,?,?,?,?)''', game_field_list)
        conn.commit()
        c.close()
        conn.close()




