# -*- coding: utf-8 -*-

"""

    URL definitions.

"""

from webapp2 import Route
from webapp2_extras.routes import HandlerPrefixRoute

rules = [

    HandlerPrefixRoute('project.handlers.', [

        ## === Main URLs === ##
        Route('/', name='landing', handler='main.Landing'),
        Route('/offline', name='offline', handler='main.Offline'),
        Route('/_action/enqueue', name='enqueue', handler='main.QueueURL'),
        Route('/_action/scrape', name='scrape', handler='main.ScrapeURL'),

        ## === Security URLs === ##
        HandlerPrefixRoute('security.', [

            Route('/login', name='auth/login', handler='Login'),
            Route('/logout', name='auth/logout', handler='Logout'),
            Route('/register', name='auth/register', handler='Register'),

        ])

    ])
]
