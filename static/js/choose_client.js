$(document).ready(function() {
  //when add new client clicked, display add client partial
  $('.add_client').click(function(){
    $.get('/index/add_client', function(res) {
      if (res.error) {
        window.location.assign('/')
      } else {
        $('.main_content').html(res);
      }
    })
  });
  //when next is clicked, load add class partial
  $('.add,.gen').click(function(){
    var source = $(this).attr('data-source')
    console.log(source)
    client = {"id": $('.existing_client').val(), "source": source}
    // console.log(client)
    $.post('/choose_client', client, function(res) {
      if (res.error) {
        window.location.assign('/')
      } else {
        $('.main_content').html(res);
      }
    })
  })
});
