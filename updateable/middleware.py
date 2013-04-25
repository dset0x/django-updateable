# -*- coding: utf-8 -*-

from django.http import HttpResponse


class UpdateableMiddleware(object):
    def process_request(self, request):
        updateable = bool(request.GET.get('update'))
        hashvals = {}
        if updateable:
            ids = request.GET.getlist('ids[]')
            hashes = request.GET.getlist('hash[]')
            for id, hash in zip(ids, hashes):
                hashvals[id] = hash
        request._updateable = {
            'updateable': bool(request.GET.get('update')),
            'hashes': hashvals,
            'contents': [],
        }
    def process_response(self, request, response):
        if request._updateable['updateable']:
            contents = request._updateable['contents']
            content = '<div>%s</div>' % u''.join(contents)
            return HttpResponse(content)
        return response
