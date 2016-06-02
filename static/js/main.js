$(document).ready(function() {
  //set header according to view
  $('.page_title').html("Certify Me!");
  //hide sidebar options on login page
  $('.sidebar').css('visibility', 'hidden')
  //build logo
  $('.sidebar').append('<div class="logo"><div class="badge"><i class="fa fa-certificate" aria-hidden="true"></i></div><div class="paw"><i class="fa fa-paw" aria-hidden="true"></i></div></div>')
  //index frame
  //ajax for login, load client partial or email partial, depending on user permissions
  $('.login').click(function(){
    //show sidebar menu toggle button only after logged in
    $('.sidebar').css('visibility', 'visible')
    //load whichever partial user has permission to access after login
    $.get('/index/login', function(res) {
      // console.log(res)
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
  //expand sidebar menu when hamburger is clicked
  $('.fa-bars').click(function(){
    $('.sidebar_content').toggle('slow');
  });

});
