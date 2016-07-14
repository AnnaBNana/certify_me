$(document).ready(function() {

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
          console.log(res);
          $('input:not(:submit,:button),select').each(function(){
            $(this).val("");
          })
          $('.existing_pdf').hide('slow');
          $('.pdffilename').hide('slow');
          $('.csvfilename').hide('slow');
          $('.jssuccess').show('slow');
        }
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


});
