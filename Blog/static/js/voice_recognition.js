let recognition;
let isRecording = false;

// Initialize speech recognition
function initSpeechRecognition() {
    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        recognition.onresult = function(event) {
            let finalTranscript = '';
            let interimTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                } else {
                    interimTranscript += transcript;
                }
            }

            const transcriptionArea = document.getElementById('transcription');
            transcriptionArea.value = finalTranscript + interimTranscript;
            updateWordCount();
        };

        recognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
            stopRecording();
        };

        recognition.onend = function() {
            if (isRecording) {
                recognition.start();
            }
        };
    } else {
        alert('Speech recognition is not supported in your browser.');
    }
}

// Start recording
function startRecording() {
    if (!recognition) {
        initSpeechRecognition();
    }
    
    try {
        recognition.start();
        isRecording = true;
        document.getElementById('startBtn').disabled = true;
        document.getElementById('stopBtn').disabled = false;
        document.getElementById('status').textContent = 'Recording...';
        document.getElementById('recordingIndicator').style.display = 'block';
    } catch (error) {
        console.error('Error starting speech recognition:', error);
    }
}

// Stop recording
function stopRecording() {
    if (recognition) {
        recognition.stop();
        isRecording = false;
        document.getElementById('startBtn').disabled = false;
        document.getElementById('stopBtn').disabled = true;
        document.getElementById('status').textContent = 'Not recording';
        document.getElementById('recordingIndicator').style.display = 'none';
    }
}

// Update word count
function updateWordCount() {
    const transcription = document.getElementById('transcription').value;
    const wordCount = transcription.trim().split(/\s+/).length;
    document.getElementById('wordCount').textContent = wordCount;
}

// Initialize when document is ready
document.addEventListener('DOMContentLoaded', function() {
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    const transcription = document.getElementById('transcription');
    
    if (startBtn) startBtn.addEventListener('click', startRecording);
    if (stopBtn) stopBtn.addEventListener('click', stopRecording);
    if (transcription) transcription.addEventListener('input', updateWordCount);
    
    // Copy transcription to content field when form is submitted
    const blogForm = document.getElementById('blogForm');
    if (blogForm) {
        blogForm.addEventListener('submit', function(e) {
            const contentField = document.getElementById('content');
            if (contentField) {
                contentField.value = transcription.value;
            }
        });
    }
}); 