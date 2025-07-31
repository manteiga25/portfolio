document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contactForm');
    if (form) {
        form.addEventListener('submit', send);
    }
});

async function send(e) {
    e.preventDefault();

    const nameField = document.getElementById('firstName');
    const subNameField = document.getElementById('lastName');
    const emailField = document.getElementById('email');
    const subjectField = document.getElementById('subject');
    const messageField = document.getElementById('message');

    const statusDiv = document.getElementById('status');

    const name = nameField.value + " " + subNameField.value;
    const email = emailField.value;
    const subject = subjectField.value;
    const message = messageField.value;

    if (name.length > 100) {
        return;
    }

    if (email.length > 127) {
        return;
    }

    if (subject.length > 100) {
        return;
    }

    fetch('/send', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        // Enviamos o novo tema no corpo do pedido
                        body: JSON.stringify({ name: name, email: email, subject: subject, message: message })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            statusDiv.className = 'status success';
                            statusDiv.textContent = data.message;
                            document.getElementById('contactForm').reset;
                        } else {
                            throw new Error(data.error || 'Error to send message');
                        }
                    })
                    .catch(error => {
                        statusDiv.className = 'status error';
                        statusDiv.textContent = 'Error: ' + error.message;
                    })
                    .finally(() => {
                        setTimeout(() => {
                            if (statusDiv) {
                                statusDiv.className = 'status';
                                statusDiv.textContent = '';
                            }
                        }, 5000);
                    });

}