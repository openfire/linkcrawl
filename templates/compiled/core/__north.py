from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source/core/__north.html'

    def root(context, environment=environment):
        l_asset = context.resolve('asset')
        l_page = context.resolve('page')
        if 0: yield None
        yield u'<title>'
        for event in context.blocks['title'][0](context):
            yield event
        yield u'</title>\n\n<!-- Stylesheets -->\n<style>@import url(http://fonts.googleapis.com/css?family=Satisfy);</style>\n<link rel="stylesheet" href="%s">\n\n' % (
            context.call(environment.getattr(l_asset, 'style'), 'main', 'compiled'), 
        )
        if environment.getattr(l_page, 'ie'):
            if 0: yield None
            yield u'\n\t<link rel="stylesheet" href="%s">\n' % (
                context.call(environment.getattr(l_asset, 'style'), 'ie', 'compiled'), 
            )

    def block_title(context, environment=environment):
        l_page = context.resolve('page')
        l_title = context.resolve('title')
        if 0: yield None
        if environment.getattr(l_page, 'title'):
            if 0: yield None
            yield to_string(environment.getattr(l_page, 'title'))
        else:
            if 0: yield None
            if l_title:
                if 0: yield None
                yield to_string(l_title)

    blocks = {'title': block_title}
    debug_info = '1=11&5=14&7=16&8=19&1=22'
    return locals()