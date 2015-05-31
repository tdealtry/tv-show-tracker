import wikipydia

def tvShowTitleToLink(title):
    """Crawls the Wikipedia URL of the 'List of Episodes' page of the given TV Show
    
    @title: string - title of the TV Show 
    """
    
    searchQuery = "list of " + title + " episodes"
    tvShowURL = wikipydia.opensearch(searchQuery)[-1][0]
    return tvShowURL
    
def tvShowLinkToCode(tvShowURL):
    """Gives the TV Show title and the Wikipedia Show Code
    
    @tvShowURL: string - tvShowTitleToLink(title)
    @title: string - title of the TV Show    
    """
    tvShow = "".join(tvShowURL.split('wiki/')[1].split('_')[2:-1])
    tvShowCode = tvShowURL.split('wiki/')[1]
    return [tvShow, tvShowCode]
    