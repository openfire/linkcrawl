from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source/main/urls.html'

    def root(context, environment=environment):
        parent_template = None
        if 0: yield None
        parent_template = environment.get_template('core/base_web.html', '/source/main/urls.html')
        for name, parent_block in parent_template.blocks.iteritems():
            context.blocks.setdefault(name, []).append(parent_block)
        for event in parent_template.root_render_func(context):
            yield event

    def block_main(context, environment=environment):
        l_link = context.resolve('link')
        l_scraped = context.resolve('scraped')
        l_queued = context.resolve('queued')
        t_1 = environment.filters['truncate']
        if 0: yield None
        yield u"\n\n<!-- styles -->\n<style>.hidden { display: none; }</style>\n\n\n<!-- top bar -->\n<h1>Welcome to the link crawler :)</h1>\n\n<form id='urlform' action='%s' method='post'>\n\n<b>Queue a URL manually: <input id='addurl' type='text' name='url' placeholder='enter a URL here' />" % (
            context.call(l_link, 'enqueue'), 
        )
        if l_scraped:
            if 0: yield None
            yield u'<select id=\'parent_select\' name=\'parent_select\'>\n\t<option value="__NULL__">--Select a Nav Parent--</option>\n\t'
            l_scraped_item = missing
            for l_scraped_item in l_scraped:
                if 0: yield None
                yield u'\n\t<option value="%s">%s</option>\n\t' % (
                    context.call(environment.getattr(environment.getattr(l_scraped_item, 'key'), 'urlsafe')), 
                    environment.getattr(l_scraped_item, 'title'), 
                )
            l_scraped_item = missing
        yield u"</b><input id='add_submit' type='submit' value='Add' /><br />\n<b class='hidden'><img href='http://placehold.it/32x32' alt='loading_placeholder' /></b><br />\n<br />\n\n</form>\n\n<hr />\n\n\n<!-- url's left to crawl -->\n<h2>Queued URLs</h2>\n\n"
        if l_queued:
            if 0: yield None
            yield u"\n<ul id='queued_list'>\n\t"
            l_queued_url = missing
            for l_queued_url in l_queued:
                if 0: yield None
                yield u"\n\t<li id='queued_%s'><b>%s</b> - " % (
                    context.call(environment.getattr(environment.getattr(l_queued_url, 'key'), 'urlsafe')), 
                    t_1(environment.getattr(l_queued_url, 'url'), 150), 
                )
                if environment.getattr(l_queued_url, 'started') == False:
                    if 0: yield None
                    yield u"<b style='font-color: red;'>not started</b>"
                else:
                    if 0: yield None
                    yield u"<b style='font-color: green;'>started</b>"
                yield u'</li>\n\t'
            l_queued_url = missing
            yield u'\n</ul>\n'
        else:
            if 0: yield None
            yield u'\n<b>No queued URLs. Yay!</b>\n'
        yield u'\n\n<br /><br /><br />\n<hr /><br /><br />\n\n\n<!-- pages successfully crawled -->\n<h2>Scraped URLs</h2>\n\n'
        if l_scraped:
            if 0: yield None
            yield u"\n<ul id='scraped_list'>\n\t"
            l_scraped_page = missing
            l_queued_url = context.resolve('queued_url')
            for l_scraped_page in l_scraped:
                if 0: yield None
                yield u"\n\t<li id='scraped_%s'>URL key: <b>%s</b> - %s</li>\n\t" % (
                    context.call(environment.getattr(environment.getattr(l_queued_url, 'key'), 'urlsafe')), 
                    context.call(environment.getattr(environment.getattr(l_scraped_page, 'queued_url'), 'urlsafe')), 
                    context.call(environment.getattr(l_scraped_page, 'contenttext')), 
                )
            l_scraped_page = missing
            yield u'\n</ul>\n'
        else:
            if 0: yield None
            yield u'\n<b>No finished URLs. Aww.</b>\n'
        yield u'\n\n\n<script>\n\n\n\n$(document).ready(function () {\n\n\tfunction addURLEventHandler(event) {\n\n\t\tevent.preventDefault();\n\t\tevent.stopPropagation();\n\n\t\tif ($(\'#parent_select\').val()) {\n\t\t\trequest = $.apptools.api.crawl.add_url($(\'#addurl\').val(), $(\'#parent_select\').val());\n\t\t}\n\t\telse\n\t\t{\n\t\t\trequest = $.apptools.api.crawl.add_url($(\'#addurl\').val());\n\t\t}\n\t\trequest.fulfill({\n\n\t\t\tfailure: function (error) {\n\t\t\t\tconsole.log(\'An error occurred.\', error);\n\t\t\t\talert(\'An error occurred. Check the console.\');\n\t\t\t},\n\n\t\t\tsuccess: function (response) {\n\t\t\t\tconsole.log(\'A success response was receied.\', response);\n\t\t\t\t$(\'#queued_list\').append(\'<li class="added"><b>\'+$(\'#addurl\').value()+\'</b>\');\n\t\t\t}\n\n\t\t});\n\n\t}\n\n\t$(\'#urlform\').submit(addURLEventHandler);\n\t$(\'#add_submit\').click(addURLEventHandler);\n\n});\n\n'

    blocks = {'main': block_main}
    debug_info = '1=9&3=15&12=22&14=24&17=28&18=31&32=36&34=40&35=43&49=59&51=64&52=67'
    return locals()