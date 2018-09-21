# -*- coding: utf-8 -*-

from hashlib import md5
from django.template import Library, Node, TemplateSyntaxError
from .. import settings
import logging


register = Library()

class UpdateableNode(Node):
    def __init__(self, element_id, element, nodelist):
        self.element = element
        self.element_id = element_id
        self.nodelist = nodelist

    def render(self, context):
        request = context.get('request')
        contents = u''.join(n.render(context) for n in self.nodelist)
        hash = md5(contents.encode()).hexdigest()
        rcontext = {
            'id': self.element_id,
            'contents': contents,
            'hash': hash,
            'element': self.element,
        }
        output = u'<%(element)s data-updateable="%(id)s" data-hash="%(hash)s">%(contents)s</%(element)s>' % rcontext

        if bool(request.GET.get(settings.UPDATEABLE_GET_VARIABLE)):
            output = f'<template>{output}</template>'
        updateable_dict = getattr(request, settings.UPDATEABLE_REQUEST_OBJECT)
        if updateable_dict['updateable'] and updateable_dict['hashes'].get(id, '') != hash:
            updateable_dict['contents'].append(output)
        return output


@register.tag
def updateable(parser, token):
    contents = token.split_contents()
    try:
        element_id = contents[1]
        element = contents[2]
    except IndexError:
        raise TemplateSyntaxError('%s must have at least 1 argument' % contents[0])
    else:
        nodelist = parser.parse(('endupdateable',))
        parser.delete_first_token()
        return UpdateableNode(element_id, element, nodelist)

