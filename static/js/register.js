// JavaScript for disabling form submissions if there are invalid fields
(function () {
    'use strict'
  
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')
  
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
      .forEach(function (form) {
        form.addEventListener('submit', function (event) {
          if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
          }
  
          form.classList.add('was-validated')
        }, false)
      })
  })()

// Code reference: https://stackoverflow.com/questions/6218494/using-the-html5-required-attribute-for-a-group-of-checkboxes //
$(function(){
    var requiredCheckboxes = $('.options :checkbox[required]');
    requiredCheckboxes.change(function(){
        if(requiredCheckboxes.is(':checked')) {
            requiredCheckboxes.removeAttr('required');
        } else {
            requiredCheckboxes.attr('required', 'required');
        }
    });
});

// code reference: https://stackoverflow.com/questions/52036574/how-to-add-one-or-more-form-by-a-button-and-remove-it-by-another-button-by-javas/52038786 //
$("#add_button").click(function(){
  var intial_field = $(this).data("intial");
  var content = '<div id="input_'+intial_field+'"><input class="form-control" type="text" name="cocktail_ingredients" id="cocktail_ingredients"></input><button id="remove_btn" data-remove="'+intial_field+'">X</button></div>';
  $("#recurssion_container").append(content);
  $(this).data("intial",intial_field+1);
});

$(document).on("click","#remove_btn",function(){
  var remove_element = $(this).data("remove");
  $("#input_"+remove_element).remove();
});
