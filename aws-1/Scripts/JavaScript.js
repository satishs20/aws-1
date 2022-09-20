$(function(){
  $('body').on('click', '.list-group-item', function(){
    $('.list-group-item').removeClass('active');
    $(this).closest('.list-group-item').addClass('active');
  });
});