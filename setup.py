# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='django-updateable',
    version='0.1',
    author=u'Baldur Þór Emilsson',
    author_email='baldur@baldur.biz',
    packages=['updateable', 'updateable.templatetags'],
    package_data={'updateable': ['static/updateable.js']},
    url='https://github.com/baldurthoremilsson/django-updateable',
    license='LICENSE',
    description='Automatic updates for portions of templates with {% updateable %} tag',
    long_description=open('README.md').read(),
)
