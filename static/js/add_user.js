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
  $('.close_container').click(function() {
    $('.popup').hide('slow');
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
      $('.all').show('slow');
    } else {
      //if passwords do not match, show nomatch error
      pword = $('.password').val();
      cpword = $('.confirmpassword').val();
      if (pword != cpword) {
        $('.pwerr').append("password and confirmation do not match");
        $('.pwerr').show();
      //otherwise, hide all errors and send form data to backend for additional validation
      } else {
        $('.jserror').hide();
        var data = $(this).serialize();
        $.post('/add_user', data, function(res){
          //show inline error message if any server side validations failed
          if (res.dupe_error) {
            $('.emailerr').append(res.dupe_error)
            $('.emailerr').show();
          }
          if (res.name_error) {
            $('.namerr').append(res.name_error)
            $('.namerr').show();
          }
          if (res.email_error) {
            $('.emailerr').append(res.email_error)
            $('.emailerr').show();
          }
          if (res.password_error) {
            $('.pwerr').append(res.password_error)
            $('.pwerr').show();
          }
          //otherwise, show success message
          if (res.id) {
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
  //success message window button redirects to user list
  $('.user_list').click(function(){
    $.get('/index/users', function(res){
      if (res.error) {
        window.location.assign('/')
      } else {
        $('.main_content').html(res)
      }
    })
  })
});
