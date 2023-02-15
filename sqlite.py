import sqlite3
from datetime import datetime, timezone


class Table:
    def __init__(self):
        self.con = sqlite3.connect("test.db")
        self.cur = self.con.cursor()

    def create_all_channels_table(self, username):
        self.cur.execute(f""" CREATE TABLE IF NOT EXISTS telegramChannels_{username}_allchannels(id_channel TEXT PRIMARY KEY
        );
        """)
        record = self.cur.fetchall()

    def create_table(self, username, channel):
        self.cur.execute(f""" CREATE TABLE IF NOT EXISTS telegramChannels_{username}_{channel}(
        number INTEGER PRIMARY KEY,
        date TEXT,
        id_channel TEXT,
        name_channel TEXT,
        number_users INTEGER
        );
        """)
        record = self.cur.fetchall()

    def insert(self, item, username, channel):
        self.cur.execute(
            f"""INSERT INTO telegramChannels_{username}_{channel} (date, id_channel, name_channel, number_users) VALUES(?,?,?,?)
            ;""", item)
        self.con.commit()

    def insert_in_all_channels_table(self, username, channel):
        self.cur.execute(
            f"""INSERT OR REPLACE INTO telegramChannels_{username}_allchannels (id_channel) VALUES('{channel}')
            ;""")
        self.con.commit()

    def get_channel_statistics(self, username, channel):
        array_of_channels_ids = self.cur.execute(
            f"""SELECT * FROM telegramChannels_{username}_{channel}
            ;""")
        array_channels = []
        for el in array_of_channels_ids:
            array_channels.append(el)
        return array_channels

    def create_username_table(self):
        self.cur.execute(f""" CREATE TABLE IF NOT EXISTS telegramChannels_username(
        username TEXT PRIMARY KEY
        );
        """)
        record = self.cur.fetchall()

    def get_user_id(self, username):
        if username:
            self.cur.execute(
                f""" INSERT OR REPLACE INTO telegramChannels_username (username) VALUES('{username}')""")
            self.con.commit()
            user = self.cur.execute(
                """ SELECT * FROM telegramChannels_username""")
            user = self.cur.fetchone()
            return user[0]

    def user(self):
        user_id = self.cur.execute(
            """SELECT * FROM telegramChannels_username""")
        user_id = self.cur.fetchone()
        if user_id:
            return user_id[0]

    def get_channels_id(self, username):
        if username:
            array_of_channels_ids = self.cur.execute(
                f"""SELECT id_channel FROM telegramChannels_{username}_allchannels
                ;""")
            array_channels = []
            for el in array_of_channels_ids:
                array_channels.append(el)
            return array_channels
        else:
            return 1

    def select(self, channel):
        username = Table().user()
        selection = self.cur.execute(
            f"""SELECT name_channel, date, number_users FROM telegramChannels_{username}_{channel}
            ;""")
        selection = self.cur.fetchall()
        return selection

    def close(self):

        self.cls = self.cur.close()
        if self.con:
            self.con.close()


# item = ("sdaf", "sdffg", 12)

# Table()
# Table().create_table()
# Table().insert(item)
# Table().close()
