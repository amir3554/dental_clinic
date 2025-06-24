//<!-- You would place this script tag typically at the end of your body or in a linked JS file -->
//<script>
let hiddenDateInput; // Declare these globally but assign inside DOMContentLoaded
let submitButton;

/**
 * @brief Checks if the hidden date input has a value and enables/disables the submit button.
 * This function should be called whenever the hidden_date input's value might change.
 */
function updateSubmitButtonState() {
    // Ensure elements exist before trying to access their properties
    if (!hiddenDateInput || !submitButton) {
        console.error("Error: hiddenDateInput or submitButton not found.");
        return; // Exit if elements are not found to prevent further errors
    }

    // Check if the hiddenDateInput has a value.
    // A simple check for truthiness works because an empty string is falsy.
    if (hiddenDateInput.value) {
        submitButton.disabled = false; // Enable the button
    } else {
        submitButton.disabled = true; // Disable the button
    }
}

// This ensures the script runs only after the entire HTML document is loaded and parsed.
document.addEventListener('DOMContentLoaded', () => {
    // Get references to the hidden date input and the submit button
    // These assignments now happen when the DOM is ready
    hiddenDateInput = document.getElementById('hidden_date');
    submitButton = document.getElementById('submitBtn');

    // Initial check when the page loads
    // This ensures the button is disabled if the hidden field is initially empty
    updateSubmitButtonState();

    // Add an event listener to the hidden input.
    // The 'change' event might not fire for programmatic changes to value.
    // If your date picker updates the value programmatically,
    // you'll need to call updateSubmitButtonState() directly after updating hidden_date.
    if (hiddenDateInput) { // Only add listener if element exists
        hiddenDateInput.addEventListener('change', updateSubmitButtonState);
    } else {
        console.error("Error: hidden_date element not found. Submit button state may not update correctly.");
    }
});

// IMPORTANT: If your date/time picker (from "common/date_form.html")
// updates the 'hidden_date' field programmatically,
// you must call `updateSubmitButtonState()` immediately after setting its value.
// Example (assuming you have a function that sets the date):
/*
function setHiddenDate(dateString) {
    if (hiddenDateInput) {
        hiddenDateInput.value = dateString;
        updateSubmitButtonState(); // Call this after updating the value
    }
}
*/
//</script>

//<script>
$(function(){
  const $submit = $('#submitBtn');
  const $hidden = $('#hidden_date');

  // حين يغيّر datepicker أو تنقر على خلية وقت:
  function checkEnable() {
    if ($hidden.val().trim()) {
      $submit.prop('disabled', false);
    } else {
      $submit.prop('disabled', true);
    }
  }

  // ربط مع datepicker
  $('#dp1').datepicker({ /* إعداداتك */ })
    .on('changeDate', function(){
      $hidden.val($(this).val());
      checkEnable();
    });

  // ربط مع خانات الوقت
  $('.cell').on('click', function(){
    $('.cell.selected').removeClass('selected');
    $(this).addClass('selected');
    const datePart = $('#dp1').val();
    const timePart = $(this).text().trim();
    $hidden.val(datePart + ' ' + timePart);
    checkEnable();
  });
});


function showAlert(message, type) {
  $.notify({
    // محتوى الرسالة
    message: message
  },{
    // خيارات التنبيه
    type: type,          // 'success', 'danger', 'info', 'warning'
    allow_dismiss: true,
    delay: 3000
  });
}



//</script>