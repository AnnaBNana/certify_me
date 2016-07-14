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
  });

  //show info window when client clicks question mark next to permissions label
  $('.info').click(function(){
    $('.info_window').show('slow');
  });

  //close info window
  $('.close').click(function() {
    $('.popup').hide('slow');
  });

  $('form#user').submit(function(){
    // console.log('confirmed')
    var valid = true;
    // check each input to see if it is empty
    $('input.requiredu').each(function(){
      console.log("confirmed");
      if(!$(this).val()) {
        valid = false;
      }
    });
    //if some fields are empty, show empty error
    if (!valid) {
      $('.usererr').show('slow');
    } else {
      user = $(this).serialize();
      console.log(user)
      $.post('/update_user', user, function(res){
        if (res.error) {
          window.location.assign('/')
        } else {
          $('.user').show('slow')
        }
      })
    }
    return false
  });

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

  $('form#password').submit(function(){
    // console.log('confirmed')
    var valid = true;
    // check each input to see if it is empty
    $('input.requiredp').each(function(){
      if(!$(this).val()) {
        valid = false;
      }
    });
    var newp = $('.newp').val();
    var confp = $('.confp').val();

    if (!valid) {
      $('.pworderr').show('slow');
    }
    else if (newp != confp){
      $('.pworderr').html('<p>new password and password confirmation must match</p>')
      $('.pworderr').show('slow');
    } else {
      passwords = $(this).serialize();
      console.log(user)
      $.post('/update_password', passwords, function(res){
        if (res.error) {
          window.location.assign('/');
        }
        else if (res.validation_err){
          $('.pworderr').html('<p>' + res.validation_err + '</p');
          $('.pworderr').show('slow');
        } else {
          var top = $(document).height() - ($('.popup').height() * 2);
          $('.popup').css({'top': top});
          $('.password').show('slow');
        }
        $('input.requiredp').val("");
      })
    }
    return false
  });
});
