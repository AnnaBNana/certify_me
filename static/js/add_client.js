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
        if (res.error) {
          window.location.assign('/')
        }
        if (res.name_error) {
          $('.namerr').html(res.name_error).show('slow');
        }
        if (res.title_error) {
          $('.titlerr').html(res.title_error).show('slow');
        }
        if (res.biz_name_error) {
          $('.biznamerr').html(res.biz_name_error).show('slow');
        }
        if (res.street_addr_error) {
          $('.streeterr').html(res.street_addr_error).show('slow');
        }
        if (res.city_addr_error) {
          $('.cityerr').html(res.city_addr_error).show('slow');
        }
        if (res.state_addr_error) {
          $('.staterr').html(res.state_addr_error).show('slow');
        }
        if (res.zip_addr_error) {
          $('.ziperr').html(res.zip_addr_error).show('slow');
        }
        if (res.email_error) {
          $('.emailerr').html(res.email_error).show('slow');
        }
        if (res.success) {
          $('.popup').show('slow');
          $('input:not(:submit),select').each(function(){
            $(this).val("");
          });
          $('form').attr('data-source', "new");
          $('form').attr('data-id', res.biz_id);
        }
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
    var data = {'id': $('form').attr('data-id'), 'source': $('form').attr('data-source')}
    $.post('/choose_business', data, function(res) {
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
