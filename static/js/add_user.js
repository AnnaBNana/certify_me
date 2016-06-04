$(document).ready(function() {
  //listen for change to user permission
  $('.permissions').change(function(e) {
    // console.log(e)
    if (e.currentTarget.value == "admin" || e.currentTarget.value == "user") {
      // console.log('admin')
      $('.client_select').show();
    }
    else if (e.currentTarget.value == "super-admin") {
      // console.log('super-admin')
      $('.client_select').hide();
    }
  });
  //show info window when client clicks question mark next to permissions label
  $('.info').click(function(){
    $('.info_window').show(900);
  })
  //close info window
  $('.close').click(function() {
    $('.info_window').hide('slow');
  })
  //submit register user form
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
      $('.jserror').show();
    } else {
      //if passwords do not match, show nomatch error
      if ($('.password').val() != $('.confirmpassword').val()) {
        $('.nomatch').show();
      } else {
        $('.jserror').hide();
        $('.nomatch').hide();
        var data = $(this).serialize();
        $.post('/add_user', data, function(res){
          console.log(res);
          if (res.error) {
            $('.dberror').append('<p>' + res.error + '</p>')
            $('.jserror').show();
          }
          else if (res.id) {
            $('.success').show();
          }
          $('input:not(:submit)').each(function(){
            $(this).val("");
          })
        })
      }
    }
    return false;
  })
});
