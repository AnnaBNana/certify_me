$(document).ready(function() {
  $('.change_pdf').click(function(){
    $('.pdfupload').click()
  })

  $('.pdfupload').change(function(){
    $('.pdffilename').show()
    console.log($(this).val())
    $('.pdffilename').val($(this).val())
  })
  $('.add_csv').click(function(){
    $('.csvupload').click()
  })
  $('.csvupload').change(function(){
    $('.csvfilename').show()
    console.log($(this).val())
    $('.csvfilename').val($(this).val())
  });
  $('.client_alert_button').click(function(){
    $.get('/index/choose_client', function(res){
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
        $('.old_pdf_file_name').val(res.url[0].pdf_url)
        $('.old_pdf_file_name').show()
      } else {
        $('.no_pdf').show();
        $('.no_pdf_button').click(function(){
          $('.no_pdf').hide();
        })
      }
    })
  })
  $('form').submit(function(e){
    // e.preventDefault();
    var valid = true;
    //if no old pdf is selected, new pdf is required
    if ($('.old_pdf_file_name').val() == "") {
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
          $('.old_pdf_file_name').hide('slow');
          $('.pdffilename').hide('slow');
          $('.csvfilename').hide('slow');
          $('.success').show('slow');
          $('.success_button').click(function(){
            $('.success').hide('slow')
          })
        }
      })
    }
    return false;
  })
  $('.close_container').click(function(){
    $('.popup').hide('slow')
  })
});
