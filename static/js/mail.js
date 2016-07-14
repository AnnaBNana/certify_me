$(document).ready(function() {
  $('.send').click(function(){
    var students = {};
    $("input[type='checkbox']:checked").each(function(){
      var student = $(this).val();
      students[student] = student
    });
    $.post('/send_mail', students, function(res){
      if (res.error) {
        window.location.assign('/')
      } else {
        console.log(res);
        var placement = $(document).height() - ($('.popup').height() * 2)
        $('.popup').css({'top': placement})
        $('.sent').show('slow');
      }
    })
  });

  $('textarea').keydown(function(){
    $(this).css('color', '#ec795b')
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
