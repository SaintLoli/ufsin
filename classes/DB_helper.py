import sqlite3

class DBHelper:
    def __init__(self):
        self.con = sqlite3.connect('data/ItemBase.db')
        self.cur = self.con.cursor()


    def delete_table(self, table):
        self.cur.execute(f"DELETE FROM {table}")
        self.con.commit()

    def add_info_to_main_table(self, data_dict):
        data_dict["title"] = data_dict["title"].replace("'", "`")
        print(data_dict['title'])

        self.cur.execute(f"""
                            INSERT INTO Main_Table(group_id, type, title) VALUES
                            (
                                '{data_dict["group_id"]}', '{data_dict["type"]}', '{data_dict["title"]}'
                            )
                        """)
        self.con.commit()


    def add_info_to_data_table(self, data_dict):
        self.delete_table('Data_Table')
        for skin in data_dict:
            print(f"""
                                       INSERT INTO Data_Table(skin_title, min_float, stickers, skin_price) VALUES
                                       (
                                           '{skin["title"]}', '{skin["min_float"]}', '{skin["stickers"]}', '{skin["skin_price"]}'
                                       )
                                   """)

            self.cur.execute(f"""
                                       INSERT INTO Data_Table(skin_title, min_float, stickers, skin_price) VALUES
                                       (
                                           '{skin["title"].replace("'", "`")}', '{skin["min_float"]}', '{str(skin["stickers"]).replace("'", '"')}', '{skin["skin_price"]}'
                                       )
                                   """)
            self.con.commit()
