
# coding: utf-8

# # A simple WebScrape using BeautifulSoup
# ## Author: Quinn McLaughlin
# ### Credit: 
# 
# 
# BeautifulSoup Team 
#  
#  
# Colin OKeefe for 'Practical Introduction to Web Scraping in Python" 

# In[44]:

from timeit import default_timer as timer


"""
A simple WebScrape using BeautifulSoup
Author: Quinn McLaughlin

Credit: BeautifulSoup Team 
        Colin OKeefe for 'Practical Introduction to Web Scraping in Python" 
"""

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


# Some Functions Below
# 
# 
# simple_get(url)
# 
#                 reads a url, returns the raw HTML/XML of the url.
#                 
#                 
# is_good_response(resp)
# 
#                 Checks if the url request (resp) is an HTML, returns a boolean.
#                 
#                 
# log_error(error)
# 
#                 Prints the error to the console. 
#                 

# In[ ]:

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as error:
        log_error('Error during requests to {0} : {1}'.format(url, str(error)))
        return None


# In[ ]:

def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


# In[ ]:

def log_error(error):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(error)


# Looking at a simple HTML webpage: http://www.fabpedigree.com/james/mathmen.htm
# 
# 
# Bunch of info on 'Top 100 Greatest Mathemeticians of All Time' 
# 
# 
# Credit: Colin OKeefe for his blog post. 

# In[41]:

raw_HTML = simple_get('http://www.fabpedigree.com/james/mathmen.htm')
"""
    Takes the raw text and parses it into a 'Beautiful Soup' to make it easy to work with.
    
    Make sure to pass 'html.parser', even though it's the default behavior unless you want 
error warnings.
"""
html = BeautifulSoup(raw_HTML, 'html.parser')

#prints all '<li>' content from our HTML. 
for i, li in enumerate(html.select('li')):
    print(i, li.text)


# In[42]:

def get_names():
    """
    Downloads the page where the list of mathematicians is found
    and returns a list of strings, one per mathematician
    """
    url = 'http://www.fabpedigree.com/james/mathmen.htm'
    response = simple_get(url)

    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        names = set()
        for li in html.select('li'):
            for name in li.text.split('\n'):
                if len(name) > 0:
                    names.add(name.strip())
        return list(names)

    # Raise an exception if we failed to get any data from the url
    raise Exception('Error retrieving contents at {}'.format(url))


# In[43]:

def get_hits_on_name(name):
    """
    Accepts a `name` of a mathematician and returns the number
    of hits that mathematician's wikipedia page received in the 
    last 60 days, as an `int`
    """
    # url_root is a template string that used to buld a URL.
    url_root = 'https://xtools.wmflabs.org/articleinfo/en.wikipedia.org/{}'
    response = simple_get(url_root.format(name))

    if response is not None:
        html = BeautifulSoup(response,'html.parser')

        hit_link = [a for a in html.select('a')
                    if a['href'].find('latest-60') > -1]

        if len(hit_link) > 0:
            # Strip commas:
            link_text = hit_link[0].text.replace(',','')
            try:
                # Convert to integer
                return int(link_text)
            except:
                log_error('couldn\'t parse {} as an \`int\`'.format(link_text))
                          
    log_error('No pageviews found for {}'.format(name))
    return None


# In[39]:

'''
Main Method
'''
if __name__ == '__main__':
    print('Getting the list of names....')
    names = get_names()
    print('... done.\n')

    results = []

    print('Getting stats for each name....')

    for name in names:
        try:
            hits = get_hits_on_name(name)
            if hits is None:
                hits = -1
            results.append((hits, name))
        except:
            results.append((-1, name))
            log_error('error encountered while processing '
                      '{}, skipping'.format(name))

    print('... done.\n')

    results.sort()
    results.reverse()

    if len(results) > 5:
        top_marks = results[:5]
    else:
        top_marks = results

    print('\nThe most popular mathematicians are:\n')
    for (mark, mathematician) in top_marks:
        print('{} with {} page views'.format(mathematician, mark))

    no_results = len([res for res in results if res[0] == -1])
    print('\nBut we did not find results for '
          '{} mathematicians on the list'.format(no_results))


# In[ ]:



