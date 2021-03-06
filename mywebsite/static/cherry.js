const validateEmail = function validateEmail(email) {
  var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(String(email).toLowerCase());
}

$( document ).ready(function(){
  $('.sidenav').sidenav();
  $('.parallax').parallax();
  $('.modal').modal();
  $('.dropdown-trigger').dropdown();
  $('select').formSelect();
  // Intitialization of auto complete
  // NOTE: update tags as your include more on the backend
  const searchData = {
    "research": '/static/tag.svg',
    "health": '/static/tag.svg',
    "animals": '/static/tag.svg',
    "environment": '/static/tag.svg',
    "education": '/static/tag.svg',
    "human rights": '/static/tag.svg',
    "community development": '/static/tag.svg',
    "arts/culture": '/static/tag.svg',
    "human services": '/static/tag.svg',
  }
  $('input.autocomplete').autocomplete({
    data: searchData,
  });
  $('#autocomplete-input').keyup(function() {
    const searchText = $('#autocomplete-input').val()
    if (searchText && searchText !== '' && searchText.toLowerCase() in searchData) {
      $('#autocomplete-help').text(`Search for charities tagged with "${searchText}"`)
    } else if (searchText && searchText !== '') {
      $('#autocomplete-help').text(`Search for charities like "${searchText}"`)
    } else {
      $('#autocomplete-help').text('Search by name, category...')
    }
  });
  $('#searchSubmit').submit(function (event) {
    event.preventDefault()
    const csrftoken = $("[name=csrfmiddlewaretoken]").val();
    const searchText = $('#autocomplete-input').val()
    $('#default-results').addClass('hidden')
    $('#fetching-search').removeClass('hidden')

    if (searchText && searchText !== '' && searchText.toLowerCase() in searchData) {
      // Find charities that are tagged with searchText
      window.location.href = `/charities/?tag=${searchText}`
    } else if (searchText && searchText !== '') {
      window.location.href = `/charities/?name=${searchText}`
    } else {
      window.location.href = '/charities/'
    }
  })
  // this is how the login button works
  $('#login_btn').click(function(){
    // First reveal the spinner component by removing hidden class
    $('#login-spinner').removeClass('hidden')
    // Second hide the form component by adding hidden class
    $('#login-form-row').addClass('hidden')
    $('#login-error').addClass('hidden')
    $('#forget-password-success').addClass('hidden')
    // Third make request
    const csrftoken = $("[name=csrfmiddlewaretoken]").val();
    $.ajax({
      url: '/login/',
      type: 'post',
      data: {
        'username':$('#user_name').val(),
        'password':$('#password').val()
      },
      headers: {
          "X-CSRFToken": csrftoken,
      },
      dataType: 'json',
      success: function (response) {
        console.log(response)
        if (response.is_admin && response.success) {
            window.location.href = '/charities'
        } else if (response.success && response.is_password_reset) {
            window.location.href = `/charity/${response.charity_profile_name}/${response.charity_profile_id}/?reset_password=true`
        } else if (response.success) {
            window.location.href = `/charity/${response.charity_profile_name}/${response.charity_profile_id}/`
        } else {
            // Reveal an error message
            $('#login-error').removeClass('hidden')
            $('#login-spinner').addClass('hidden')
            $('#login-form-row').removeClass('hidden')
        }
      }
    })
  })

  // This is how the forget password form renders from login modal
  $('#forgot_password_btn').click(function() {
    // Hide everything in login modal
    $('#login-form-modal').addClass('hidden')
    // Reveal forget password content
    $('#forget-password-modal').removeClass('hidden')
  })

  $('#back_to_login_btn').click(function() {
    // Forget everything in login modal
    $('#login-form-modal').removeClass('hidden')
    // Hide forget password content
    $('#forget-password-modal').addClass('hidden')
  })

  // Rest password form validation
  const isResetPasswordFormValid = function () {
      return (
        $('#forget_password_email').val() &&
        $('#forget_password_email').val() !== '' &&
        validateEmail($('#forget_password_email').val())
      )
  }
  const toggleResetPasswordSubmit = function () {
    if (isResetPasswordFormValid() && $('#forget_password_submit_btn').hasClass('disabled')) {
      $('#forget_password_submit_btn').removeClass('disabled')
    } else if (!isResetPasswordFormValid() && !$('#forget_password_submit_btn').hasClass('disabled')) {
      $('#forget_password_submit_btn').addClass('disabled')
    }
  }
  $('#forget_password_email').keyup(toggleResetPasswordSubmit)

  // this is how the reset password form submission works
  $('#forget_password_submit_btn').click(function() {
    // First reveal the spinner component by removing hidden class
    $('#forget-password-spinner').removeClass('hidden')
    // Second hide the form component by adding hidden class
    $('#forget-password-form-row').addClass('hidden')
    $('#forget-password-error').addClass('hidden')
    // Third make request
    const csrftoken = $("[name=csrfmiddlewaretoken]").val();
    $.ajax({
      url: '/forget_password/',
      type: 'post',
      data: {
        'email': $('#forget_password_email').val(),
      },
      headers: {
          "X-CSRFToken": csrftoken,
      },
      dataType: 'json',
      success: function (response) {
        if (response.success) {
          $('#forget-password-success').removeClass('hidden')
          // Clean and reset form
          $('#forget-password-spinner').addClass('hidden')
          $('#forget-password-form-row').removeClass('hidden')
          $('#forget_password_email').val('')
          // Go back to login modal
          $('#login-form-modal').removeClass('hidden')
          $('#forget-password-modal').addClass('hidden')
        } else {
          // Reveal an error message
          $('#forget-password-error').removeClass('hidden')
          $('#forget-password-spinner').addClass('hidden')
          $('#forget-password-form-row').removeClass('hidden')
        }
      }
    })
  })

  // this is how the logout button works
  $('#logout_btn, #logout_btn_sidebar').click(function(){
    const csrftoken = $("[name=csrfmiddlewaretoken]").val();
    $.ajax({
      url: '/logout/',
      type: 'post',
      data: {},
      headers: {
          "X-CSRFToken": csrftoken,
      },
      dataType: 'json',
      success: function(response) {
        window.location.href = '/'
      }
    })
  })
  // Sign form validation
  const isSignupFormValid = function () {
    return (
      ($('#new_user_name').val() && $('#new_user_name').val() !== '') &&
      ($('#new_password').val() && $('#new_password').val() !== '') &&
      ($('#email').val() && $('#email').val() !== '' && validateEmail($('#email').val())) &&
      ($('#new_charity_name').val() && $('#new_charity_name').val() !== '') &&
      // ($('#new_charity_url').val() && $('#new_charity_url').val() !== '') &&
      ($('#new_charity_bio').val() && $('#new_charity_bio').val() !== '') &&
      ($('#new_charity_campaign_name').val() && $('#new_charity_campaign_name').val() !== '')
    )
  }
  const toggleSignupSubmit = function () {
    if (isSignupFormValid() && $('#signup_submit').hasClass('disabled')) {
      $('#signup_submit').removeClass('disabled')
    } else if (!isSignupFormValid() && !$('#signup_submit').hasClass('disabled')) {
      $('#signup_submit').addClass('disabled')
    }
  }
  $('#new_user_name').keyup(toggleSignupSubmit)
  $('#new_password').keyup(toggleSignupSubmit)
  $('#email').keyup(toggleSignupSubmit)
  $('#new_charity_name').keyup(toggleSignupSubmit)
  $('#new_charity_url').keyup(toggleSignupSubmit)
  $('#new_charity_bio').keyup(toggleSignupSubmit)
  $('#new_charity_campaign_name').keyup(toggleSignupSubmit)
  //signup spinner works
  $('#signup_submit').click(function(){
      $('#signup-spinner').removeClass('hidden')
      // $('#login-form-row').addClass('hidden')
      const csrftoken = $("[name=csrfmiddlewaretoken]").val()
      $.ajax({
        url: '/charity/create/',
        type: 'post',
        data: {
          'username':$('#new_user_name').val(),
          'password':$('#new_password').val(),
          'email': $('#email').val(),
          'name':$('#new_charity_name').val(),
          'charity_url':$('#new_charity_url').val() == '' ? null : $('#new_charity_url').val(),
          'bio': $('#new_charity_bio').val(),
          'campaign_name': $('#new_charity_campaign_name').val(),
        },
        headers: {
            "X-CSRFToken": csrftoken,
        },
        dataType: 'json',
        success: function(response) {
          if (response.success) {
              window.location.href = `/charity/${response.charity_profile_name}/${response.charity_profile_id}/?first_time=true`
          } else {
              $('#signUpFormErrorContent').text(response.message)
              $('#signUpFormError').removeClass('hidden')
              $('#signup_modal').modal('close')
          }
        }
      })
  })

  // This is how update btn form works
  const isEmailFieldValid = function () {
    const email = $('#account_email').val()
    return (
      email === null ||
      email === '' ||
      validateEmail(email)
    )
  }

  const isPasswordFieldValid = function () {
    const password = $('#account_password').val()
    const passwordRepeat = $('#account_password_repeat').val()
    return (
      // Password fields are null
      (password === null && passwordRepeat === null) ||
      (password === '' && passwordRepeat === '') ||
      // Password fields are not null, equal, and > 8 characters
      (
        password !== null &&
        passwordRepeat !== null &&
        password === passwordRepeat &&
        password.length >= 8 &&
        passwordRepeat.length >= 8
      )
    )
  }
  const toggleUpdateSubmit = function () {
    if (
      isPasswordFieldValid() && isEmailFieldValid()
    ) {
        $('#update_btn').removeClass('disabled')
    } else if (
      !isPasswordFieldValid() || !isEmailFieldValid()
    ) {
        $('#update_btn').addClass('disabled')
    }
  }
  const toggleAccountErrorMessage = function () {
    if (isEmailFieldValid() && !$('#email-error').hasClass('hidden')) {
      $('#email-error').addClass('hidden')
    } else if (!isEmailFieldValid() && $('#email-error').hasClass('hidden')) {
      $('#email-error').removeClass('hidden')
    }
  }
  const togglePasswordErrorMessage = function () {
    if (isPasswordFieldValid() && !$('#password-error').hasClass('hidden')) {
      $('#password-error').addClass('hidden')
    } else if (!isPasswordFieldValid() && $('#password-error').hasClass('hidden')) {
      $('#password-error').removeClass('hidden')
    }
  }

  $('#account_email').keyup(toggleUpdateSubmit)
  $('#account_email').keyup(toggleAccountErrorMessage)
  $('#account_password').keyup(toggleUpdateSubmit)
  $('#account_password').keyup(togglePasswordErrorMessage)
  $('#account_password_repeat').keyup(toggleUpdateSubmit)
  $('#account_password_repeat').keyup(togglePasswordErrorMessage)

  $('#update_btn').click(function(){
    const userUpdatedFields = {}
    const newAccountEmail = $('#account_email').val()
    if (newAccountEmail && newAccountEmail !== '') {
      userUpdatedFields.email = newAccountEmail
    }

    const newAccountPassword = $('#account_password').val()
    if (newAccountPassword && newAccountPassword !== '') {
      userUpdatedFields.password = newAccountPassword
    }

    const newAccountPasswordRepeat = $('#account_password_repeat').val()
    if (newAccountPasswordRepeat && newAccountPasswordRepeat !== '') {
      userUpdatedFields.password_repeat = newAccountPasswordRepeat
    }

    const updatedFields = {}
    const newName = $('#name').val()
    if (newName && newName !== '') {
      updatedFields.name = newName
    }
    const newBio = $('#bio').val()
    if (newBio && newBio !== '') {
      updatedFields.bio = newBio
    }
    const newLongBio = $('#long_bio').val()
    if (newLongBio && newLongBio !== '') {
      updatedFields.long_bio = newLongBio
    }
    const newURL = $('#url').val()
    if (newURL && newURL !== '') {
      updatedFields.charity_url = newURL
    }
    const newImgURL = $('#img_url').val()
    if (newImgURL && newImgURL !== '') {
      updatedFields.img_url = newImgURL
    }
    const updateTags = {}
    let tag = null
    const rawTags = $('*[data-name]').get()
    for (let index = 0; index < rawTags.length; index++) {
        updateTags[rawTags[index].dataset.name] = !!rawTags[index].checked
    }
    const formData = {
      fields: updatedFields,
      user_fields: userUpdatedFields,
      tags: updateTags
    }
    const csrftoken = $("[name=csrfmiddlewaretoken]").val();
    $.ajax({
      url: `/charity/${$('#charity_current_name').val()}/${$('#charity_id').val()}/update/`,
      type: 'post',
      data: JSON.stringify(formData),
      headers: {
          "X-CSRFToken": csrftoken,
      },
      dataType: 'json',
      success: function(response){
        window.location.href = response.redirect_url
      }
    })
  })
  // This is how we create a new campaign
  $('#create_campaign_btn').click(function() {
    const newCampaign = {
      'new_campaign_name': $('#new_campaign_name').val(),
      'charity_id' : $('#charity_id').val(),
    }
    const csrftoken = $("[name=csrfmiddlewaretoken]").val()
    $.ajax({
      url: '/campaign/create/',
      type: 'post',
      data: newCampaign,
      headers: {
          "X-CSRFToken": csrftoken,
      },
      dataType: 'json',
      success: function(response) {
        console.log(response)
        location.reload()
      }
    })
  })
  // This is how we update the campaign item form
  $('#add_campaign_item').click(function() {
    const campaignId = $('#campaign_selected option:selected').val()
    const newItem = {
      'item_name': $('#item_name').val(),
      'item_cost': $('#item_cost').val(),
      'item_description': $('#item_description').val(),
      'item_img_url': $('#item_img_url').val(),
    }
    const csrftoken = $("[name=csrfmiddlewaretoken]").val()
    $.ajax({
      url: `/campaign/${campaignId}/add/`,
      type: 'post',
      data: newItem,
      headers: {
          "X-CSRFToken": csrftoken,
      },
      dataType: 'json',
      success: function(response) {
        console.log(response)
        location.reload()
      }
    })
  })
  // This is how we delete campaign items
  $('.delete-campaign-item').click(function(event) {
    $.get(
      `/campaign-item/${event.currentTarget.dataset.campaignItemId}/delete/`,
      function(response) {
        console.log(response)
        location.reload()
      }
    )
  })
  //This is how we delete campaigns (NEW)
  $('.delete-campaign').click(function(event){
    $.get(
      `/campaign/${event.currentTarget.dataset.campaignId}/delete/`,
      function(response){
        console.log(response)
        location.reload()
      }
    )
  })

  // only open the need help on first time login
  const urlParams = new URLSearchParams(window.location.search);
  const first_time = urlParams.get('first_time');
  if (first_time && first_time !== '') {
    $('#needhelp').modal('open')
  }
  // Open the edit modal upon password resets
  const reset_password = urlParams.get('reset_password');
  if (reset_password && reset_password !== '') {
    $('#edit').modal('open')
  }
})
