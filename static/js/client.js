$(document).ready(function() {
  //when add new client clicked, display add client partial
  $('.add_client').click(function(){
    $.get('/index/add_client', function(res) {
      $('.main_content').html(res);
    })
  });
  //when next is clicked, load add class partial
  $('.next').click(function(){
    client = {"id": $('.existing_client').val()}
    console.log(client)
    $.post('/choose_client', client, function(res) {
      $('.main_content').html(res);
    })
  })
});
