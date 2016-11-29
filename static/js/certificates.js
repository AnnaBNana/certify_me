$(document).ready(function() {
  //set up loading animation position based on size of window
  var x = ($(window).width() / 2);
  var y = ($(window).height() / 2);
  $('.dizzy-gillespie').css({'position': 'absolute', 'top': y/2 + "px", 'left': x + "px", 'z-index': 5});

  $('.client_alert').css('display', 'block');

  $('.change_pdf').click(function(){
    $('.pdfupload').click();
    $('.existing_pdf').val("").hide();
  });

  $('.pdfupload').change(function(){
    $('.pdffilename').show().val($(this).val());
  });

  $('.add_csv').click(function(){
    $('.csvupload').click()
  });

  $('.csvupload').change(function(){
    $('.csvfilename').show().val($(this).val());
  });

  $('.client_alert_button').click(function(){
    $.get('/index/choose_business', function(res){
      if (res.error) {
        window.location.assign('/')
      } else {
        $('.main_content').html(res);
      }
      $('.client_alert').hide();
    })
  });

  $('.default_pdf').click(function(){
    $.get('/check_pdf_url', function(res){
      if (res.error) {
        window.location.assign('/')
      }
      else if (res.url[0].pdf_url) {
        console.log(res)
        $('.existing_pdf').val(res.url[0].pdf_url).show()
      } else {
        $('.no_pdf').show();
        $('.no_pdf_button').click(function(){
          $('.no_pdf').hide();
        });
      }
    });
  });

  $('form').submit(function(e){
    // e.preventDefault();
    var valid = true;
    //if no old pdf is selected, new pdf is required
    if ($('.existing_pdf').val() == "") {
      $('.pdffilename').addClass('required')
    }
    $('.required').each(function() {
      if(!$(this).val()) {
        valid = false;
      }
    });
    if (!valid) {
      $('.jserror').show();
    } else {
      $('.dizzy-gillespie').show();
      var height = $(document).height();
      $('.dim').css({'min-height': height});
      $('.dim').show();
      $('.jserror').hide();
      var data = new FormData($('#form_data')[0])
      data.append("existing_pdf", $(".existing_pdf").val())
      data.append("pdf_file", $(".pdfupload")[0].files[0])
      data.append("csv_file", $(".csvupload")[0].files[0])
      $.ajax({
        url: '/certificates',
        data: data,
        contentType: false,
        type: 'POST',
        processData: false,
        dataType: 'json',
        success: function(res){
          // console.log(res)
          if (res.error) {
            window.location.assign('/')
          }
          else if (res.file_error) {
            hide_loader();
            $('.file_error').show();
          } else {
            var valid = true;
            for (var i = 0; i < res.messages.length; i++) {
              if ("placement_error" in res.messages[i]) {
                $('.pdf_gen_error').append(res.messages[i].placement_error);
                valid = false;
              }
            }
            if (!valid) {
              hide_loader();
              $('.pdf_gen_error').show('slow');
            } else {
              $('input:not(:submit,:button),select').each(function(){
                $(this).val("");
              })
              hide_loader();
              hide_inputs();
              $('.jssuccess').show('slow');
            }
          }
        }
      }).fail(function(){
        console.log('something weird happened, what are you going to do?');
      })
    }
    return false;
  });

  $('.continue').click(function(){
    $.get("/index/mail", function(res){
      if (res.error) {
        window.location.assign('/')
      } else {
        $('.main_content').html(res);
      }
    })
  });
  $('.skip').click(function(){
    var id = $('.skip_class').val();
    console.log(id);
    $.get("/index/mail/" + id, function(res){
      if (res.error) {
        window.location.assign('/')
      } else {
        $('.main_content').html(res);
      }
    })
  });

  $('.close_container,.stay').click(function(){
    $('.popup').hide('slow')
  });

  $('.epdf').click(function(){
    $('.pdf1_info').show('slow');
  });

  $('.npdf').click(function(){
    $('.pdf2_info').show('slow');
  });

  $('.csv').click(function(){
    $('.csv_info').show('slow');
  });
  function hide_loader(){
    $('.dizzy-gillespie').hide();
    $('.dim').hide();
  }
  function hide_inputs() {
    $('.existing_pdf').hide();
    $('.pdffilename').hide();
    $('.csvfilename').hide();
  }

});
