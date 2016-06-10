$(document).ready(function() {
  $('.edit').click(function(){
    id = $(this).attr('data-user-id');
    console.log(id);
    $.get('/index/user/' + id, function(res){
      if (res.error) {
        window.location.assign('/')
      } else {
        $('.main_content').html(res);
      }
    })
  });
  $('.delete').click(function(e){
    //set top of popup window position to be 200px below window scroll point
    var top = e.view.scrollY + 200 + "px"
    $('.popup').css('top', top)
    var id = $(this).attr('data-user-id')
    $('.delete_popup').show('slow')
    $('.confirm_delete').click(function(){
      $.get('/delete/user/' + id, function(res){
        $('.main_content').html(res)
      })
    })
    $('.cancel_delete').click(function(){
      $('.delete_popup').hide('slow')
    })
  })
  //show info window when client clicks question mark next to permissions label
  $('.info').click(function(){
    $('.info_window').show('slow');
  })
  //close info window
  $('.close').click(function() {
    $('.info_window').hide('slow');
  })
  $('form').submit(function(){
    var valid = true;
    // check each input to see if it is empty
    $('input').each(function(){
      if(!$(this).val()) {
        valid = false;
      }
    });
    //if some fields are empty, show empty error
    if (!valid) {
      $('.jserror').show('slow');
    } else {
      user = $(this).serialize();
      $.post('/update_user', user, function(res){
        if (res.error) {
          window.location.assign('/')
        } else {
          $('.jssuccess').show('slow')
        }
      })
    }
    return false
  })
  $('.confirm').click(function(){
    $.get('/index/users', function(res){
      $('.main_content').html(res);
    })
  })
  $('#remove').remove();
  $('.cancel').click(function(){
    $.get('/index/users', function(res){
      if(res.error) {
        window.location.assign('/');
      } else {
        $('.main_content').html(res);
      }
    })
  });
});
