$(document).ready(function() {
  var inst_num = 1;
  $('.edit').click(function(){
    var id = $(this).attr('data-class-id')
    $.get('/index/class/' + id, function(res) {
      if(res.error) {
        window.location.assign('/');
      } else {
        $('.main_content').html(res);
      }
    })
  })
  $('.cancel').click(function(){
    $.get('/index/classes', function(res){
      if(res.error) {
        window.location.assign('/');
      } else {
        $('.main_content').html(res);
      }
    })
  });
  $('.update').click(function(){
    class_data = $(this).serialize();
    $.post('/update_class', class_data, function(res){
      if(res.error) {
        window.location.assign('/');
      } else {
        $('.main_content').html(res);
      }
    })
  });
  $('.remove').click(function(){
    var id = $(this).attr('data-instructor-id');
    $('.instructor' + id).attr('name', 'remove' + id);
    var test = $('.instructor' + id).attr('name');
    console.log(test);
    $('.instructor' + id).hide();
    $(this).hide()
  });
  $('.add_instructor').click(function(){
    $('.add_instructor_target').show();
    $(this).hide();
  });
  $('.new_instructor').click(function(){
    $('.instructor').append("<div class='row'><input type='text' class='twelve columns' name='new_instructor" + inst_num + "' placeholder='enter new instructor name including degrees'></div>")
    inst_num++;
    // console.log($('.instructor').html())
  });
  $('form').submit(function() {
    var valid = true;
    // check each input to see if it is empty
    $('.required').each(function(){
      if(!$(this).val()) {
        valid = false;
      }
    });
    //if some fields are empty, show empty error
    if (!valid) {
      $('.jserror').show();
    } else {
      $('.jserror').hide();
      var data = $(this).serialize();
      console.log(data)
      $.post('/update_class', data, function(res) {
        console.log(res)
        if (res.error) {
          window.location.assign('/')
        } else {
          $('.main_content').html(res);
        }
      })
    }
    return false;
  })
});
