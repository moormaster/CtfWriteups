AUTHOR = 'moormaster'
SITENAME = 'CTF writeups'
SITEURL = ""

PATH = "content"

TIMEZONE = 'Europe/Berlin'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()

DISPLAY_CATEGORIES_ON_MENU=False

def get_menuitems(site_url):
    return (     ('CTFs', f'{site_url}/category/ctfs.html'),
                 ('Categories', f'{site_url}/categories.html'),
                 ('Tags', f'{site_url}/tags.html'),
                 ('Authors', f'{site_url}/authors.html'),
                 ('Archives', f'{site_url}/archives.html'),)
MENUITEMS = get_menuitems(SITEURL)

# Social widget
SOCIAL = ()

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
