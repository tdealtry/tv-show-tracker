#!/usr/bin/env python3

import re
import os
import sys
import ast
from urllib import request

from colorama import Fore, Back, Style

import wikipedia
from lxml import html
from lxml.html.clean import clean_html

s_t_s = '<table class="wikitable plainrowheaders wikiepisodetable"'
table_end = '</table>'
table_row_start = '<tr class="vevent"'
table_row_end = '</tr>'
episodes_start = 'id="Episode'


def clear_screen():
    os.system(['clear', 'cls'][os.name == 'nt'])


def write_file(file_name, content):
    file = open(file_name, 'w+')
    file.write(content)
    file.close()
    return file_name


def read_file(file_name):
    file = open(file_name, 'r')
    content = file.read()
    return content


def add_tv_show(title):
    if not title:
        return

    search = 'list of ' + title + ' episodes'
    title_code = re.sub(' ', '_', title)
    tv_show_folder = 'tvshows/' + title_code

    try:
        wiki_page = wikipedia.page(search)
        wiki_link = wiki_page.url

        try:
            os.mkdir(tv_show_folder)
        except FileExistsError:
            pass
        clear_screen()
    except (IndexError, wikipedia.exceptions.PageError):
        wiki_link = ''
        print('\n\n\n\nThis TV Show does not exist on Wikipedia..')
        print('Maybe try, writing it differently')
        print('e.g. Blacklist = The Blacklist')
        input('[ENTER] to go back to main menu')
        display_overview()

    wiki_content = request.urlopen(wiki_link)
    wiki_content = wiki_content.read().decode('utf-8', 'ignore')
    wiki_content = clean_html(wiki_content)
    #print (wiki_content)
    wiki_content = s_t_s + wiki_content.split(s_t_s,1)[1]
    wiki_content = re.sub(r'<br ?/?>\n', ' ', wiki_content)
    wiki_content = re.sub(r'</?a.*?>', '', wiki_content)

    no_of_tables = len(re.findall(s_t_s, wiki_content))

    seasons = [s_t_s +
               str(wiki_content).split(s_t_s)[season + 1].split(table_end)[0] +
               table_end
               for season in range(no_of_tables) if 'vevent' in
               s_t_s +
               str(wiki_content).split(s_t_s)[season + 1].split(table_end)[0] +
               table_end]

    i = 1
    for season in seasons:

        season_file_name = 'tvshows/' + title_code + '/' + title_code + '_' + str(seasons.index(season) + 1) + '.txt'
        doc_root = html.fromstring(season)
        header = ['[]', 'Total', 'Episode', 'Title']

        eps = doc_root.xpath('//table[@class="wikitable plainrowheaders wikiepisodetable"]/tbody/tr[@class="vevent"]/td[@class="summary"]//text()')
        #print (eps)
        ep = [ep for ep in eps if len(ep) > 2]

        episodes = []
        for e in ep:
            episodes.append([False, i, ep.index(e) + 1, re.sub('"', '', e)])
            i += 1
        episodes.insert(0, header)
        write_file(season_file_name, str(episodes))

    return seasons


def delete_tv_show(title):
    remove_tv_show = 'rm -rf ' + 'tvshows/' + re.sub(' ', '_', title.lower())
    os.system(remove_tv_show)


def display_header(to_display):
    print(Back.GREEN + '\n', 5 * ' ', to_display, '\n' + Back.RESET)


def display_overview():
    clear_screen()
    display_header('TVShowTracker')
    path = 'tvshows/'

    for path, dirs, files in os.walk(path):
        dirs.sort()
        for directory in dirs:
            tv_show = '%7s' % ('[' + str(dirs.index(directory) + 1) + ']   ') + \
                      '%-20s' % (re.sub('_', ' ', directory))
            print(tv_show)

    try:
        tvshows = sorted([dirs for path, dirs, files in os.walk('tvshows/') if len(dirs) > 0][0])
    except IndexError:
        tvshows = []
        print(Fore.RED + ' No TVShow added, yet - Enter [+] to add some shows!' + Fore.RESET)
    print('''\n [number] of tv show\n
    [+] add new / update show
    [-] remove show from list
    [e] exit
    [h] help page''')
    which_tvshow = input('\n\n ACTION: ')
    if which_tvshow == 'e':
        sys.exit(0)
    if which_tvshow == '0':
        display_overview()
    elif which_tvshow == 'h':
        display_help()
        return
    else:
        try:
            int(which_tvshow) <= len(tvshows)
            display_tvshow(tvshows[int(which_tvshow) - 1])
        except (IndexError, ValueError, NameError):
            if which_tvshow == '+':
                title = str(input(''' Which TV Show do you want to add to your collection?
        ''').lower().strip())
                add_tv_show(title)
                display_overview()
            elif which_tvshow == '-':
                del_show = input(''' Which TV Show should be removed?
        Please enter the Title of the show, you want to remove.
        ''').lower().strip()
                if not del_show:
                    display_overview()
                delete_tv_show(del_show)
                display_overview()
            else:
                display_overview()


