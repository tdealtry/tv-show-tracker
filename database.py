import sqlite3

conn = sqlite3.connect('tvshows.db')
c = conn.cursor()

c.execute('''select 'drop table ' || name || ';' from sqlite_master 
        where type = 'table';''')

c.execute('''CREATE TABLE links (TVShow, 
                                Link,
                                PRIMARY KEY(TVShow))''')
             
c.execute('''CREATE TABLE seasons (TVShow, 
                                Season INT,
                                PRIMARY KEY(TVShow, Season))''')

c.execute('''CREATE TABLE episodes (TVShow, 
        Season INT, 
        Episode INT, 
        Title, 
        AirDate, 
        Description,
        PRIMARY KEY(TVShow, Season, Episode))''')
