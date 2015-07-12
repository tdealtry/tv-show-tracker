import re
import os
# import sys
# import time
import fw_wiki as wipy
# import pprint

from lxml import html
from lxml.html.clean import clean_html
from lxml import etree

import ast  # string to list

wiki_link_prefix = '<a href="http://en.wikipedia.org/'

output = 'tmp/output.html'
links_removed = 'tmp/removed_links.html'
links_fixed = 'tmp/fixed_links.html'

standard_encoding = 'utf-8'

# season_table_start
s_t_s = '<table class="wikitable plainrowheaders"'
table_end = '</table>'

table_row_start = '<tr class="vevent"'
table_row_end = '</tr>'

table_date_start = '<td'
table_date_end = '</td>'

episodes_start = 'id="Episode'

path_sep = '/'
# win = '\'

index_error_msg = 'We cannot find your TV Show. Maybe you have a type in there?'


def clear_screen():
    os.system(['clear', 'cls'][os.name == 'nt'])
    # time.sleep(0.5)
    

def write_file(file_name, content):
    # print('_________EXEC', write_file.__name__)

    file = open(file_name, 'w')
    file.write(content)
    file.close()
    return file_name


def read_file(file_name):
    # print('_________EXEC', read_file.__name__)

    file = open(file_name, 'r')
    content = file.read()
    return content


def add_tv_show(title):
    # print(title)
    title_code = re.sub(' ', '_', title)
    tv_show_folder = 'tvshows/' + title_code
    # title_file = tv_show_folder + '/' + title_code + '.html'

    if not os.path.exists(tv_show_folder):
        os.mkdir(tv_show_folder)
    # print(tv_show_folder)

    clear_screen()

    search = 'list of ' + title + ' episodes'
    wiki_link = wipy.opensearch(search)[-1][0]
    # print('WikiLink: ' + wiki_link)

    wiki_code = wiki_link.split('wiki/')[1]
    # print('WikiCode: ' + wiki_code)

    wiki_content = wipy.query_text_rendered(wiki_code)['html']
    # print('Content : ' + wiki_content[:80])

    wiki_content = clean_html(wiki_content)  # remove style etc.
    wiki_content = re.sub(r'<br ?/?>\n', ' ', wiki_content)
    # print('Cleaned : ' + wiki_content[:80])

    wiki_content = wiki_content.split(episodes_start)[1]
    # print('NoPreTbl: ' + wiki_content[:80])

    wiki_content = re.sub(r'</?a.*?>', '', wiki_content)
    # print('NoLinks : ' + wiki_content[:80])
        
    no_of_tables = len(re.findall(s_t_s, wiki_content))
    # print('Tables  : ' + str(no_of_tables))

    # no_of_episodes = len(re.findall('vevent', wiki_content))
    # print('Episodes: ' + str(no_of_episodes))

    seasons = [s_t_s +
               wiki_content.split(s_t_s)[season + 1].split(table_end)[0] +
               table_end
               for season in range(no_of_tables) if 'vevent' in
               s_t_s +
               wiki_content.split(s_t_s)[season + 1].split(table_end)[0] +
               table_end]
    # print('Seasons : ' + str(len(seasons)))

    # wiki_content = ''.join(seasons)
    i = 1
    for season in seasons:
        
        # print(seasons.index(season) + 1)
        season_file_name = 'tvshows/' + title_code + '/' + title_code + '_' + str(seasons.index(season) + 1) + '.txt'
        # print(season_file_name)
        
        doc_root = html.fromstring(season)
        
        # headers = doc_root.xpath('//table/tr/th//text()')
        # only keep Episode Number and Title
#        header = [header for header in headers if
#                  'No.' in header or
#                  'season' in header or
#                  'Season' in header or
#                  'title' in header or
#                  'Title' in header or
#                  'webisode' in header]
        header = ['Number in series', 'Number in season', 'Title']

        eps = doc_root.xpath('//table/tr[@class="vevent"]/td[@class="summary"]//text()')
        ep = [ep for ep in eps if len(ep) > 2]

        episodes = []
        for e in ep:
            episodes.append([i, ep.index(e) + 1, re.sub('"', '', e)])
            i += 1
        episodes.insert(0, header)
        write_file(season_file_name, str(episodes))

    # delete unused columns
    nc = ''
    for season in seasons:
        table = html.fragment_fromstring(season)
        for row in table.iterchildren():
            row.remove(row.getchildren()[0])
        nc += html.tostring(table).decode('utf-8')

    tvs = []
    for season in seasons:
        table = etree.XML(season)
        rows = iter(table)
        headers = [col.text.lower() for col in next(rows)]
        for row in rows:
            values = [col.text for col in row]
            tvs.append(list(zip(headers, values)))

    # os.system('firefox tmp/output.html')

    # CLEAN
    # print('\n')
    return seasons


def delete_tv_show(title):
    remove_tv_show = 'rm -rf ' + 'tvshows/' + re.sub(' ', '_', title)
    os.system(remove_tv_show)


def start_from_scratch():
    remove_everything = 'rm -rf tvshows/*'
    os.system(remove_everything)


def display_overview():
    path = 'tvshows/'
    for path, dirs, files in os.walk(path):
        dirs.sort()
        for directory in dirs:
            print('[', dirs.index(directory) + 1, ']\t',
                  re.sub('_', ' ', directory))


def display_tvshow(title):
    title_code = re.sub(' ', '_', title).lower()    
    path = 'tvshows/'.format(title_code)
    for path, dirs, files in os.walk(path):
        files.sort()
        for season in files:
            print('[', files.index(season) + 1, ']\t',
                  'Season', season.split('_')[-1].split('.')[0])


def display_season(title_code, season):
    season_path = 'tvshows/' + title_code + '/' + title_code + '_' + season + '.txt'
    season_list = ast.literal_eval(read_file(season_path))
    for episode in season_list:
        ep = '' + str(episode[1]) + '(' + str(episode[0]) + ')' + episode[2]
        print(ep)


##########################################
##
# TEST
##
##########################################

    
# add_tv_show(sys.argv[1])

not_working = ['sherlock',
               'person of interest',
               'true detective',
               'family guy'
               ]

tvshows = ['game of thrones',
           'breaking bad',
           'the wire',
           # 'the big bang theory',
           # 'the walking dead',
           #          'dexter',
           #          'how i met your mother',
           #          'arrow',
           #          'homeland',
           #          'fringe',
           #          'lost',
           #          'house',
           #          'suits',
           #          'supernatural',
           #          'modern family',
           #          'house of cards',
           #          'true blood',
           #          'community',
           #          'the simpsons',
           #          'once upon a time',
           #          'futurama',
           #          'south park',
           #          'the vampire diaries',
           #          'prison break',
           #          'chuck',
           #          'castle',
           #          'californication',
           #          'the mentalist',
           #          'vikings',
           #          'two and a half men'
           ]

start_from_scratch()
for show in tvshows:
    print(show)
    add_tv_show(show)

# time.sleep(2)
# start_from_scratch()

print('\n')
display_overview()
for tvshow in tvshows:
    print('\n')
    display_tvshow(tvshow)

display_season('game_of_thrones', '1')
