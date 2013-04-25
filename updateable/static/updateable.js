$(function() {
  var TIMEOUT = 3000;
  var update = function() {
    var ids = [], hash = [];
    $('[data-updateable]').each(function() {
      ids.push($(this).data('updateable'));
      hash.push($(this).data('hash'));
    });
    $.get('', {update: true, ids: ids, hash: hash}, function(data) {
      var updated = $(data);
      window.updated = updated;
      $('[data-updateable]').each(function() {
        var $t = $(this);
        var id = $t.data('updateable');
        var ud = updated.find('[data-updateable="' + id + '"]');
        if(ud.length == 1) {
          $t.replaceWith(ud[0]);
          if(updateCallback !== 'undefined')
            updateCallback.apply(ud[0]);
        }
      });
      setTimeout(update, TIMEOUT);
    });
  };

  setTimeout(update, TIMEOUT);
});
