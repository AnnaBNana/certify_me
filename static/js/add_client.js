$(document).ready(function() {
  $('.client').click(function(){
    $.get('/index/login', function(res) {
      $('.main_content').html(res);
    })
  })
});
