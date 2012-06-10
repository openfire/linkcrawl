# -*- coding: utf-8 -*-
## Project Services Init
import logging
from protorpc import remote
from protorpc import message_types

from apptools import BaseService
from project.models import QueuedURL
from project.models import ScrapedPage

from project.handlers.main import add_url

from project.messages import AddURL
from project.messages import CrawlStatus
from project.messages import AddURLResponse
from project.messages import QueuedURLMessage
from project.messages import ScrapedPageMessage
from project.messages import ScrapedPagesMessage

from google.appengine.ext import ndb


class CrawlService(BaseService):

	''' Crawler Management Service '''

	def _getstatus(self):
		
		''' Prepare and return the crawler's current status. '''

		queued = QueuedURL.query().filter(QueuedURL.started == False)
		pending = QueuedURL.query().filter(QueuedURL.started == True).filter(QueuedURL.finished == False)
		finished = QueuedURL.query().filter(QueuedURL.finished == True)

		queued_count = queued.count()
		pending_count = pending.count()
		finished_count = finished.count()

		if queued_count > 0:
			queued_urls = queued.fetch(queued_count)
		else:
			queued_urls = []

		if pending_count > 0:
			pending_urls = pending.fetch(pending_count)
		else:
			pending_urls = []

		if finished_count > 0:
			finished_urls = finished.fetch(finished_count)
		else:
			finished_urls = []

		status = CrawlStatus()
		status.total_queued = queued_count
		status.total_pending = pending_count
		status.total_finished = finished_count

		for status_mountpoint, group in ((status.queued_urls, queued_urls), (status.pending_urls, pending_urls), (status.finished_urls, finished_urls)):
			if len(group) > 0:
				for queued_url in group:

					## Build response fragment
					qu = QueuedURLMessage(key=queued_url.key.urlsafe())
					qu.url = queued_url.url
					qu.started = queued_url.started

					if queued_url.key.parent() is not None:
						qu.parent = queued_url.key.parent().urlsafe()
						qu.parent_url=queued_url.key.parent().id_or_name()
					
					qu.modified = str(queued_url.modified)
					qu.created = str(queued_url.created)
					
					if queued_url.status_code:
						qu.status_code = queued_url.status_code
					if queued_url.task_id:
						qu.task_id = queued_url.task_id

					status_mountpoint.append(qu)
			else:
				status_mountpoint = []

		return status

	@remote.method(AddURL, AddURLResponse)
	def add_url(self, request):

		''' Add a URL to the crawl routine '''

		logging.info('========== ADD_URL ==========')

		if request.parent is not None:
			logging.info('URL has parent.')
			p = ndb.Key(urlsafe=request.parent)
			q = QueuedURL(key=ndb.Key(k, QueuedURL, request.url), url=request.url)
			k = q.put()
		else:
			logging.info('URL has NO parent.')
			q = QueuedURL(key=ndb.Key(QueuedURL, request.url), url=request.url)
			k = q.put()

		logging.info('QueuedURL key: '+k.urlsafe())

		c = QueuedURL.query().count()

		logging.info('New URL count: '+str(c))

		## Generate response
		qu = QueuedURLMessage(key=k.urlsafe())
		qu.url = request.url
		qu.started = q.started
		if q.key.parent() is not None:
			qu.parent = q.key.parent().urlsafe()
			qu.parent_url=q.key.parent().id_or_name()
		qu.modified = str(q.modified)
		qu.created = str(q.created)
		if q.status_code:
			qu.status_code = q.status_code
		if q.task_id:
			qu.task_id = q.task_id

		return AddURLResponse(added=True, newcount=c, queued_url=qu)

	@remote.method(message_types.VoidMessage, CrawlStatus)
	def start(self, request):

		''' Begin the crawl routine '''

		global add_url

		logging.critical('========== STARTING CRAWL ROUTINE ==========')

		q = QueuedURL.query()
		c = q.count()
		qu = q.fetch(c)
		logging.info('Found '+str(c)+' queued URLs. Kicking off tasks.')
		crawl_tasks = []
		for queued_url in qu:
			logging.info('--Building task for queued URL at key "'+str(queued_url.key.urlsafe())+'"...')
			task, qu = add_url(queued_url, None, False)
			logging.info('------Built task: "'+str(task.name)+'".')
			crawl_tasks.append(task)
			logging.info('------Adding to deferred batch at index '+str(crawl_tasks.index(task))+'.')

		try:
			logging.info('Finished generating deferred batch. Kicking off tasks! :)')
			if len(crawl_tasks) > 0:
				logging.info('--Found '+str(len(crawl_tasks))+' crawltasks, which is more than 0.')
			else:
				logging.error('NO CRAWLTASKS :(')
				raise remote.ApplicationError('No crawltasks could be generated :(')
		except:
			raise

		else:
			tasks = self.api.taskqueue.Queue('crawler').add(crawl_tasks)
			logging.info('========== '+str(len(tasks))+' TASKS ENQUEUED '+'==========')

			return self._getstatus()

	@remote.method(message_types.VoidMessage, CrawlStatus)
	def status(self, request):

		''' Get crawler status info and return '''

		return self._getstatus()

	@remote.method(message_types.VoidMessage, ScrapedPagesMessage)
	def scraped(self, request):

		''' Get all stored, scraped pages '''

		pass
