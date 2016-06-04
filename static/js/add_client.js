$(document).ready(function() {
  $('.client').click(function(){
    $.get('/index/choose_client', function(res) {
      $('.main_content').html(res);
    })
  })
  //submit form data to add client to db
  $('form').submit(function(){
    var valid = true;
    $('.required').each(function() {
      if(!$(this).val()) {
        valid = false;
      }
    });
    if (!valid) {
      $('.jserror').show();
    } else {
      $('.jserror').hide();
      var data = $(this).serialize();
      $.post('/add_client', data, function(res) {
        console.log(res);
        $('input:not(:submit),select').each(function(){
          $(this).val("");
        })
        $('.popup').show('slow');
      })
    }
    return false;
  })
});
