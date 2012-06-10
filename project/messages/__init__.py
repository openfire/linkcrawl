# -*- coding: utf-8 -*-
## Project RPC Messages Init
from protorpc import messages


###### ==== Objects ==== ######
class QueuedURLMessage(messages.Message):

	''' Represents a queued URL. '''

	key = messages.StringField(1)
	url = messages.StringField(2)
	started = messages.BooleanField(3)
	parent = messages.StringField(4)
	parent_url = messages.StringField(5)
	modified = messages.StringField(6)
	created = messages.StringField(7)
	status_code = messages.IntegerField(8)
	task_id = messages.StringField(9)
	finished = messages.BooleanField(10)
	scraped_page = messages.StringField(11)


class ScrapedPageMessage(messages.Message):

	''' Represents a scraped page. '''

	key = messages.StringField(1)
	queued_url = messages.MessageField(QueuedURLMessage, 2)
	full_content = messages.StringField(3)
	main_content_section = messages.StringField(4)
	left_sidebar_content = messages.StringField(5)
	right_sidebar_content = messages.StringField(6)
	modified = messages.StringField(7)
	created = messages.StringField(8)
	task_id = messages.StringField(9)


class ScrapedPagesMessage(messages.Message):

	''' Represents a list of scraped pages. '''

	count = messages.IntegerField(1)
	pages = messages.MessageField(ScrapedPageMessage, 2, repeated=True)


###### ==== URL Management ==== ######
class AddURL(messages.Message):

	''' Add a URL to the crawl list '''

	url = messages.StringField(1)
	parent = messages.StringField(2, default=None)


class AddURLResponse(messages.Message):

	''' Response to a request to add a URL to the crawl list '''

	added = messages.BooleanField(1, default=False)
	newcount = messages.IntegerField(2, default=1)
	queued_url = messages.MessageField(QueuedURLMessage, 3)


###### ==== Crawler Management ==== ######
class CrawlStatus(messages.Message):

	''' Represents a status message about the crawler. '''

	total_queued = messages.IntegerField(1, default=0)
	queued_urls = messages.MessageField(QueuedURLMessage, 2, repeated=True)
	total_pending = messages.IntegerField(3, default=0)
	pending_urls = messages.MessageField(QueuedURLMessage, 4, repeated=True)
	total_finished = messages.IntegerField(5, default=0)
	finished_urls = messages.MessageField(QueuedURLMessage, 6, repeated=True)
