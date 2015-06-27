import pkgs.wikipydia as wipy
import re
import xml.etree.ElementTree as ElTree
# import os

wiki_link_prefix = '<a href="http://en.wikipedia.org/'

output = 'tmp/output.html'
links_removed = 'tmp/removed_links.html'
links_fixed = 'tmp/fixed_links.html'

standard_encoding = 'utf-8'

season_table_start = '<table class="wikitable plainrowheaders" style="width'
table_end = '</table>'

table_row_start = '<tr'
table_row_end = '</tr>'

table_date_start = '<td'
table_date_end = '</td>'


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
        self.output_file = 'tmp/' + title + '_output.html'
        self.tables = []
        self.table_rows = []
        self.episodes = []
        self.seasons = self.get_no_of_seasons()

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
            return fixed_links
        elif handle == 'remove':
            no_links = re.sub(r'</?a.*?>', '', read_file(self.output_file))
            return no_links

    def get_no_of_seasons(self):
        no_of_seasons = len(re.findall(season_table_start, read_file(self.output_file)))
        return no_of_seasons

    def get_no_of_episodes(self, table):
        no_of_episodes = re.findall('vevent', table)
        return no_of_episodes

    def get_no_of_table_rows(self, table):
        no_of_table_rows = len(re.findall(table_row_start, table))
        return no_of_table_rows

    def strip_content(self):
        for number in range(self.get_no_of_seasons()):
            self.tables.append(season_table_start +
                               read_file(self.output_file).split(season_table_start)[number + 1].split(table_end)[0] +
                               table_end)
        write_file(self.output_file, ''.join(self.tables))
        return self.tables

    def get_table_rows(self, table):
        for number in range(self.get_no_of_table_rows(table)):
            self.table_rows.append(table_row_start +
                                   table.split(table_row_start)[number + 1].split(table_row_end)[0] +
                                   table_row_end)
        return self.table_rows

    def create_episode_dict(self, season):
        tmp_episodes = []
        for episode in range(self.get_no_of_episodes(self.tables[0])):
            tmp_episodes.append(filter(None,
                                       ''.join(ElTree.fromstring(self.get_table_rows(
                                           self.tables[season - 1])[episode]).itertext()).split('\n')))
        for episode in self.episodes:
            episodes = [episode[1],
                        episode[self.episodes[0].index('Title')],
                        episode[self.episodes[0].index('Original air date')]]
            self.episodes.append(episodes)




vikings = TVShow('Vikings')
print('Wiki Link:\n', vikings.get_wiki_link())
print('Wiki Code:\n', vikings.get_wiki_code())
vikings.get_content()
write_file(vikings.output_file, vikings.handle_links())
vikings.strip_content()
print('Number of seasons:\n', vikings.seasons)
print(vikings.get_table_rows(vikings.tables[0]))

