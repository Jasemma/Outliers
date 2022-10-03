import sqlite3
import json
import sys

def create_test_table():
    with sqlite3.connect('warehouse.db') as con:
        cursor = con.cursor()
        cursor.execute(
            """
            create table if not exists test_table (
            Id INTEGER,
           	PostId INTEGER,
        	VoteTypeId INTEGER,
            CreationDate TEXT
            );
            """
        )

create_test_table()


def add_data_to_test_table():
    with open(sys.argv[1]) as votes_in:
         for line in votes_in:
            line = json.loads(line)
            with sqlite3.connect('warehouse.db') as con:
                cursor = con.cursor()
                cursor.execute(
                    """
                    insert into
                    test_table (
                    Id,
                    PostId,
                    VoteTypeId,
                    CreationDate
                    )
                    values (
                    """ +

                    "\'" + str(line['Id']) + '\',' +
                    "\'" + str(line['PostId']) + '\',' +
                    "\'" + str(line['VoteTypeId']) + '\',' +
                    "\'" +str(line['CreationDate']).split('T')[0] + '\'' +
                    ')'
                )

def select_from_test_table():
    with sqlite3.connect('warehouse.db') as con:
        cursor = con.cursor()
        print(list(cursor.execute(
        "select * from test_table"
        )))


def delete_table():
    with sqlite3.connect('warehouse.db') as con:
        cursor = con.cursor()
        cursor.execute(
        "drop table test_table;"
        )

# # create_test_table()
select_from_test_table()
#add_data_to_test_table()
