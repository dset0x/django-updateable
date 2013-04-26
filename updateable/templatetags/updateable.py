# -*- coding: utf-8 -*-

from hashlib import md5
from django.template import Library, Node, TemplateSyntaxError
from .. import settings


register = Library()

class UpdateableNode(Node):
    def __init__(self, element, nodelist):
        self.element = element
        self.nodelist = nodelist

    def render(self, context):
        request = context.get('request')
        updateable_count = context.render_context.get('updateable_count', 1)
        context.render_context['updateable_count'] = updateable_count + 1

        id = self.get_id(request, updateable_count)
        contents = u''.join(n.render(context) for n in self.nodelist)
        hash = md5(contents).hexdigest()
        rcontext = {
            'id': id,
            'contents': contents,
            'hash': hash,
            'element': self.element,
        }
        output = u'<%(element)s data-updateable="%(id)s" data-hash="%(hash)s">%(contents)s</%(element)s>' % rcontext

        updateable_dict = getattr(request, settings.UPDATEABLE_REQUEST_OBJECT)
        if updateable_dict['updateable'] and updateable_dict['hashes'].get(id, '') != hash:
            updateable_dict['contents'].append(output)
        return output

    def get_id(self, request, updateable_count):
        if not request:
            id = updateable_count
        else:
            id = md5('%d-%s' % (updateable_count, request.path)).hexdigest()
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

