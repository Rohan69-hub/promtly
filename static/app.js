document.addEventListener('DOMContentLoaded', () => {
    // Spotlight & Shine Tracking
    document.addEventListener('pointermove', (e) => {
        const spotlights = document.querySelectorAll('.spotlight-card');
        const shiners = document.querySelectorAll('.shine-border');
        
        spotlights.forEach(card => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);
        });

        shiners.forEach(shiner => {
            const rect = shiner.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;
            shiner.style.setProperty('--shine-x', `${x}%`);
            shiner.style.setProperty('--shine-y', `${y}%`);
        });
    });

    const promptInput = document.getElementById('promptInput');
    const sendBtn = document.getElementById('sendBtn');
    const inputSection = document.getElementById('inputSection');
    const resultSection = document.getElementById('resultSection');
    const sphere = document.getElementById('sphere'); // Hidden but kept for logic safety
    const voiceBtn = document.getElementById('voiceBtn');
    
    const friendlyMessage = document.getElementById('friendlyMessage');
    const perfectedPrompt = document.getElementById('perfectedPrompt');
    const copyBtn = document.getElementById('copyBtn');
    const resetBtn = document.getElementById('resetBtn');

    // Auto resize textarea
    promptInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
        sendBtn.disabled = this.value.trim() === '';
    });
    
    // Enter to submit, Shift+Enter for new line
    promptInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!sendBtn.disabled) {
                sendBtn.click();
            }
        }
    });
    
    // Initial setup with default text
    if (promptInput.value.trim() !== '') {
        promptInput.style.height = (promptInput.scrollHeight) + 'px';
        sendBtn.disabled = false;
        // Move cursor to end on initial focus
        promptInput.addEventListener('focus', function() {
            const val = this.value;
            this.value = '';
            this.value = val;
        }, { once: true });
    } else {
        sendBtn.disabled = true;
    }

    // Voice recognition setup
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = false;
        
        let isListening = false;
        let manuallyStopped = false; // Add state flag to persist Voice
        
        voiceBtn.addEventListener('click', () => {
            if (isListening) {
                manuallyStopped = true;
                recognition.stop();
                return;
            }
            manuallyStopped = false;
            voiceBtn.innerHTML = '<i class="fa-solid fa-microphone-lines fa-fade"></i> Listening... (Click to stop)';
            try {
                recognition.start();
                isListening = true;
            } catch (err) {
                console.log(err);
            }
        });
        
        recognition.onresult = (event) => {
            let finalTranscript = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                }
            }
            
            if (finalTranscript) {
                promptInput.value += (promptInput.value ? ' ' : '') + finalTranscript.trim();
                promptInput.style.height = 'auto';
                promptInput.style.height = (promptInput.scrollHeight) + 'px';
                sendBtn.disabled = promptInput.value.trim() === '';
            }
        };
        
        recognition.onerror = (event) => {
            if (event.error === 'not-allowed') {
                manuallyStopped = true;
                isListening = false;
                voiceBtn.innerHTML = '<i class="fa-solid fa-microphone"></i> Voice';
            }
        };
        
        recognition.onend = () => {
            if (!manuallyStopped) {
                // The browser aggressively cut off the listener, so boot it back up immediately
                try {
                    recognition.start();
                } catch(e) {
                    isListening = false;
                    voiceBtn.innerHTML = '<i class="fa-solid fa-microphone"></i> Voice';
                }
            } else {
                voiceBtn.innerHTML = '<i class="fa-solid fa-microphone"></i> Voice';
                isListening = false;
            }
        };
    } else {
        voiceBtn.addEventListener('click', () => alert("Voice recognition not supported in this browser."));
    }

    sendBtn.addEventListener('click', async () => {
        const text = promptInput.value.trim();
        if (!text) return;

        // UI Loading State
        sendBtn.disabled = true;
        sendBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> ENGAGED...';
        promptInput.disabled = true;

        try {
            const response = await fetch('/api/optimize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ imperfect_prompt: text })
            });
            
            const data = await response.json();
            
            if(data.status === 'success') {
                friendlyMessage.textContent = data.friendly_message;
                perfectedPrompt.value = data.perfected_prompt;
                
                // Animate transition
                document.querySelector('.header').style.display = 'none';
                inputSection.style.display = 'none';
                resultSection.style.display = 'block';
            } else {
                alert("Error optimizing prompt: " + data.friendly_message);
            }
        } catch (error) {
            alert("Network error: Failed to reach backend engine.");
        } finally {
            sendBtn.innerHTML = '<i class="fa-solid fa-arrow-up"></i> Send';
            sendBtn.disabled = false;
            promptInput.disabled = false;
        }
    });

    copyBtn.addEventListener('click', () => {
        perfectedPrompt.select();
        document.execCommand('copy');
        copyBtn.innerHTML = '<i class="fa-solid fa-check"></i> COPIED';
        setTimeout(() => {
            copyBtn.innerHTML = 'COPY';
        }, 2000);
    });

    resetBtn.addEventListener('click', () => {
        resultSection.style.display = 'none';
        document.querySelector('.header').style.display = 'block';
        inputSection.style.display = 'block';
        promptInput.value = 'I want to tell my AI to ';
        promptInput.style.height = 'auto';
        promptInput.style.height = (promptInput.scrollHeight) + 'px';
        sendBtn.disabled = false;
        copyBtn.innerHTML = '<i class="fa-regular fa-copy"></i> Copy';
    });

    // Fetch and display AI news
    const fetchNews = async () => {
        const newsGrid = document.getElementById('newsGrid');
        try {
            const response = await fetch('/news.json');
            if (!response.ok) throw new Error('Failed to load news');
            
            const news = await response.json();
            newsGrid.innerHTML = '';
            
            news.forEach(item => {
                const card = document.createElement('div');
            card.className = 'news-card spotlight-card';
            
            const shineWrapper = document.createElement('div');
            shineWrapper.className = 'shine-border';
            
            card.innerHTML = `
                <div class="news-tag">${item.tag || 'AI Update'}</div>
                <h4 class="news-title">${item.title}</h4>
                <p class="news-snippet">${item.snippet}</p>
                <a href="${item.url}" target="_blank" class="news-link">
                    Read Story <i class="fa-solid fa-arrow-right"></i>
                </a>
            `;
            
            shineWrapper.appendChild(card);
            newsGrid.appendChild(shineWrapper);
            });
        } catch (error) {
            console.error('Error fetching news:', error);
            newsGrid.innerHTML = '<p style="color: #666; font-family: monospace;">News update in progress...</p>';
        }
    };

    fetchNews();
});

