# -*- coding: utf-8 -*-

from django.http import HttpResponse
from updateable import settings


class UpdateableMiddleware(object):

    def process_request(self, request):
        updateable = bool(request.GET.get(settings.UPDATEABLE_GET_VARIABLE))
        hashvals = {}
        if updateable:
            ids = request.GET.getlist('ids[]')
            hashes = request.GET.getlist('hash[]')
            for id, hash in zip(ids, hashes):
                hashvals[id] = hash
        updateable_dict = {
            'updateable': updateable,
            'hashes': hashvals,
            'contents': [],
        }
        setattr(request, settings.UPDATEABLE_REQUEST_OBJECT, updateable_dict)

    def process_response(self, request, response):
        updateable_dict = getattr(request, settings.UPDATEABLE_REQUEST_OBJECT)
        if updateable_dict['updateable']:
            contents = updateable_dict['contents']
            content = ''.join(contents)
            response['Content-length'] = str(len(content))
            if getattr(response, 'streaming', False):
                response.streaming_response = (content,)
            else:
                response.content = content
            response['Cache-control'] = 'no-cache' # Preventing IE bug
        return response

