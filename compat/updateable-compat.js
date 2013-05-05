(function() {
  var settings = $.extend({
    timeout: 3000,
    callback: function() {},
    getVariable: 'update'
  }, updateableSettings);

  var update = function() {
    var ids = [], hash = [];
    $('[data-updateable]').each(function() {
      ids.push($(this).data('updateable'));
      hash.push($(this).data('hash'));
    });
    var getVars = {
      ids: ids,
      hash: hash
    };
    getVars[settings.getVariable] = true;
    $.get('', getVars, function(data) {
      var updated = $('<div>').html(data);
      $('[data-updateable]').each(function() {
        var id = $(this).data('updateable');
        var ud = updated.find('[data-updateable="' + id + '"]');
        if(ud.length == 1) {
          $(this).replaceWith(ud[0]);
          settings.callback.call(ud[0]);
        }
      });
      setTimeout(update, settings.timeout);
    });
  };

  setTimeout(update, settings.timeout);
})();
