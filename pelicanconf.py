#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'moormaster'
SITENAME = 'CTF writeups'
SITEURL = ''

PATH = 'content'

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
MENUITEMS = (('CTFs', '/CtfWriteups/category/ctfs.html'),
             ('Categories', '/CtfWriteups/categories.html'),
             ('Tags', '/CtfWriteups/tags.html'),
             ('Authors', '/CtfWriteups/authors.html'),)

# Social widget
SOCIAL = ()

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
