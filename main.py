import pkgs.wikipydia as wipy
import re
from html2text import html2text
import os
import glob
import pprint
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
    print('_________EXEC', write_file.__name__)

    file = open(file_name, 'w')
    file.write(content)
    file.close()
    return file_name


def read_file(file_name):
    print('_________EXEC', read_file.__name__)

    file = open(file_name, 'r')
    content = file.read()
    return content


class ErrorMessages:

    index_error_msg = 'We cannot find your TV Show. Maybe you have a type in there?'


class TVShow:

    def __init__(self, title):
        print('_________EXEC', self.__init__.__name__)

        self.title = title
        self.output_file = 'tmp' + path_sep + '_'.join(self.title.split()) + '_output.html'
        write_file(self.output_file, '')
        self.tables = []
        self.table_rows = []
        self.episodes = []
        self.seasons = int
        # print('self.seasons:', self.seasons)
        self.html_tables = ''

    def get_wiki_link(self):
        print('_________EXEC', self.get_wiki_link.__name__)

        search_query = 'list of ' + self.title + ' episodes'
        wiki_link = wipy.opensearch(search_query)[-1][0]
        return wiki_link

    def get_wiki_code(self):
        print('_________EXEC', self.get_wiki_code.__name__)

        wiki_link = self.get_wiki_link()
        tv_show_code = wiki_link.split('wiki/')[1]
        return tv_show_code

    def get_content(self):
        print('_________EXEC', self.get_content.__name__)

        try:
            wipy.query_text_rendered(self.get_wiki_code()[1])
            pass
        except IndexError:
            print(ErrorMessages.index_error_msg)
            raise
        write_file(self.output_file,
                   wipy.query_text_rendered(self.get_wiki_code())['html'])

    def handle_links(self, handle='remove'):
        print('_________EXEC', self.handle_links.__name__)

        if handle == 'fix':
            fixed_links = re.sub(r'<a href="/', wiki_link_prefix, read_file(self.output_file))
            write_file(self.output_file, fixed_links)
            return fixed_links
        elif handle == 'remove':
            no_links = re.sub(r'</?a.*?>', '', read_file(self.output_file))
            write_file(self.output_file, no_links)
            return no_links

    def get_no_of_seasons(self):
        print('_________EXEC', self.get_no_of_seasons.__name__)

        no_of_seasons = len(re.findall(season_table_start, read_file(self.output_file)))
        return no_of_seasons

    def get_no_of_episodes(self, table):
        print('_________EXEC', self.get_no_of_episodes.__name__)

        no_of_episodes = len(re.findall('vevent', table))
        return no_of_episodes

    def get_no_of_table_rows(self, table):
        print('_________EXEC', self.get_no_of_table_rows.__name__)

        no_of_table_rows = len(re.findall(table_row_start, table))
        return no_of_table_rows

    def strip_content(self):
        print('_________EXEC', self.strip_content.__name__)

        file = read_file(self.output_file)
        self.seasons = self.get_no_of_seasons()
        for number in range(self.seasons):
            self.tables.append(season_table_start +
                               file.split(season_table_start)[number + 1].split(table_end)[0] +
                               table_end)
            if 'vevent' not in self.tables[-1]:  # could be faster, if if before append
                self.tables.remove(self.tables[-1])
        self.seasons = self.get_no_of_seasons()
        write_file(self.output_file, ''.join(self.tables))
        # pprint.pprint(''.join(self.tables))  # is correct, error in build_html!
        return self.tables

    def get_table_rows(self, table):
        print('_________EXEC', self.get_table_rows.__name__)

        for number in range(self.get_no_of_table_rows(table)):
            table_row = '' + \
                        table_row_start + \
                        table.split(table_row_start)[number + 1].split(table_row_end)[0] + \
                        table_row_end
            if 'vevent' or 'Title' in table_row:
                self.table_rows.append(table_row)
        return self.table_rows

    def strip_html_to_table_rows(self, season):
        print('_________EXEC', self.strip_html_to_table_rows.__name__)
        print('Season:', season)

        # headers = re.sub('\n', '', html2text(self.get_table_rows(self.tables[season - 1])[0])).split('|')
        tmp_episodes = []

        table_rows = self.get_table_rows(self.tables[season - 1])
        # print('tablerows', table_rows)
        for episode in range(len(table_rows)):
            tmp_episodes.append(re.sub('\n',
                                       '',
                                       html2text(table_rows[episode])).split('|'))

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
        print('_________EXEC', self.create_episode_dict.__name__)

        # headers = re.sub('\n', '', html2text(self.get_table_rows(self.tables[0])[0])).split('|')
        season_dict = {row[0]: list(row[1:]) for row in zip(*self.strip_html_to_table_rows(season))}
        return season_dict

    def dict_to_html(self, season):
        print('_________EXEC', self.dict_to_html.__name__)

        season_dict = self.create_episode_dict(season)
        tags = [tag for tag in season_dict.keys()]
        rows = zip(*[season_dict[tag] for tag in tags])
        return dict(rows=rows, colnames=tags)

    def dict_to_html_table(self, dictionary):
        print('_________EXEC', self.dict_to_html_table.__name__)

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

    def build_html_body(self):
        print('_________EXEC', self.build_html_body.__name__)
        html_tables = ''
        self.seasons = self.get_no_of_seasons()
        print('All Seasons: ', self.seasons)
        for season in range(1, self.seasons + 1):

            table = '''<table class="rwd-table align="center">
            <h2>Season %s</h2>
            <tr>
            <th>Episode</th>
            <th>Title</th>
            <th>Date</th>
            <th>Watched</th>
            </tr>
            %s
            </table>''' % (str(season), self.dict_to_html_table(self.create_episode_dict(season)))

            html_tables += table
            print(season)
            # pprint.pprint(table)
        return html_tables

    def build_html(self):
        print('_________EXEC', self.build_html.__name__)

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
        </html>''' % (self.title, self.title, self.build_html_body())

        season_file = self.output_file  # self.output_file.split('.html')[0] + '_' + str(season) + '.html'

        write_file(season_file, body)

    def build_html_overview(self):
        print('_________EXEC', self.build_html_overview.__name__)

        for f in glob.glob('./tmp/*output.html'):
            os.remove(f)
        seasons = []
        html_files = glob.glob('./tmp/*.html')
        for file in html_files:
            f = file.split('tmp/')[1]
            tv_show = f.split('_output_')[0]
            season = f.split('_output_')[1].split('.html')[0]
            tup = [tv_show, season, file]
            seasons.append(tup)
        # for s in seasons:
            # print(s)


def run(tv_show):
    print('_________EXEC', run.__name__, tv_show)

    tvs = TVShow(tv_show)
    tvs.get_content()
    tvs.handle_links()
    tvs.strip_content()

    tvs.build_html()

    # tvs.build_html_overview()

    # print(tvs.get_wiki_link(), '\n', tvs.get_wiki_code())
    # write_file(tvs.output_file, ''.join(tvs.tables))
    # pprint.pprint(tvs.create_episode_dict(1))
    # tvs.build_html(1)

# run('Greys Anatomy')
# run('The Blacklist')
run('Vikings')
# run('Sherlock')
# run('The Simpsons', 1)


# for s in range(1, 27):
#     run('The Simpsons', s)

pprint.pprint('Finished :*')
