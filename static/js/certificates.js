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
  })
});
