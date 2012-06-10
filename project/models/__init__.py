# -*- coding: utf-8 -*-
from google.appengine.ext import ndb


class QueuedURL(ndb.Model):

    ''' Represents a URL waiting to be scraped. '''

    url = ndb.StringProperty()
    started = ndb.BooleanProperty(default=False)
    parent = ndb.KeyProperty(default=None)
    modified = ndb.DateTimeProperty(auto_now=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    status_code = ndb.IntegerProperty(choices=[001, 200, 304, 404, 500])
    task_id = ndb.StringProperty()
    scraped_page = ndb.KeyProperty(default=None)
    finished = ndb.BooleanProperty(default=False)
    error = ndb.BooleanProperty(default=False)


class ScrapedPage(ndb.Model):

    ''' Represents a page after being scraped. '''

    url = ndb.StringProperty()
    queued_url = ndb.KeyProperty()
    full_content = ndb.TextProperty()
    main_content_section = ndb.TextProperty(default=None)
    left_sidebar_content = ndb.TextProperty(default=None)
    right_sidebar_content = ndb.TextProperty(default=None)
    modified = ndb.DateTimeProperty(auto_now=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    task_id = ndb.StringProperty()