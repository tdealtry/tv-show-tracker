# tvshowtracker by wohfab
A python based (not yet, but hopefully soon) web-controllable TV Show tracker to keep track of TV Shows. 


## Features

- Get Wikipedia URL of TVShow  `get_tv_show_link(title)`
- Get Wikipedia Code of TVShow `get_tv_show_code(title)`
- Get HTML Content of Wikipedia page `crawl(tv_show)`
- Strip down HTML content to *tables only* `get_tables(file_name)`
- Convert the relative links to absolute links `fix_links(file_name)`
- Input / Output functions `read_html(file_name)` and `write_html(file_name, content)`
- ~Number of seasons in TVShow `get_number_of_tables(file_name)` 
- Number of episodes in season `get_number_of_table_rows(table)`
- List of episodes in season `get_table_rows(table)`
- Episodes in table `get_episodes(table)`
- Remove HTML td-tags in table `get_table_row_data(table)`
  - Not working, yet

## Test function

- TVShow as user input
- Crawl HTML content - gives `output.html`
- Strip down to *tables only* - gives `tables.html`
- Fix the links to absolute links - gives `fixed_links.html`
