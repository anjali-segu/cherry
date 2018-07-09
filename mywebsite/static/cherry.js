$( document ).ready(function(){
  $('.sidenav').sidenav();
  $('.parallax').parallax();
  $('.modal').modal();
  $('.dropdown-trigger').dropdown();
  $('select').formSelect();
  // this is how the login button works
  $('#login_btn').click(function(){
    $.post('/login/',{
      'username':$('#user_name').val(),
      'password':$('#password').val()
    },
    function(response){
      window.location.href = `/charity/${response.charity_profile_name}/${response.charity_profile_id}/`
    })
  })
  // this is how the logout button works
  $('#logout_btn, #logout_btn_sidebar').click(function(){
    $.post('/logout/', {},function(response){
      window.location.href = '/'
    })
  })
  // this is how the signup button works
  $('#signup_submit').click(function(){
    $.post('/charity/create/',{
      'username':$('#new_user_name').val(),
      'password':$('#new_password').val(),
      'email': $('#email').val(),
      'name':$('#new_charity_name').val(),
      'charity_url':$('#new_charity_url').val(),
    },function(response){
      window.location.href = `/charity/${response.charity_profile_name}/${response.charity_profile_id}/`
    })
  })
  $('#update_btn').click(function(){
    const updatedFields = {}
    const newName = $('#name').val()
    if (newName && newName !== '') {
      updatedFields.name = newName
    }
    const newBio = $('#bio').val()
    if (newBio && newBio !== '') {
      updatedFields.bio = newBio
    }
    const newURL = $('#url').val()
    if (newURL && newURL !== '') {
      updatedFields.charity_url = newURL
    }
    const newImgURL = $('#img_url').val()
    if (newImgURL && newImgURL !== '') {
      updatedFields.img_url = newImgURL
    }

    $.post(
      `/charity/${$('#charity_current_name').val()}/${$('#charity_id').val()}/update/`,
      updatedFields,
      function(response){
        location.reload()
      }
    )
  })
  // This is how we update the campaign item form
  $('#add_btn').click(function() {
    const campaignId = $('#campaign_selected option:selected').val()
    const newItem = {
      'item_name': $('#item_name').val(),
      'item_cost': $('#item_cost').val(),
      'item_description': $('#item_description').val(),
      'item_img_url': $('#item_img_url').val(),
    }

    $.post(
      `/campaign/${campaignId}/add/`,
      newItem,
      function(response){
        console.log(response)
        location.reload()
      }
    )
  })
  // This is how we delete campaign items
  $('.delete-campaign-item').click(function(event) {
    console.log(event)
    $.get(
      `/campaign-item/${event.currentTarget.dataset.campaignItemId}/delete/`,
      function(response) {
        console.log(response)
        location.reload()
      }
    )
  })
})
