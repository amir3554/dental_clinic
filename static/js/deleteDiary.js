//<button class="delete-btn" data-diary-id="1">Delete</button>

document.querySelectorAll('.delete-btn').forEach(button => {
    button.addEventListener('click', function() {
        const diaryId = this.getAttribute('data-diary-id');
        const confirmDelete = confirm("Are you sure you want to delete this diary?");
        
        if (confirmDelete) {
            deleteDiary(diaryId);
        }
    });
});

function deleteDiary(diaryId) {
    fetch(`/mydiary/diary/delete/${diaryId}`, {
        method: 'DELETE', // or 'POST' if you are using a form submission
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token for Django
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.ok) {
            // Optionally remove the diary from the UI
            const diaryElement = document.getElementById(`diary-${diaryId}`);
            if (diaryElement) {
                alert("diary deleted successfully!");
                diaryElement.remove();
            } else {
                alert("There was an issue deleting the diary.");
            }
        }  
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred while trying to delete the diary. CATCH");
    });
}

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}