$(document).ready(function() {
  //when add new client clicked, display add client partial
  $('.add_client').click(function(){
    $.get('/index/add_client', function(res) {
      $('.main_content').html(res);
    })
  });

});
