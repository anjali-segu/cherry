$( document ).ready(function(){
  $('.sidenav').sidenav();
  $('.parallax').parallax();
  $('.modal').modal();
  // this is how the login button works
  $('#login_btn').click(function(){
    console.log($('#user_name').val())
    console.log($('#password').val())
    $.post('/login/',{
      'username':$('#user_name').val(),
      'password':$('#password').val()
    },
    function(response){
      console.log(response)
      window.location.href = `/charity/${response.charity_profile_name}/${response.charity_profile_id}/`
    })
  })
  // this is how the logout button works
  $('#logout_btn, #logout_btn_sidebar').click(function(){
    $.post('/logout/', {},function(response){
      console.log(response)
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
      console.log(response)
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

    console.log(updatedFields)

    $.post(
      `/charity/${$('#charity_current_name').val()}/${$('#charity_id').val()}/update/`,
      updatedFields,
      function(response){
        console.log(response)
        location.reload()
      }
    )
  })
})
