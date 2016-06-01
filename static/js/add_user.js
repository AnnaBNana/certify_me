$(document).ready(function() {
  //listen for change to user permission
  $('.permissions').change(function(e) {
    console.log(e)
    if (e.currentTarget.value == "admin" || e.currentTarget.value == "user") {
      console.log('admin')
      $('.client_select').show();
    }
    else if (e.currentTarget.value == "super-admin") {
      console.log('super-admin')
      $('.client_select').hide();
    }
  });
  //show info window when client clicks question mark next to permissions label
  $('.info').click(function(){
    $('info_window').show();
  })
});
