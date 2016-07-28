$(document).ready(function() {
  //when add seminar is clicked, load pdf partial
  var inst_num = 1;
  $('form').submit(function() {
    var valid = true;
    // check each input to see if it is empty
    $('.required').each(function(){
      if(!$(this).val()) {
        valid = false;
      }
    });
    //if some fields are empty, show empty error
    if (!valid) {
      $('.jserror').show();
    } else {
      $('.jserror').hide();
      var data = $(this).serialize();
      $.post('/add_class', data, function(res) {
        // console.log(res)
        if (res.error) {
          window.location.assign('/')
        }
        if (res.name_error) {
          $('.namerr').html(res.name_error).show('slow');
        }
        if (res.course_num_error) {
          $('.courserr').html(res.course_num_error).show('slow');
        }
        if (res.duration_error) {
          $('.durationerr').html(res.duration_error).show('slow');
        }
        if (res.date_error) {
          $('.daterr').html(res.date_error).show('slow');
        }
        if (res.instructor_error) {
          $('.instructorerr').html(res.instructor_error).show('slow');
        }
        if (res.email_error) {
          $('.emailerr').html(res.email_error).show('slow');
        }
        if (res.race_verbiage) {
          $('.racerr').html(res.race_verbiage).show('slow');
        }
        if (res.id) {
          $('.main_content').html(res);
        }
      })
    }
    return false;
  })
  $('.new_instructor').click(function(){
    $('.instructor').append("<div class='row'><input type='text' class='twelve columns' name='new_instructor" + inst_num + "' placeholder='enter new instructor name including degrees'></div>")
    inst_num++;
    // console.log($('.instructor').html())
  })
  $('.client_alert_button').click(function(){
    $.get('/index/choose_business', function(res){
      if (res.error) {
        window.location.assign('/')
      } else {
        $('.main_content').html(res);
      }
      $('.client_alert').hide();
    })
  })
});
