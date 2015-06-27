# Initial DB setup

import sqlite3
from main import *
import datetime

season_dict = test()


# c = sqlite3.connect('tv_shows.db').cursor()
#
# c.execute('''select 'drop table ' || name || ';' from sqlite_master
#         where type = 'table';''')
#
# c.execute('''CREATE TABLE links (TVShow,
#                                 Link,
#                                 PRIMARY KEY(TVShow))''')
#
# c.execute('''CREATE TABLE seasons (TVShow,
#                                 Season INT,
#                                 PRIMARY KEY(TVShow, Season))''')
#
# c.execute('''CREATE TABLE episodes (TVShow,
#         Season INT,
#         Episode INT,
#         Title,
#         AirDate,
#         Description,
#         PRIMARY KEY(TVShow, Season, Episode))''')


c = sqlite3.connect('tvs.db').cursor()

c.execute(''' CREATE TABLE episodes (
              no_in_series	INTEGER NOT NULL,
              no_in_season	INTEGER NOT NULL,
              title	TEXT NOT NULL,
              original_air_date	TEXT NOT NULL,
              PRIMARY KEY(no_in_series))''')

