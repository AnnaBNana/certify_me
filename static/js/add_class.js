$(document).ready(function() {
  //when add seminar is clicked, load pdf partial
  $('form').submit(function() {
    var data = $(this).serialize();
    console.log(data)
    $.post('/add_class', data, function(res) {
      $('.main_content').html(res);
    })
    return false;
  })
});
