// This file contains JavaScript specific to the admin dashboard

document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners for admin actions
    const deleteButtons = document.querySelectorAll('.delete-job');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this job?')) {
                e.preventDefault();
            }
        });
    });
    
    // Add more admin-specific JavaScript as needed
});
