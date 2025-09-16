// doctor_tools/static/doctor_tools/js/main.js
document.addEventListener('DOMContentLoaded', function () {
    // --- Clinical Assistant Query Logic ---
    const queryForm = document.getElementById('query-form');
    if (queryForm) {
        const questionInput = document.getElementById('question-input');
        const submitButton = document.getElementById('submit-button');
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const initialState = document.getElementById('initial-state');
        const loadingState = document.getElementById('loading-state');
        const resultsContent = document.getElementById('results-content');
        const errorState = document.getElementById('error-state');
        const patientSelect = document.getElementById('patient-select');

        queryForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const question = questionInput.value.trim();
            const patientId = patientSelect.value;

            if (!question || !patientId) {
                alert('Please select a patient and enter a question.');
                return;
            }
            
            submitButton.disabled = true;
            submitButton.textContent = 'Analyzing...';
            initialState.classList.add('hidden');
            resultsContent.innerHTML = '';
            errorState.classList.add('hidden');
            loadingState.classList.remove('hidden');

            try {
                const response = await fetch('/doctor/api/ask/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
                    body: JSON.stringify({ 
                        question: question,
                        patient_id: patientId
                    }),
                });
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || `HTTP error! Status: ${response.status}`);
                }
                const data = await response.json();
                loadingState.classList.add('hidden');
                resultsContent.innerHTML = parseResponse(data.answer);
            } catch (error) {
                loadingState.classList.add('hidden');
                const errorMessage = `<div class="bg-red-100 dark:bg-red-900/50 text-red-700 dark:text-red-300 border border-red-200 dark:border-red-800 p-4 rounded-lg"><h3 class="font-bold">Analysis Failed</h3><p class="text-sm mt-2">${error.message}</p></div>`;
                errorState.innerHTML = errorMessage;
                errorState.classList.remove('hidden');
            } finally {
                submitButton.disabled = false;
                submitButton.innerHTML = `Analyze & Respond`;
            }
        });
        
        function parseResponse(text) {
            let html = text.replace(/</g, "&lt;").replace(/>/g, "&gt;");
            html = html.replace(/\*\*(.*?)\*\*/g, '<strong class="text-gray-900 dark:text-white">$1</strong>');
            html = html.replace(/^\s*(\d+\.\s.*)$/gm, '<h3 class="text-lg font-bold mt-6 mb-2">$1</h3>');
            html = html.replace(/^\s*-\s*(.*)$/gm, '<li class="mt-1">$1</li>');
            html = html.replace(/(<li>.*<\/li>)/gs, '<ul class="list-disc list-inside space-y-1 pl-4 mt-2">$1</ul>');
            return html.split('\n').map(line => {
                if (line.trim() === '' || line.startsWith('<h3') || line.startsWith('<ul') || line.startsWith('<li')) return line;
                return `<p class="mb-4">${line}</p>`;
            }).join('');
        }
    }

    // --- Appointment Confirmation Logic ---
    document.querySelectorAll('.confirmation-form').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const appointmentId = e.target.dataset.id;
            const date = e.target.querySelector('.date-input').value;
            const time = e.target.querySelector('.time-input').value;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            try {
                const response = await fetch(`/appointments/api/confirm/${appointmentId}/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
                    body: JSON.stringify({ date, time }),
                });
                if (!response.ok) throw new Error('Failed to confirm appointment');
                const requestCard = document.getElementById(`request-${appointmentId}`);
                requestCard.innerHTML = `<p class="text-green-600 text-center font-bold p-4">Appointment Confirmed!</p>`;
                setTimeout(() => location.reload(), 1500);
            } catch (error) {
                alert(error.message);
            }
        });
    });
});