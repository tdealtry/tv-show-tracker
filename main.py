import pkgs.wikipydia as wipy
import re
from html2text import html2text
# import os
# import pprint
# import time

wiki_link_prefix = '<a href="http://en.wikipedia.org/'

output = 'tmp/output.html'
links_removed = 'tmp/removed_links.html'
links_fixed = 'tmp/fixed_links.html'

standard_encoding = 'utf-8'

season_table_start = '<table class="wikitable plainrowheaders" '
table_end = '</table>'

table_row_start = '<tr'
table_row_end = '</tr>'

table_date_start = '<td'
table_date_end = '</td>'

path_sep = '/'
# win = '\'


def write_file(file_name, content):
    file = open(file_name, 'w')
    file.write(content)
    file.close()
    return file_name


def read_file(file_name):
    file = open(file_name, 'r')
    content = file.read()
    return content


class ErrorMessages:

    index_error_msg = 'We cannot find your TV Show. Maybe you have a type in there?'


class TVShow:

    def __init__(self, title):
        self.title = title
        self.output_file = 'tmp' + path_sep + '_'.join(self.title.split()) + '_output.html'
        write_file(self.output_file, '')
        self.tables = []
        self.table_rows = []
        self.episodes = []
        self.seasons = self.get_no_of_seasons()
        self.html_tables = ''

    def get_wiki_link(self):
        search_query = 'list of ' + self.title + ' episodes'
        wiki_link = wipy.opensearch(search_query)[-1][0]
        return wiki_link

    def get_wiki_code(self):
        wiki_link = self.get_wiki_link()
        tv_show_code = wiki_link.split('wiki/')[1]
        return tv_show_code

    def get_content(self):
        try:
            wipy.query_text_rendered(self.get_wiki_code()[1])
            pass
        except IndexError:
            print(ErrorMessages.index_error_msg)
            raise
        write_file(self.output_file,
                   wipy.query_text_rendered(self.get_wiki_code())['html'])

    def handle_links(self, handle='remove'):
        if handle == 'fix':
            fixed_links = re.sub(r'<a href="/', wiki_link_prefix, read_file(self.output_file))
            write_file(self.output_file, fixed_links)
            return fixed_links
        elif handle == 'remove':
            no_links = re.sub(r'</?a.*?>', '', read_file(self.output_file))
            write_file(self.output_file, no_links)
            return no_links

    def get_no_of_seasons(self):
        no_of_seasons = len(re.findall(season_table_start, read_file(self.output_file)))
        return no_of_seasons

    def get_no_of_episodes(self, table):
        no_of_episodes = len(re.findall('vevent', table))
        return no_of_episodes

    def get_no_of_table_rows(self, table):
        no_of_table_rows = len(re.findall(table_row_start, table))
        return no_of_table_rows

    def strip_content(self):
        for number in range(self.get_no_of_seasons()):
            self.tables.append(season_table_start +
                               read_file(self.output_file).split(season_table_start)[number + 1].split(table_end)[0] +
                               table_end)
            if 'vevent' not in self.tables[-1]:
                self.tables.remove(self.tables[-1])
        write_file(self.output_file, ''.join(self.tables))
        return self.tables

    def get_table_rows(self, table):
        for number in range(self.get_no_of_table_rows(table)):
            table_row = '' + \
                        table_row_start + \
                        table.split(table_row_start)[number + 1].split(table_row_end)[0] + \
                        table_row_end
            if 'vevent' or 'Title' in table_row:
                self.table_rows.append(table_row)
        return self.table_rows

    def strip_html_to_table_rows(self, season):
        # headers = re.sub('\n', '', html2text(self.get_table_rows(self.tables[season - 1])[0])).split('|')
        tmp_episodes = []
        for episode in range(len(self.get_table_rows(self.tables[season - 1]))):
            tmp_episodes.append(re.sub('\n',
                                       '',
                                       html2text(self.get_table_rows(
                                           self.tables[season - 1])[episode])).split('|'))

        for e in tmp_episodes:
            ep = [episode.strip() for episode in e]
            tmp_episodes[tmp_episodes.index(e)] = ep
            if len(e) < 3:
                tmp_episodes.remove(e)

        for episode in tmp_episodes:
            self.episodes.append([episode[0],
                                  episode[tmp_episodes[0].index('Title')],
                                  episode[tmp_episodes[0].index('Original air date')]])

        self.episodes[0][0], self.episodes[0][1], self.episodes[0][2] = 'no', 'title', 'date'

        for episode in self.episodes:
            for element in episode:
                episode[episode.index(element)] = element.strip()

        return self.episodes

    def create_episode_dict(self, season):
        # headers = re.sub('\n', '', html2text(self.get_table_rows(self.tables[0])[0])).split('|')
        season_dict = {row[0]: list(row[1:]) for row in zip(*self.strip_html_to_table_rows(season))}
        return season_dict

    def dict_to_html(self, season):
        season_dict = self.create_episode_dict(season)
        tags = [tag for tag in season_dict.keys()]
        rows = zip(*[season_dict[tag] for tag in tags])
        return dict(rows=rows, colnames=tags)

    def dict_to_html_table(self, dictionary):
        html_table = ''

        checkbox = '<input type="button" class="css-button" value="watch">'

        tr = '''<tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        </tr>'''

        for episode in range(len(dictionary['no'])):
            html_table += tr % (dictionary['no'][episode],
                                dictionary['title'][episode],
                                dictionary['date'][episode],
                                checkbox)

        return html_table

    def build_html_body(self, season):
        table = '''<table class="rwd-table align="center">
        <h2>Season %d</h2>
        <tr>
        <th>Episode</th>
        <th>Title</th>
        <th>Date</th>
        <th>Watched</th>
        </tr>
        %s
        </table>''' % (season, self.dict_to_html_table(self.create_episode_dict(season)))
        return table

    def build_html(self, season):

        body = '''<!DOCTYPE html>
        <html lang="en"
        <head>
        <link rel="stylesheet" type="text/css" href="style.css">
        <meta charset="UTF-8">
        <title>%s</title>
        </head>
        <body>
        <h1>%s</h1>
        %s
        </body>
        </html>''' % (self.title, self.title, self.build_html_body(season))

        season_file = self.output_file.split('.html')[0] + '_' + str(season) + '.html'

        write_file(season_file, body)


def run(tv_show):
    tvs = TVShow(tv_show)
    tvs.get_content()
    tvs.handle_links()
    tvs.strip_content()

    print(tvs.table_rows)

    print(tvs.get_wiki_link())
    print(tvs.get_wiki_code())

    for number in range(1, len(tvs.tables)):
        tvs.build_html(number)

    write_file(tvs.output_file, ''.join(tvs.tables))
    # pprint.pprint(tvs.create_episode_dict(1))
    # tvs.build_html(1)

# run('Greys Anatomy')
# run('The Blacklist')
run('Vikings')
# run('Sherlock')
