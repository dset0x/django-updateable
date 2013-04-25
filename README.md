django-updateable
=================

Adds {% updateable %} template tag for automatically updating parts of templates via AJAX

Usage
-----

  * Add updateable to INSTALLED\_APPS in settings.py:
  * Add updateable.middleware.UpdateableMiddleware to MIDDLEWARE\_CLASSES
  * Add updateable.js to your page, e.g. <script src='{% static "updateable.js" %}'></script>
  * Load the updateable template tags in your template: {% load updateable %}
  * Add the {% updateable %} template tag around the portion of your template that you want to be auto updated:

    <p>Some HTML</p>
    {% updateable %}
      <ul>
        {% for user in users %}
          <li>{{ user.username }}</li>
        {% endfor %}
      </ul>
    {% endupdateable %}
    <p>Some more HTML</p>


Implementation
--------------

_A.k.a. how does it work?_

All contents inside an {% updateable %} template tag is wrapped in a div element\*.
The element has two attributes: data-updateable and data-hash. data-updateable contains
a unique ID for this updateable block and data-hash contains an MD5 sum of the contents
of the block. Every 3 seconds the JavaScript in updateable.js sends a GET request to
the server to the same URL as the current page. It contains three GET variables:
update = true along with ids and hash. ids and hash are arrays containing a list of all
ids and hashes of the updateable blocks on the current page. When the request hits the
server we fully render the response but the updateable middleware is triggered (with
the update = true GET parameter) and it returns instead only the updateable blocks that
contain different data (the hash is used to determine whether the content is new or
unchanged).

\* If you want a different tag you can specify it in the template tag, e.g. {% updateable span %}
