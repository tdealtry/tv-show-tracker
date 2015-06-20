import wikipydia

def get_tv_show_link(title):
    """Crawls the Wikipedia URL of the 'List of Episodes' page of the given TV Show
    
    @title: string - title of the TV Show 
    """
     
    search_query = "list of " + title + " episodes"
    tv_show_url = wikipydia.opensearch(search_query)[-1][0]
    return tv_show_url

    
def get_tv_show_code(title):
    """Gives the TV Show title and the Wikipedia Show Code
    
    @tvShowURL: string - tvShowTitleToLink(title)
    @title: string - title of the TV Show    
    """
    
    tv_show_url = get_tv_show_link(title)
    tv_show = "".join(tv_show_url.split('wiki/')[1].split('_')[2:-1])
    tv_show_code = tv_show_url.split('wiki/')[1]
    return [tv_show, tv_show_code]
