# TVSHOWTRACKER
____________________________________________________

The TVSHOWTRACKER is a command line based program,
written in Python,
to organise the watch status of your TVShows.
You can add and remove TVShows from your list,
and keep track of the episodes, you already watched.
This way, you always now, what to watch next.

It will work with the **english wikipedia** only.

____________________________________________________

*Written for **Python 3.4.3**
GCC 4.9.2 on linux*

____________________________________________________

To run the TVSHOWTRACKER, you need following packages:

*import re, import os, import sys, import time, 
import fw_wiki as wipy,
from lxml import html, from lxml.html.clean 
import clean_html, from lxml import etree
import ast*

fw_wiki is a slightly changed form of the 
[*wikipydia* package](http://github.com/j2labs/wikipydia)
to make it compatible to Python 3.4.3
For fw_wiki, you additionally need:

*simplejson*

____________________________________________________

**Enter the wanted symbol or number
then press ENTER to send your request.
You have to press ENTER, 
in order to have the program recognize your wish.**

## MAIN MENU

+ No TVShow added, yet - Enter [+] to add some shows!
  + Your TVShow list is empty
+ [number] of tv show
  + If there are TVShows in your list, enter the number, 
    next to it's name
    This way, you will go directly to the season overview
+ [+] add new / update show
  + You can add a new TVShow to your list, or update one, 
    that is already in there
    Updates are useful, to fetch new episodes/seasons, 
    that might have been releases since your last update
    **ATTENTION**: *Updating a TVShow means, 
    reloading from Wikipedia. 
    This way, your **watch** status will be deleted!*
    To keep your watch status, 
    make a backup of the *.txt* file of all the seasons, 
    you want to keep.
+ [-] remove show from list
  + remove a TVShow from your list if you are done watching, 
    or *you are **done*** watching ;)
+ [e] exit
  + simple as it is, exit the TVSHOWTRACKER
+ [o] open wikipedia page in browser
  + If there exists a wikipedia page for a TVShow, 
    you can open it in the default browser with [o]
+ [h] help page
  + That's exactly, where you are right now!
  
## SEASON OVERVIEW OF TVSHOW

+ [m]ain menu
  + Go back to the main menu
+ [number] of season
  + Go to detailed view of a single season.
    Simply enter the number next to the season.
    There, you can *watch* or *unwatch* episodes.
    
## DETAILED SEASON VIEW

+ [w]atch/unwatch single episode
  + Enter [w] and then enter the number of the episode,
    you want to mark as watched/unwatched
+ [a]ll episodes toggled
  + [a] changes the state of all episodes in the season.
    all watched episodes become unwatched,
    all unwatched episodes become watched.
+ [m]ain menu
  + Go back to the main menu
+ [b]ack to tv show
  + Go back to the season overview

