# -*- coding: utf-8 -*-

from hashlib import md5
from django.template import Library, Node, TemplateSyntaxError

register = Library()


class UpdateableNode(Node):
    def __init__(self, element, nodelist):
        self.element = element
        self.nodelist = nodelist

    def render(self, context):
        request = context.get('request')
        un_nr = context.render_context.get('un_nr', 1)
        context.render_context['un_nr'] = un_nr + 1

        id = self.get_id(request, un_nr)
        contents = u''.join(n.render(context) for n in self.nodelist)
        hash = md5(contents).hexdigest()
        rcontext = {
            'id': id,
            'contents': contents,
            'hash': hash,
            'element': self.element,
        }
        output = u'<%(element)s data-updateable="%(id)s" data-hash="%(hash)s">%(contents)s</%(element)s>' % rcontext

        _ud = request._updateable
        if _ud['updateable'] and _ud['hashes'].get(id, '') != hash:
            request._updateable['contents'].append(output)
        return output

    def get_id(self, request, un_nr):
        if not request:
            id = un_nr
        else:
            id = md5('%d-%s' % (un_nr, request.path)).hexdigest()
        return id


@register.tag
def updateable(parser, token):
    contents = token.split_contents()
    if len(contents) == 1:
        element = 'div'
    elif len(contents) == 2:
            element = contents[1]
    else:
        raise TemplateSyntaxError('%s can have at most one argument' % contents[0])

    nodelist = parser.parse(('endupdateable',))
    parser.delete_first_token()
    return UpdateableNode(element, nodelist)

