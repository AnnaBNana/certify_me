$(document).ready(function() {
  $('.client').click(function(){
    $.get('/index/choose_business', function(res) {
      if (res.error) {
        window.location.assign('/')
      } else {
        $('.main_content').html(res);
      }
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
        // console.log(res);
        $('input:not(:submit),select').each(function(){
          $(this).val("");
        })
        $('.popup').show('slow');
      })
    }
    return false;
  })
  //handle add biz button click by loading add business partial
  $('.add_biz').click(function(){
    $.get('./index/add_biz', function(res) {
      $('.new_biz').html(res);
      $('.biz_opts').remove();
    })
  })
  $('.activate').click(function(){
    $.get('/index/add_class', function(res) {
      $('.popup').hide()
      if (res.error) {
        window.location.assign('/')
      } else {
        $('.main_content').html(res);
      }
    })
  });
  $('.choose').click(function(){
    $.get('/index/choose_business', function(res) {
      $('.popup').hide()
      if (res.error) {
        window.location.assign('/')
      } else {
        $('.main_content').html(res);
      }
    })
  })
  $('.close').click(function(){
    $('.popup').hide();
  })
});
