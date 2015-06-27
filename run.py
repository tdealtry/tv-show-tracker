import wikipydia
import re
import xml.etree.ElementTree as ElTree
import os

html_tables = []


def __init__(tv_show):
    crawl(tv_show)
    for season in range(1, get_number_of_tables(op) + 1):
        # safe_dict_to_file(tv_show, season, create_season_dict(tv_show, season, rl))
        html_tables.append(build_html_body(create_season_dict(season, rl)))
    build_html(tv_show, ''.join(html_tables))


# ERROR MESSAGES
tv_show_error_msg = '''I am sorry! The TV Show you have entered, cannot be found.
Maybe you forgot a "the" in the title?'''

# VALUES, VARIABLES, ETC
tableStart = '<table class="wikitable plainrowheaders" style="width'
tableEnd = '</table>'

tableRowStart = '<tr'
tableRowEnd = '</tr>'

tableDateStart = '<td'
tableDateEnd = '</td>'

wikiLinkPrefix = '<a href="http://en.wikipedia.org/'

path_sep = '/'
# For Windows: use '\'

rl = 'tmp/removed_links.html'
op = 'tmp/output.html'


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
    try:
        wikipydia.query_text_rendered(get_tv_show_code(tv_show)[1])
    except IndexError:
        print(tv_show_error_msg)

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
    write_file(rl, removed_n)


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


def create_season_dict(season, input_file_name):
    # get_tables('tmp/output.html')
    remove_links(op)

    episodes = []
    for episode in range(get_number_of_episodes(get_tables(input_file_name)[0])):
        episodes.append(filter(None,
                               ''.join(ElTree.fromstring(get_table_rows(
                                   get_tables(input_file_name)[season - 1])[episode]).itertext()).split('\n')))

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


def dict_to_html(season, input_file_name):
    season_dict = create_season_dict(season, input_file_name)
    tags = [tag for tag in season_dict.keys()]
    rows = zip(*[season_dict[tag] for tag in tags])
    return dict(rows=rows, colnames=tags)


def dict_to_html_table(dictionary):
    html_table = ''

    checkbox = '''<input type="button" class="css-button" value="watch">
    '''

    tr = '''<tr>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    </tr>
    '''

    for episode in range(len(dictionary['no_in_season'])):
        html_table += tr % (dictionary['no_in_season'][episode],
                            dictionary['title'][episode],
                            dictionary['original_air_date'][episode],
                            checkbox)
    return html_table


def build_html_body(season_dict):
    table = '''
    <table class="rwd-table" align="center">
    <tr>
    <th>Episode</th>
    <th>Title</th>
    <th>Date</th>
    <th>Watched</th>
    </tr>
    %s
    </table>''' % (dict_to_html_table(season_dict))
    return table


def build_html(tv_show, tables):
    body = '''<!DOCTYPE html>
    <html lang="en">
    <head>
    <link rel="stylesheet" type="text/css" href="style.css">
        <meta charset="UTF-8">
        <title>%s</title>
    </head>
    <body>
    <h1>%s</h1>
    %s
    </body>
    </html>''' % (tv_show, tv_show, tables)

    write_file('simple.html', body.encode('utf-8', 'ignore'))


__init__(input('TVS: '))
