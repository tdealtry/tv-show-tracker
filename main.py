import wikipydia
import re
import xml.etree.ElementTree as ElTree
import os

# tvShow = 'Vikings'
# tvShow = 'Sherlock'
# tvShow = 'Simpsons'

tableStart = '<table class="wikitable plainrowheaders" style="width'
tableEnd = '</table>'

tableRowStart = '<tr'
tableRowEnd = '</tr>'

tableDateStart = '<td'
tableDateEnd = '</td>'

wikiLinkPrefix = '<a href="http://en.wikipedia.org/'

path_sep = '/'
# For Windows use '\'


def get_tv_show_link(title):
    """Crawls the Wiki URL of the 'List of Episodes' page of the given TV Show

    @title: string - title of the TV Show
    """

    search_query = 'list of ' + title + ' episodes'
    tv_show_url = wikipydia.opensearch(search_query)[-1][0]
    return tv_show_url


def get_tv_show_code(title):
    """Gives the TV Show title and the Wiki Show Code

    @tvShowURL: string - tvShowTitleToLink(title)
    @title: string - title of the TV Show
    """

    tv_show_url = get_tv_show_link(title)
    tv_show = ''.join(tv_show_url.split('wiki/')[1].split('_')[2:-1])
    tv_show_code = tv_show_url.split('wiki/')[1]
    return [tv_show, tv_show_code]


def crawl(tv_show):
    write_file('tmp/output.html',
               wikipydia.query_text_rendered(get_tv_show_code(tv_show)[1])['html'].encode('ascii', 'ignore'))


def get_tables(file_name):
    tables = []
    for number in range(get_number_of_tables(file_name)):
        tables.append(tableStart + read_html(file_name).split(tableStart)[number + 1].split(tableEnd)[0] + tableEnd)
    write_file('tmp/tables.html', ''.join(tables))
    return tables


def fix_links(file_name):
    content = read_html(file_name)
    fixed_links = re.sub(r'<a href="/', wikiLinkPrefix, content)
    write_file('tmp/fixed_links.html', fixed_links)


def remove_links(file_name):
    content = read_html(file_name)
    removed_links = re.sub(r'</?a.*?>', '', content)
    # remove NEW LINE HTML tags
    removed_n = re.sub(r'<br />\n', ' ', removed_links)
    write_file('tmp/removed_links.html', removed_n)


def write_file(file_name, content):
    f = open(file_name, 'w')
    f.write(content)
    f.close()


def read_html(file_name):
    f = open(file_name, 'r')
    content = f.read()
    f.close()
    return content


def get_number_of_tables(file_name):
    number_of_tables = len(re.findall(tableStart, read_html(file_name)))
    return number_of_tables


def get_number_of_table_rows(table):
    number_of_table_rows = len(re.findall(tableRowStart, table))
    return number_of_table_rows


def get_table_rows(table):
    table_rows = []
    for number in range(get_number_of_table_rows(table)):
        table_rows.append(tableRowStart + table.split(tableRowStart)[number + 1].split(tableRowEnd)[0] + tableRowEnd)
    return table_rows


def get_number_of_episodes(table):
    episodes = re.findall('vevent', table)
    return len(episodes)


def create_season_dict(tv_show, season, input_file_name):
    crawl(tv_show)
    get_tables('tmp/output.html')
    remove_links('tmp/tables.html')

    episodes = []
    for episode in range(get_number_of_episodes(get_tables(input_file_name)[0])):
        episodes.append(filter(None,
                               ''.join(ElTree.fromstring(get_table_rows(
                                   get_tables(input_file_name)[
                                       season - 1])[episode]).itertext()).split('\n')))

    eps = []
    for episode in episodes:
        ep = [episode[1],
              episode[episodes[0].index('Title')],
              episode[episodes[0].index('Original air date')]]
        eps.append(ep)

    eps[0][0], eps[0][1], eps[0][2] = 'no_in_season', 'title', 'original_air_date'

    season_dict = {row[0]: list(row[1:]) for row in zip(*eps)}

    return season_dict


def safe_dict_to_file(tv_show, season, season_dict):
    season_path = 'tv_shows' + path_sep + tv_show.lower() + path_sep
    file_path = season_path + tv_show.lower() + '_' + str(season) + '.txt'
    if not os.path.isdir(season_path):
        os.makedirs(season_path)
    write_file(file_path, str(season_dict))


def __init__():
    tv_show = input('TVS: ')
    season = input('season: ')

    crawl(tv_show)
    safe_dict_to_file(tv_show, season, create_season_dict(tv_show, season, 'tmp/removed_links.html'))


__init__()
