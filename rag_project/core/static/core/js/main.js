// core/static/core/js/main.js
document.addEventListener('DOMContentLoaded', function () {
    // --- Theme Toggle Logic ---
    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
    const themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');

    // Check for saved theme in localStorage
    if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
        themeToggleLightIcon.classList.remove('hidden');
    } else {
        document.documentElement.classList.remove('dark');
        themeToggleDarkIcon.classList.remove('hidden');
    }

    themeToggleBtn.addEventListener('click', function () {
        // toggle icons inside button
        themeToggleDarkIcon.classList.toggle('hidden');
        themeToggleLightIcon.classList.toggle('hidden');

        // if set via local storage previously
        if (localStorage.getItem('color-theme')) {
            if (localStorage.getItem('color-theme') === 'light') {
                document.documentElement.classList.add('dark');
                localStorage.setItem('color-theme', 'dark');
            } else {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('color-theme', 'light');
            }
        } else { // if NOT set via local storage previously
            if (document.documentElement.classList.contains('dark')) {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('color-theme', 'light');
            } else {
                document.documentElement.classList.add('dark');
                localStorage.setItem('color-theme', 'dark');
            }
        }
    });

    // --- Chat Logic ---
    const chatForm = document.getElementById('chat-form');
    const questionInput = document.getElementById('question-input');
    const submitButton = document.getElementById('submit-button');
    const chatHistory = document.getElementById('chat-history');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    chatForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const question = questionInput.value.trim();
        if (!question) return;

        // Disable form and show loading state
        questionInput.value = '';
        questionInput.disabled = true;
        submitButton.disabled = true;

        // Add user's message to chat history
        appendMessage(question, 'user');

        // Add thinking indicator
        const thinkingIndicator = appendMessage('', 'bot', true);

        try {
            const response = await fetch('/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({ question: question }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'An unknown error occurred.');
            }

            const data = await response.json();
            // Remove thinking indicator and add final response
            thinkingIndicator.remove();
            appendMessage(data.answer, 'bot');

        } catch (error) {
            thinkingIndicator.remove();
            appendMessage(`Error: ${error.message}`, 'bot', false, true);
        } finally {
            // Re-enable form
            questionInput.disabled = false;
            submitButton.disabled = false;
            questionInput.focus();
        }
    });

    function appendMessage(text, sender, isThinking = false, isError = false) {
        const messageWrapper = document.createElement('div');
        messageWrapper.className = 'flex items-start gap-3' + (sender === 'user' ? ' justify-end' : '');
        
        let messageContent;
        if (sender === 'user') {
            messageContent = `
                <div class="bg-teal-500 text-white p-4 rounded-xl rounded-br-none max-w-lg">
                    <p>${text}</p>
                </div>
                <div class="flex-shrink-0 w-10 h-10 rounded-full bg-gray-200 dark:bg-gray-600 flex items-center justify-center font-bold text-gray-500 dark:text-gray-300">
                    You
                </div>
            `;
            messageWrapper.innerHTML = messageContent;
        } else { // Bot message
            const icon = `
                <div class="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-teal-400 to-blue-500 flex items-center justify-center text-white font-bold">
                    AI
                </div>`;
            
            let textBubble;
            if (isThinking) {
                textBubble = `
                    <div class="bg-gray-100 dark:bg-gray-700 p-4 rounded-xl rounded-tl-none max-w-lg">
                        <div class="flex items-center space-x-2">
                            <div class="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
                            <div class="w-2 h-2 bg-gray-400 rounded-full animate-pulse [animation-delay:0.2s]"></div>
                            <div class="w-2 h-2 bg-gray-400 rounded-full animate-pulse [animation-delay:0.4s]"></div>
                        </div>
                    </div>`;
            } else if (isError) {
                textBubble = `
                    <div class="bg-red-100 dark:bg-red-900/50 text-red-700 dark:text-red-300 border border-red-200 dark:border-red-800 p-4 rounded-xl rounded-tl-none max-w-lg">
                        <p>${text}</p>
                    </div>`;
            } else {
                 textBubble = `
                    <div class="bg-gray-100 dark:bg-gray-700 p-4 rounded-xl rounded-tl-none max-w-lg prose prose-sm dark:prose-invert">
                        <p>${text}</p>
                    </div>`;
            }
            messageWrapper.innerHTML = icon + textBubble;
        }
        
        chatHistory.appendChild(messageWrapper);
        chatHistory.scrollTop = chatHistory.scrollHeight; // Scroll to bottom
        return messageWrapper;
    }
});