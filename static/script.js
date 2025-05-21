document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const input = document.querySelector('#message');
    const chatbox = document.querySelector('#chatbox');

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        const userMessage = input.value.trim();

        if (!userMessage) return;

        // Show user message
        appendMessage('You', userMessage);
        input.value = '';

        try {
            const response = await fetch('/get', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMessage })
            });

            const data = await response.json();
            appendMessage('Bot', data.reply);
        } catch (error) {
            console.error('Error:', error);
            appendMessage('Bot', 'Oops! Something went wrong.');
        }
    });

    function appendMessage(sender, message) {
        const messageElem = document.createElement('div');
        messageElem.classList.add('message');
        messageElem.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatbox.appendChild(messageElem);
        chatbox.scrollTop = chatbox.scrollHeight;
    }
});
