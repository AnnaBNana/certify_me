$(document).ready(function() {
  $.get('/permission_partial', function(res){
    console.log(res)
    if (res.error) {
      window.location.assign('/')
    } else {
      $('.main_content').html(res);
    }

  })
  //expand sidebar menu when hamburger is clicked
  $('.fa-bars').click(function(){
    $('.sidebar_content').toggle('slow');
  });
  //when add `user link is clicked, load add user partial
  $('.add_user').click(function() {
    $.get('/index/add_user', function(res) {
      $('.main_content').html(res);
    })
  });
  //when add client link is clicked, load add client partial
  $('.add_client').click(function() {
    $.get('/index/add_client', function(res) {
      $('.main_content').html(res);
    })
  });
  //when new seminar is clicked, load add class partial
  $('.add_class').click(function() {
    $.get('/index/add_class', function(res) {
      $('.main_content').html(res);
    })
  });
  //when generate pdf is clicked, load choose pdf partial
  $('.generate_certs').click(function() {
    $.get('/index/certificates', function(res) {
      $('.main_content').html(res);
    })
  });

});
