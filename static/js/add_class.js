$(document).ready(function() {
  //when add seminar is clicked, load pdf partial
  $('.add_seminar').click(function() {
    $.get('/index/certificates', function(res) {
      $('.main_content').html(res);
    })
  })
});
