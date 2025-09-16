// core/static/core/js/main.js
document.addEventListener('DOMContentLoaded', function () {
    // --- Theme Toggle Logic ---
    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
    const themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');
    if (themeToggleBtn) {
        if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
            if (themeToggleLightIcon) themeToggleLightIcon.classList.remove('hidden');
        } else {
            document.documentElement.classList.remove('dark');
            if (themeToggleDarkIcon) themeToggleDarkIcon.classList.remove('hidden');
        }
        themeToggleBtn.addEventListener('click', function () {
            if (themeToggleDarkIcon) themeToggleDarkIcon.classList.toggle('hidden');
            if (themeToggleLightIcon) themeToggleLightIcon.classList.toggle('hidden');
            if (localStorage.getItem('color-theme')) {
                if (localStorage.getItem('color-theme') === 'light') {
                    document.documentElement.classList.add('dark');
                    localStorage.setItem('color-theme', 'dark');
                } else {
                    document.documentElement.classList.remove('dark');
                    localStorage.setItem('color-theme', 'light');
                }
            } else {
                if (document.documentElement.classList.contains('dark')) {
                    document.documentElement.classList.remove('dark');
                    localStorage.setItem('color-theme', 'light');
                } else {
                    document.documentElement.classList.add('dark');
                    localStorage.setItem('color-theme', 'dark');
                }
            }
        });
    }

    // --- REFACTORED CHAT & APPOINTMENT LOGIC ---
    const chatForm = document.getElementById('chat-form');
    if (chatForm) {
        const questionInput = document.getElementById('question-input');
        const submitButton = document.getElementById('submit-button');
        const chatHistory = document.getElementById('chat-history');
        const resetButton = document.getElementById('reset-button');
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const modal = document.getElementById('booking-modal');
        const modalBackdrop = document.getElementById('booking-modal-backdrop');
        const modalPanel = document.getElementById('modal-panel');

        // --- Step 1: Define the two different behaviors for the form ---
        const mainChatSubmitHandler = async (e) => {
            e.preventDefault();
            const question = questionInput.value.trim();
            if (!question) return;

            setFormEnabled(false);
            appendMessage(question, 'user');
            const thinkingIndicator = appendMessage('', 'bot', true);

            try {
                const response = await fetch('/chat/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
                    body: JSON.stringify({ question: question }),
                });
                if (!response.ok) throw new Error('An unknown error occurred.');

                const data = await response.json();
                thinkingIndicator.remove();
                appendMessage(data.answer, 'bot');

                if (data.is_complete) {
                    setFormEnabled(false);
                    appendMessage("Our screening is complete. You can start over by clicking the 'Start Over' button.", 'bot', false, false, 'system');
                    if (data.follow_up_action) {
                        handleFollowUpAction(data.follow_up_action);
                    }
                } else {
                    setFormEnabled(true);
                }
            } catch (error) {
                thinkingIndicator.remove();
                appendMessage(`Error: ${error.message}`, 'bot', false, true);
                setFormEnabled(true);
            }
        };
        
        const locationSubmitHandler = async (e) => {
            e.preventDefault();
            const location = questionInput.value.trim();
            if (!location) return;

            setFormEnabled(false);
            appendMessage(location, 'user');
            const thinkingIndicator = appendMessage('', 'bot', true);

            try {
                const response = await fetch(`/appointments/api/find-hospitals/?location=${location}`);
                const data = await response.json();
                thinkingIndicator.remove();
                showHospitalButtons(data.hospitals);
            } catch (error) {
                thinkingIndicator.remove();
                appendMessage("Sorry, I encountered an error finding hospitals. Please try again.", 'bot', false, true);
                setFormEnabled(true);
            } finally {
                // Restore the original chat handler
                chatForm.removeEventListener('submit', locationSubmitHandler);
                chatForm.addEventListener('submit', mainChatSubmitHandler);
            }
        };

        // --- Step 2: Set up the initial state and reset logic ---
        const startNewChat = async () => {
            const response = await fetch('/reset-chat/', { method: 'GET' });
            const data = await response.json();
            chatHistory.innerHTML = '';
            appendMessage(data.answer, 'bot');
            setFormEnabled(true);
            fetchPatientAppointments();
            
            // This is the key: always ensure ONLY the main listener is active on reset.
            chatForm.removeEventListener('submit', locationSubmitHandler);
            chatForm.removeEventListener('submit', mainChatSubmitHandler); // Remove first to prevent duplicates
            chatForm.addEventListener('submit', mainChatSubmitHandler);
        };

        startNewChat(); // Set up the chat initially
        resetButton.addEventListener('click', startNewChat);

        // --- Step 3: All other helper functions ---
        
        function setFormEnabled(enabled) {
            questionInput.disabled = !enabled;
            submitButton.disabled = !enabled;
            if (enabled) {
                questionInput.value = '';
                questionInput.focus();
            }
        }
        
        function appendMessage(text, sender, isThinking = false, isError = false, type = 'chat') {
            if (type === 'system') {
                const systemMessageWrapper = document.createElement('div');
                systemMessageWrapper.className = 'text-center my-4';
                systemMessageWrapper.innerHTML = `<span class="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded-full dark:bg-blue-900 dark:text-blue-300">${text}</span>`;
                chatHistory.appendChild(systemMessageWrapper);
                chatHistory.scrollTop = chatHistory.scrollHeight;
                return;
            }
            const messageWrapper = document.createElement('div');
            messageWrapper.className = 'flex items-start gap-3' + (sender === 'user' ? ' justify-end' : '');
            let messageContent = '';
            if (sender === 'user') {
                messageContent = `<div class="bg-teal-500 text-white p-4 rounded-xl rounded-br-none max-w-lg"><p>${text}</p></div><div class="flex-shrink-0 w-10 h-10 rounded-full bg-gray-200 dark:bg-gray-600 flex items-center justify-center font-bold text-gray-500 dark:text-gray-300">You</div>`;
            } else {
                const icon = `<div class="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-teal-400 to-blue-500 flex items-center justify-center text-white font-bold">AI</div>`;
                let textBubble = '';
                if (isThinking) {
                    textBubble = `<div class="bg-gray-100 dark:bg-gray-700 p-4 rounded-xl rounded-tl-none max-w-lg"><div class="flex items-center space-x-2"><div class="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div><div class="w-2 h-2 bg-gray-400 rounded-full animate-pulse [animation-delay:0.2s]"></div><div class="w-2 h-2 bg-gray-400 rounded-full animate-pulse [animation-delay:0.4s]"></div></div></div>`;
                } else if (isError) {
                    textBubble = `<div class="bg-red-100 dark:bg-red-900/50 text-red-700 dark:text-red-300 border border-red-200 dark:border-red-800 p-4 rounded-xl rounded-tl-none max-w-lg"><p>${text}</p></div>`;
                } else {
                     textBubble = `<div class="bg-gray-100 dark:bg-gray-700 p-4 rounded-xl rounded-tl-none max-w-lg prose prose-sm dark:prose-invert"><p>${text.replace(/\n/g, '<br>')}</p></div>`;
                }
                messageContent = icon + textBubble;
            }
            messageWrapper.innerHTML = messageContent;
            chatHistory.appendChild(messageWrapper);
            chatHistory.scrollTop = chatHistory.scrollHeight;
            return messageWrapper;
        }

        function handleFollowUpAction(action) {
            if (action.type === 'ask_to_book') {
                appendMessage(action.question, 'bot');
                const optionsContainer = document.createElement('div');
                optionsContainer.className = 'flex justify-center gap-4 my-2';
                action.options.forEach(option => {
                    const button = document.createElement('button');
                    button.textContent = option.text;
                    button.className = 'px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors';
                    button.dataset.payload = option.payload;
                    optionsContainer.appendChild(button);
                });
                chatHistory.appendChild(optionsContainer);
                chatHistory.scrollTop = chatHistory.scrollHeight;
                optionsContainer.addEventListener('click', (e) => {
                    if (e.target.tagName === 'BUTTON') {
                        const payload = e.target.dataset.payload;
                        optionsContainer.remove();
                        handleAppointmentChoice(payload);
                    }
                });
            }
        }

        function handleAppointmentChoice(payload) {
            if (payload === 'wants_to_book') {
                appendMessage("You replied: Yes", 'user');
                showLocationStep();
            } else if (payload === 'does_not_want_to_book') {
                appendMessage("You replied: No", 'user');
                appendMessage("Okay, that's perfectly fine. Please remember to seek medical advice from a professional soon. Stay safe.", 'bot');
            }
        }
        
        function showLocationStep() {
            appendMessage("Of course. To find hospitals near you, please tell me your location (e.g., city, state).", 'bot');
            setFormEnabled(true);
            // Swap event listeners
            chatForm.removeEventListener('submit', mainChatSubmitHandler);
            chatForm.addEventListener('submit', locationSubmitHandler);
        }

        function showHospitalButtons(hospitals) {
            if (hospitals.length === 0) {
                appendMessage("I couldn't find any specialized hospitals in that area. You may want to try a broader search.", 'bot');
                return;
            }
            appendMessage("Here are some highly-rated hospitals I found. Please select one to request an appointment:", 'bot');
            const hospitalContainer = document.createElement('div');
            hospitalContainer.className = 'flex flex-col items-start gap-2 my-2';
            hospitals.forEach(hospital => {
                const button = document.createElement('button');
                button.innerHTML = `<strong>${hospital.name}</strong><br><span class="text-xs">${hospital.address}</span>`;
                button.className = 'w-full p-3 text-left bg-gray-200 dark:bg-gray-700 rounded-lg hover:bg-teal-100 dark:hover:bg-teal-900 transition-colors';
                button.onclick = () => {
                    showConfirmationStep({name: hospital.name, address: hospital.address});
                };
                hospitalContainer.appendChild(button);
});
            chatHistory.appendChild(hospitalContainer);
            chatHistory.scrollTop = chatHistory.scrollHeight;
        }

        function showConfirmationStep(hospital) {
            modalPanel.innerHTML = `<div class="p-6"><h3 class="text-lg font-semibold text-gray-900 dark:text-white">Confirm Request</h3><p class="mt-2 text-sm">Are you sure you want to request an appointment at <strong>${hospital.name}</strong>?</p><div class="mt-6 flex justify-end gap-3"><button type="button" id="cancel-btn" class="bg-gray-200 dark:bg-gray-600 px-4 py-2 rounded-lg text-sm">No, go back</button><button type="button" id="confirm-request-btn" class="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm">Yes, request</button></div></div>`;
            openModal();
            document.getElementById('cancel-btn').addEventListener('click', closeModal);
            document.getElementById('confirm-request-btn').addEventListener('click', () => createAppointmentRequest(hospital));
        }

        async function createAppointmentRequest(hospital) {
            await fetch('/appointments/api/request/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
                body: JSON.stringify(hospital),
            });
            closeModal();
            appendMessage('Your appointment request has been sent. A doctor will confirm the date and time shortly. You can check the status in the "My Appointments" section below.', 'bot', false, false, 'system');
            fetchPatientAppointments();
        }

        function openModal() { modal.classList.remove('hidden'); modalBackdrop.classList.remove('hidden'); }
        function closeModal() { modal.classList.add('hidden'); modalBackdrop.classList.add('hidden'); }

        async function fetchPatientAppointments() {
            const response = await fetch('/api/my-appointments/');
            const data = await response.json();
            const listEl = document.getElementById('appointments-list');
            if (!listEl) return;
            if (data.appointments.length === 0) {
                listEl.innerHTML = `<p class="text-gray-500 dark:text-gray-400">You have no appointments.</p>`; return;
            }
            listEl.innerHTML = data.appointments.map(app => `<div class="p-4 rounded-lg border dark:border-gray-700 ${app.status === 'Confirmed' ? 'bg-green-50 dark:bg-green-900/30' : ''}"><p class="font-bold">${app.hospital}</p>${app.status === 'Confirmed' ? `<p class="text-sm text-green-600 dark:text-green-400">Status: Confirmed</p><p class="text-sm">With: Dr. ${app.doctor}</p><p class="text-sm">On: ${new Date(app.date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })} at ${app.time ? app.time.slice(0, 5) : ''}</p>` : `<p class="text-sm text-yellow-600 dark:text-yellow-400">Status: ${app.status}</p>`}</div>`).join('');
        }
    }
});