def display_help():
    clear_screen()
    os.system('cat README.md | more')
    input('\n\n [ENTER] to go back to main menu\n ')
    display_overview()


def display_tvshow(title):
    clear_screen()
    display_header(re.sub('_', ' ', title).capitalize())
    path = 'tvshows/' + title + '/'
    for path, dirs, files in os.walk(path):
        files.sort(key=lambda x: int(x.split('_')[-1][:-4]))
        for season in files:
            season_number = season.split('_')[-1][:-4]
            watched = get_watch_status(title, season)
            print_season = ' %-7s' % ('[' + season_number + ']') + 'Season %2s' % season_number + '%7s' % watched
            print(print_season)
    season = input('\n [m]ain menu\n [number] of season\n\n ACTION: ')
    if season == 'm':
        display_overview()
    try:
        int(season)
        try:
            display_season(title, int(season))
        except FileNotFoundError:
            display_tvshow(title)
    except ValueError:
        display_tvshow(title)


def display_season(title, season):
    season_path = 'tvshows/' + title + '/' + title + '_' + str(season) + '.txt'
    season_list = ast.literal_eval(read_file(season_path))

    clear_screen()
    display_header('' + re.sub('_', ' ', title).capitalize() + ' - Season ' + str(season))

    for episode in season_list:
        ep = ' %-7s' % ('[X]' if episode[0] else '[ ]') + \
             '%7s' % (str(episode[2])) + \
             '   %5s' % (str(episode[1])) + \
             '   ' + \
             episode[3]
        print(ep)

    print('\n WHAT DO YOU WANT TO DO NOW?\n')
    what_to_do_now = input('''
    [w]atch/unwatch single episode
    [a]ll episodes toggled
    [m]ain menu
    [b]ack to tv show\n
    ACTION: ''')
    if what_to_do_now == 'm':
        display_overview()
    elif what_to_do_now == 'w':
        episode_to_watch = int(input(' Enter [Episode] number to watch episode: '))
        try:
            toggle_episode_watched(title, season, episode_to_watch)
        except IndexError:
            display_season(title, season)
    elif what_to_do_now == 'a':
        for episode in range(1, len(season_list)):
            toggle_episode_watched(title, season, episode)
    elif what_to_do_now == 'b':
        display_tvshow(title)
    display_season(title, season)


def get_watch_status(title, season):
    season_path = 'tvshows/' + title + '/' + str(season)
    season_list = ast.literal_eval(read_file(season_path))
    watched = len(re.findall('\[True', str(season_list)))
    total = len(re.findall('\[False', str(season_list))) + watched
    watch_status = '' + str(watched) + '/' + str(total)
    return watch_status


def toggle_episode_watched(title, season, episode):
    season_path = 'tvshows/' + title + '/' + title + '_' + str(season) + '.txt'
    season_list = ast.literal_eval(read_file(season_path))
    season_list[episode][0] = not season_list[episode][0]
    write_file(season_path, str(season_list))
    print(season_list[episode])


def main():
    try:
        os.mkdir('tvshows')
    except FileExistsError:
        pass
    if not os.walk('tvshows/'):
        print('NO TVSHOW ADDED, YET. PLEASE USE [+] TO ADD A NEW SHOW')
    print('\n')
    display_overview()

if 0:
    x = input('Enter show (default Deadwood)')
    show = x if x else "Deadwood"
    add_tv_show(show)
else:
    main()
