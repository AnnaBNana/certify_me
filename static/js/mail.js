$(document).ready(function() {
  //set up loading animation position based on size of window
  var x = ($(window).width() / 2);
  var y = ($(window).height() / 2);
  $('.dizzy-gillespie').css({'position': 'absolute', 'top': y/2 + "px", 'left': x + "px", 'z-index': 5});

  $('.send').click(function(){
    var students = {};
    //grab attendee id from each row where box is checked
    $("input[type='checkbox']:checked").each(function(){
      var student = $(this).val();
      students[student] = student
    });
    $('.dizzy-gillespie').show();
    var height = $(document).height();
    $('.dim').css({'min-height': height});
    $('.dim').show();
    $.post('/send_mail', students, function(res){
      $('.dizzy-gillespie').hide();
      $('.dim').hide();
      if (res.error) {
        window.location.assign('/');
      }
      else if (res.send_error) {
        $('.popup').html("<div class='row close_container'><i class='fa fa-times-circle close' aria-hidden='true'></i></div>there was an error sending your emails, please try again later");
        $('.sent').show('slow');
        $('.close').click(function(){
          $(".popup").hide('slow')
        })
      } else {
        console.log(res);
        var placement = $(document).height() - ($('.popup').height() * 2)
        $('.popup').css({'top': placement})
        $('.sent').show('slow');
      }
    })
  });

  $('.savedb').click(function(){
    $('.popup').hide('slow');
    $('.dizzy-gillespie').show();
    var height = $(document).height();
    $('.dim').css({'min-height': height});
    $('.dim').show();
    $.get('/index/dropbox_upload', function(res){
      $('.dizzy-gillespie').hide();
      $('.dim').hide();
      if (res.error) {
        window.location.assign('/');
      }
      else if (res.upload_error) {
        $('.uploaded').html('there was an error uploading to dropbox, please try again later');
        $('.popup').hide('slow')
        $('.uploaded').show('slow');
      } else {
        var placement = $(document).height() - ($('.popup').height() * 2);
        $('.popup').css({'top': placement});
        $('.uploaded').show('slow');
      }
    })
  });

  $('.restart').click(function(){
    $.get("/index/certificates", function(res){
      if (res.error) {
        window.location.assign('/')
      } else {
        $('.main_content').html(res);
      }
    })
  })

  $('textarea').keydown(function(){
    $(this).css('color', '#B60065')
  });

  $('.change_text').click(function(){
    var email_text = {'email_text': $('.email_text').val()};
    $.post('/update_email', email_text, function(res){
      if (res.error) {
        window.location.assign('/')
      } else {
        $('textarea').css('color', '#000');
        $('.text').show('slow');
      }
    });
  });
  $('.close_container,.done').click(function(){
    $('.popup').hide('slow')
  });
});
