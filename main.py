# import database
# import sqlite3
# import lxml
# from bs4 import BeautifulSoup

import wikipydia
import re


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
    write_html('tmp/output.html',
               wikipydia.query_text_rendered(get_tv_show_code(tv_show)[1])['html'].encode('ascii', 'ignore'))


def get_tables(file_name):
    tables = []
    for number in range(get_number_of_tables(file_name)):
        tables.append(tableStart + read_html(file_name).split(tableStart)[number + 1].split(tableEnd)[0] + tableEnd)
    write_html('tmp/tables.html', ''.join(tables))
    return tables


def fix_links(file_name):
    content = read_html(file_name)
    fixed_links = re.sub(r'<a href="/', wikiLinkPrefix, content)
    write_html('tmp/fixed_links.html', fixed_links)


def write_html(file_name, content):
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


def get_episodes(table):
    episodes = re.findall('vevent', table)
    return episodes


def get_table_row_data(table):
    episodes = get_episodes(table)
    table_row_data = re.compile(r'<td.*>')
    write_html('tmp/strip.html', table_row_data.sub('', ''.join(episodes)))


def test():
    tv_show = input('TV Show: ')
    crawl(tv_show)
    get_tables('tmp/output.html')
    fix_links('tmp/tables.html')

# test()

vikings_s1 = ['<tr style="color:white;">\n<th style="background:#33373b;width:6%">No. in<br />\nseries</th>\n<th style="background:#33373b;width:6%">No. in<br />\nseason</th>\n<th style="background:#33373b;width:18%">Title</th>\n<th style="background:#33373b;width:20%">Directed by</th>\n<th style="background:#33373b;width:20%">Written by</th>\n<th style="background:#33373b;width:17%">Original air date</th>\n<th style="background:#33373b;width:13%">U.S. viewers<br />\n(million)</th>\n</tr>',
 '<tr class="vevent" style="text-align:center;background:inherit">\n<th scope="row" id="ep1" style="text-align:center">1</th>\n<td>1</td>\n<td class="summary" style="text-align:left">"Rites of Passage"</td>\n<td><a href="http://en.wikipedia.org/wiki/Johan_Renck" title="Johan Renck" class="mw-redirect">Johan Renck</a></td>\n<td><a href="http://en.wikipedia.org/wiki/Michael_Hirst_(writer)" title="Michael Hirst (writer)">Michael Hirst</a></td>\n<td>March&#160;3,&#160;2013<span style="display:none">&#160;(<span class="bday dtstart published updated">2013-03-03</span>)</span></td>\n<td>6.21<sup id="cite_ref-4" class="reference"><a href="#cite_note-4"><span>[</span>4<span>]</span></a></sup></td>\n</tr>',
 '<tr class="vevent" style="text-align:center;background:inherit">\n<th scope="row" id="ep2" style="text-align:center">2</th>\n<td>2</td>\n<td class="summary" style="text-align:left">"Wrath of the Northmen"</td>\n<td>Johan Renck</td>\n<td>Michael Hirst</td>\n<td>March&#160;10,&#160;2013<span style="display:none">&#160;(<span class="bday dtstart published updated">2013-03-10</span>)</span></td>\n<td>4.62<sup id="cite_ref-5" class="reference"><a href="#cite_note-5"><span>[</span>5<span>]</span></a></sup></td>\n</tr>',
 '<tr class="vevent" style="text-align:center;background:inherit">\n<th scope="row" id="ep3" style="text-align:center">3</th>\n<td>3</td>\n<td class="summary" style="text-align:left">"Dispossessed"</td>\n<td>Johan Renck</td>\n<td>Michael Hirst</td>\n<td>March&#160;17,&#160;2013<span style="display:none">&#160;(<span class="bday dtstart published updated">2013-03-17</span>)</span></td>\n<td>4.83<sup id="cite_ref-6" class="reference"><a href="#cite_note-6"><span>[</span>6<span>]</span></a></sup></td>\n</tr>',
 '<tr class="vevent" style="text-align:center;background:inherit">\n<th scope="row" id="ep4" style="text-align:center">4</th>\n<td>4</td>\n<td class="summary" style="text-align:left">"Trial"</td>\n<td><a href="http://en.wikipedia.org/wiki/Ciaran_Donnelly_(director)" title="Ciaran Donnelly (director)">Ciarn Donnelly</a></td>\n<td>Michael Hirst</td>\n<td>March&#160;24,&#160;2013<span style="display:none">&#160;(<span class="bday dtstart published updated">2013-03-24</span>)</span></td>\n<td>4.54<sup id="cite_ref-7" class="reference"><a href="#cite_note-7"><span>[</span>7<span>]</span></a></sup></td>\n</tr>',
 '<tr class="vevent" style="text-align:center;background:inherit">\n<th scope="row" id="ep5" style="text-align:center">5</th>\n<td>5</td>\n<td class="summary" style="text-align:left">"Raid"</td>\n<td>Ciarn Donnelly</td>\n<td>Michael Hirst</td>\n<td>March&#160;31,&#160;2013<span style="display:none">&#160;(<span class="bday dtstart published updated">2013-03-31</span>)</span></td>\n<td>4.74<sup id="cite_ref-8" class="reference"><a href="#cite_note-8"><span>[</span>8<span>]</span></a></sup></td>\n</tr>',
 '<tr class="vevent" style="text-align:center;background:inherit">\n<th scope="row" id="ep6" style="text-align:center">6</th>\n<td>6</td>\n<td class="summary" style="text-align:left">"Burial of the Dead"</td>\n<td>Ciarn Donnelly</td>\n<td>Michael Hirst</td>\n<td>April&#160;7,&#160;2013<span style="display:none">&#160;(<span class="bday dtstart published updated">2013-04-07</span>)</span></td>\n<td>3.31<sup id="cite_ref-9" class="reference"><a href="#cite_note-9"><span>[</span>9<span>]</span></a></sup></td>\n</tr>',
 '<tr class="vevent" style="text-align:center;background:inherit">\n<th scope="row" id="ep7" style="text-align:center">7</th>\n<td>7</td>\n<td class="summary" style="text-align:left">"A King\'s Ransom"</td>\n<td><a href="http://en.wikipedia.org/wiki/Ken_Girotti" title="Ken Girotti">Ken Girotti</a></td>\n<td>Michael Hirst</td>\n<td>April&#160;14,&#160;2013<span style="display:none">&#160;(<span class="bday dtstart published updated">2013-04-14</span>)</span></td>\n<td>3.42<sup id="cite_ref-10" class="reference"><a href="#cite_note-10"><span>[</span>10<span>]</span></a></sup></td>\n</tr>',
 '<tr class="vevent" style="text-align:center;background:inherit">\n<th scope="row" id="ep8" style="text-align:center">8</th>\n<td>8</td>\n<td class="summary" style="text-align:left">"Sacrifice"</td>\n<td>Ken Girotti</td>\n<td>Michael Hirst</td>\n<td>April&#160;21,&#160;2013<span style="display:none">&#160;(<span class="bday dtstart published updated">2013-04-21</span>)</span></td>\n<td>3.85<sup id="cite_ref-11" class="reference"><a href="#cite_note-11"><span>[</span>11<span>]</span></a></sup></td>\n</tr>',
 '<tr class="vevent" style="text-align:center;background:inherit">\n<th scope="row" id="ep9" style="text-align:center">9</th>\n<td>9</td>\n<td class="summary" style="text-align:left">"All Change"</td>\n<td>Ken Girotti</td>\n<td>Michael Hirst</td>\n<td>April&#160;28,&#160;2013<span style="display:none">&#160;(<span class="bday dtstart published updated">2013-04-28</span>)</span></td>\n<td>3.58<sup id="cite_ref-12" class="reference"><a href="#cite_note-12"><span>[</span>12<span>]</span></a></sup></td>\n</tr>']

vikings_s1_e1 = vikings_s1[1]
