django-updateable
=================

django-updateable adds template tags to automatically update parts of pages via AJAX.

Install
-------

You can use pip to install:

    pip install django-updateable

Configure
---------

After installing django-updateable you must change a few settings in your settings.py

* Add ``updateable`` to INSTALLED_APPS
* Add ``updateable.middleware.UpdateableMiddleware`` to MIDDLEWARE_CLASSES
* Be sure to use the ``django.core.context_processors.request`` in your TEMPLATE_CONTEXT_PROCESSORS

Usage
-----

Add updateable.js to the pages where you use updateable, e.g.
``<script src="{% static "updateable.js" %}"></script>``. Load the tags in your
template, ``{% load updateable %}``. Wrap the parts of you template you would
like to update automatically in ``{% updateable %}`` and
``{% endupdateable %}`` tags.

Example template
----------------
::

  {% load staticfiles updateable %}
  
  <!doctype html>
  <html>
    <head>
      <title>example</title>
      <script src='{% static 'updateable.js' %}'></script>
    </head>
    <body>
    <h1>Static header</h1>
    {% updateable %}
      The time is {% now 'H:i:s' %}
    {% endupdateable %}
    </body>
  </html>

The time will be updated with 3 second intervals.

Supported platforms
-------------------

django-updateable has been tested with Django 1.3, 1.4 and 1.5 on Python 2.7
and with Django 1.5 on Python 2.6.

It has been tested on the latest version of Chrome (26) and Firefox (20). It
works with IE8 and up. If you need support for earlier versions of Internet 
Explorer you can use `this JavaScript file`_ which depends on jQuery.

.. _this JavaScript file: https://raw.github.com/baldurthoremilsson/django-updateable/master/compat/updateable-compat.js

Implementation details
----------------------

The content in a ``{% updateable %}`` template tag is wrapped in a ``<div>``
element that contains data attributes with a unique ID and an MD5 hash of the
content. Every AJAX request contains the IDs and hashes of the updateable
blocks on the page along with a GET variable that triggers the
UpdateableMiddleware to return only the parts of the page that have been
updated (the MD5 sum is used to decide which parts contain content that has
changed).

A new dictionary object is created on the request object (request._updateable)
that contains data for the UpdateableMiddleware and the UpdateableNode (in the
template). The name of this object can be configured in the settings.

Advanced settings
-----------------

Optional settings in settings.py:

* UPDATEABLE_REQUEST_OBJECT
  The name of the dictionary object that is created on the request object.
  Defaults to ``'_updateable'``
* UPDATEABLE_GET_VARIABLE
  Configures the name of the GET variable that triggers UpdateableMiddleware
  to intercept the response and return only the updated parts of the page.
  See getVariable in the JavaScript settings.
  Defaults to ``'update'``

Optional template tag setting:

* {% updateable [tagname] %}
  The given tagname is used for the enclosing element around the contents
  inside the updateable template tag.
  Defaults to ``div``

Optional JavaScript settings:

* getVariable
  The name of the GET variable that triggers the UpdateableMiddleware.
  See UPDATEABLE_GET_VARIABLES
  Defaults to ``'update'``
* timeout
  Milliseconds between AJAX calls.
  Defaults to ``3000``
* callback
  A function that is called for each DOM object that is replaced. The context
  of the function is the newly added DOM object.
  Defaults to an empty function

The JavaScript settings are read from a global object (on the window object)
called updateableSettings. Example::

    <head>
      <script>
        updateableSettings = {
          timeout: 5000,
          callback: function() {
            console.log(this);
        };
      </script>
      <script src='{% static 'updateable.js' %}'></script>
    </head>

Usage with jQuery Mobile
------------------------

django-updateable began life in a project that used `jQuery Mobile`_. When the
content is updated it is necessary to call ``trigger('create')`` on the new
DOM element, so the following updateableSettings can be useful in those
circumstances::

    updateableSettings = {
      callback: function() {
        $(this).trigger('create');
      }
    }

.. _jQuery Mobile: http://jquerymobile.com/

Release history
---------------

0.2.1
=====
Bugfix: IDs of updateable segments that started with numbers caused a bug in
the Javascript. Many thanks to edtanous_!

.. _edtanous: https://github.com/edtanous

0.2
===
Bugfixes, and jQuery is no longer a dependency (except for old browsers).

0.1
===
Initial release.

