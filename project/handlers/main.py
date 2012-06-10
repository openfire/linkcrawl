# -*- coding: utf-8 -*-
import json
import logging

from bs4 import BeautifulSoup

from google.appengine.ext import ndb
from google.appengine.api import taskqueue

from project.models import QueuedURL
from project.models import ScrapedPage
from project.handlers import WebHandler


def get_task(qk, start=False):

	''' Low-level utility function to kick off scrape tasks. '''

	task = taskqueue.Task(params={'queued': qk.urlsafe()}, name=str(qk.urlsafe()), url='/_action/scrape', method='POST')
	if start:
		return task.add()
	return task


def add_url(key_or_url, urlparent=None, start=False):

	''' Creates a QueuedURL entity and optionally enqueues a task to scrape. '''

	global get_task

	if isinstance(key_or_url, basestring):
		url = key_or_url
		if urlparent is not None:
			if not isinstance(urlparent, (ndb.Model,ndb.Key)):
				urlparent = ndb.Key(urlparent)
			q = QueuedURL(key=ndb.Key(urlparent, 'QueuedURL', url), url=url, started=False, parent=urlparent)
		else:
			q = QueuedURL(key=ndb.Key('QueuedURL', url), url=url, started=False, parent=None)
		qk = q.put()
		t = get_task(qk, start)
		if start:
			qk.task_id = t.name

		return t, q

	elif isinstance(key_or_url, (ndb.Key, ndb.Model)):

		if isinstance(key_or_url, ndb.Key):
			key = key_or_url
			qu = ndb.Key(urlsafe=key).get()
		else:
			key = key_or_url.key
			qu = key_or_url

		if not qu.started:
			t = get_task(qu.key, start)
			qu.task_id = t.name
			return t, qu
		else:
			return qu.task_id, qu


class CrawlHandler(WebHandler):

	''' Parent class to crawler handlers that injects important utils. '''

	@staticmethod
	def enqueue(url, urlparent=None):

		''' Enqueue a URL. '''

		global add_url
		return add_url(url, urlparent, False)


class Landing(CrawlHandler):

	''' Displays URLs left to crawl. '''

	def get(self):

		queued_urls = QueuedURL.query()
		scraped_pages = ScrapedPage.query()

		qu_count = queued_urls.count()
		if qu_count < 5:
			qu_count = 5

		sc_count = scraped_pages.count()
		if sc_count < 5:
			sc_count = 5

		return self.render('main/urls.html', queued=queued_urls.fetch(qu_count), scraped=scraped_pages.fetch(sc_count))


class QueueURL(CrawlHandler):

	''' Queues a URL for scraping. '''

	def post(self):
		if 'parent' in self.request:
			task, model = self.enqueue(self.request.get('url'), self.request.get('parent'))
		else:
			task, model = self.enqueue(self.request.get('url'))
		result = json.dumps({'task': str(task), 'queued': str(model.key.urlsafe())})
		self.response.write(result)
		return


class ScrapeURL(CrawlHandler):

	''' Scrapes a URL for content. '''

	def post(self):
		key = self.request.get('queued')

		logging.info('========== STARTING SCRAPE TASK ==========')
		logging.info('--Queued Key: '+str(key))

		try:
			k = ndb.Key(urlsafe=key)
			queued_url = k.get()
			assert queued_url != None
		except AssertionError:
			logging.error('--Could not resolve queued URL.')
			self.error(200)
			return
		except Exception, e:
			logging.error('--Could not build queued URL key.')
			logging.error('--Exception: "%s"' % e)
			raise
			return

		queued_url.started = True
		queued_url.put()

		logging.info('--Pulling URL: "' + str(queued_url.url) + '".')

		result = self.api.urlfetch.fetch(queued_url.url)
		if result.status_code == 200:
			logging.info('--Status code 200. Success.')
			page = ScrapedPage(key=ndb.Key('ScrapedPage', queued_url.task_id, parent=queued_url.key), url=queued_url.url, queued_url=queued_url.key, task_id=queued_url.task_id)
			queued_url.status_code = 200

			logging.info('--Cookin\' soup.')
			soup = BeautifulSoup(result.content)

			page.full_content = soup.prettify()
			logging.info('--Retrieved full source with length ' + unicode(len(unicode(page.full_content))))

			## Check for nav
			## Check body content
			## Check left sidebar
			## Check right sidebar
			## Save, update and finish

			pk = page.put()

			logging.info('--Put page at key "'+str(pk)+'".')

			queued_url.scraped_page = pk
			queued_url.put()

			json_result = json.dumps({'result': 'success', 'errorcode': None, 'content': result.content, 'queued': queued_url.key.urlsafe(), 'page': pk.urlsafe()})
			self.response.write(json_result)
		else:
			queued_url.status_code = result.status_code
			queued_url.finished = True
			queued_url.error = True
			queued_url.put()

			result = json.dumps({'result': 'fail', 'errorcode': result.status_code, 'content': result.content, 'queued': queued_url.key.urlsafe()})
			self.reseponse.write(result)
		return

