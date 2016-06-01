$(document).ready(function() {
  //set header according to view
  $('.page_title').html("Certify Me!");
  //hide sidebar options on login page
  $('.sidebar').css('visibility', 'hidden')
  //build logo
  $('.sidebar').append('<div class="logo"><h1><i class="fa fa-certificate" aria-hidden="true"></i></h1><h5><i class="fa fa-paw" aria-hidden="true"></i></h5></div>')
  //index frame
  //ajax for login, load client partial or email partial, depending on user permissions
  $('.login').click(function(){
    $('.sidebar').css('visibility', 'visible')
    $.get('/index/login', function(res) {
      console.log(res)
      $('.main_content').html(res);
    });
  });
  //when add user link is clicked, load add user partial
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

  //expand sidebar menu when hamburger is clicked
  $('.fa-bars').click(function(){
    $('.sidebar_content').toggle('slow');
  });

});
