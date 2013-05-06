# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='django-updateable',
    version='0.1',
    author=u'Baldur Þór Emilsson',
    author_email='baldur@baldur.biz',
    packages=['updateable', 'updateable.templatetags'],
    package_data={'updateable': ['static/updateable.js']},
    install_requires=['Django >= 1.3'],
    url='https://github.com/baldurthoremilsson/django-updateable',
    license='BSD',
    description='Automatic updates for portions of templates with {% updateable %} tag',
    long_description=open('README.rst').read(),
)
