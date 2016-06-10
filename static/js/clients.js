$(document).ready(function() {
  var state = $('.state').attr('data-client-state');
  $('option[value="' + state + '"]').attr('selected', 'selected');
  $('.edit').click(function(){
    var id = $(this).attr('data-client-id')
    $.get('/index/client/' + id, function(res){
      if(res.error) {
        window.location.assign('/');
      } else {
        $('.main_content').html(res);
      }
    })
  })
  $('form').submit(function(e){
    console.log(e)
    // var top = e.originalEvent.path[6].innerHeight + "px"
    console.log(top)
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
      $.post('/update_client', data, function(res) {
        if(res.error) {
          window.location.assign('/');
        } else {
          $('.popup').css('top', '80vh')

          $('.jssuccess').show('slow');
        }
      })
    }
    return false;
  })
  $('.close').click(function(){
    $('.jssuccess').hide();
  })
  $('.confirm').click(function(){
    $.get('/index/clients', function(res){
      if(res.error) {
        window.location.assign('/');
      } else {
        $('.main_content').html(res);
      }
    })
  });
  $('.cancel').click(function(){
    $.get('/index/clients', function(res){
      if(res.error) {
        window.location.assign('/');
      } else {
        $('.main_content').html(res);
      }
    })
  });
});
