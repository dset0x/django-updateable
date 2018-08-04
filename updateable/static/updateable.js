window.updateableSettings = (function() {
  var us = window.updateableSettings || {};
  var settings = {
    timeout: us.timeout || 3000,
    requestTimeout: us.requestTimeout || 3000,
    callback: us.callback || function() {},
    autoUpdate: us.autoUpdate || true,
    getVariable: us.getVariable || 'update'
  };

  var getUpdateables = function() {
    return document.querySelectorAll('[data-updateable]');
  };

  var retry = function() {
      setTimeout(update, settings.timeout);
  }

  var readyStateChanged = function() {
    if(this.readyState != 4)
      return;
    if(this.status == 200 && settings.autoUpdate) {
      var fragment = document.createDocumentFragment();
      var el = document.createElement('template');
      el.innerHTML = this.responseText;
      fragment.appendChild(el);

      var updateables = getUpdateables();
      for(var i = 0; i < updateables.length; i++) {
        var updateable = updateables[i];
        var id = updateable.getAttribute('data-updateable');
        var updated = fragment.firstChild.content.querySelector('[data-updateable="' + id + '"]');
        if(updated) {
          updateable.parentNode.replaceChild(updated, updateable);
          settings.callback.call(updated);
        }
      }
    }
    retry();
  };

  var update = function() {
    if(!settings.autoUpdate) {
      retry();
      return;
    }
    var currUrlParams = new URLSearchParams(window.location.search).toString();
    var url = '?' + currUrlParams + '&' + encodeURI(settings.getVariable + '=true');
    var updateables = getUpdateables();
    for(var i = 0; i < updateables.length; i++) {
      var updateable = updateables[i];
      var id = updateable.getAttribute('data-updateable');
      var hash = updateable.getAttribute('data-hash');
      url += encodeURI('&id[]=' + id);
      url += encodeURI('&hash[]=' + hash);
    }
    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = readyStateChanged;
    httpRequest.open('GET', url);
    httpRequest.timeout = settings.requestTimeout;
    httpRequest.send();
  };

  if(document.readyState === 'complete')
    setTimeout(update);
  else if(document.addEventListener)
    document.addEventListener('DOMContentLoaded', update);
  else
    window.attachEvent('onload', update);

  return settings;
})();
