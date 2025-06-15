// Tab Navigation
function showTab(tabName) {
    // Hide all tab contents
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(tab => tab.classList.remove('active'));
    
    // Remove active class from all tab buttons
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(btn => btn.classList.remove('active'));
    
    // Show selected tab content
    document.getElementById(tabName).classList.add('active');
    
    // Add active class to clicked button
    event.target.classList.add('active');
}

// Scenario Data
const scenarios = {
    home_night: {
        title: "🏠 Home Night Emergency",
        description: "It's 2:30 AM. You're awakened by strong shaking. Your bed is moving, and you can hear dishes rattling in the kitchen. What's your immediate response?",
        choices: [
            {
                text: "Jump out of bed and run outside immediately",
                correct: false,
                explanation: "Running during shaking increases injury risk. Stay put until shaking stops."
            },
            {
                text: "Stay in bed, cover your head with a pillow, and wait",
                correct: true,
                explanation: "Correct! Stay where you are, protect your head, and wait for shaking to stop."
            },
            {
                text: "Get up and turn on the lights to see better",
                correct: false,
                explanation: "Moving during shaking is dangerous. Stay in bed and protect yourself first."
            },
            {
                text: "Call for help on your phone",
                correct: false,
                explanation: "Your safety comes first. Protect yourself before trying to communicate."
            }
        ]
    },
    office: {
        title: "🏢 Office Building Emergency",
        description: "You're working on the 15th floor when the building starts shaking violently. Colleagues are panicking. What should you do first?",
        choices: [
            {
                text: "Run to the emergency stairs immediately",
                correct: false,
                explanation: "Don't move during shaking. Take cover first, then evacuate when safe."
            },
            {
                text: "Duck under your desk and hold on",
                correct: true,
                explanation: "Perfect! Drop, cover, and hold on. Protect yourself from falling objects."
            },
            {
                text: "Stand in the doorway",
                correct: false,
                explanation: "Modern doorways aren't necessarily safer. Desk protection is better."
            },
            {
                text: "Help others get to safety first",
                correct: false,
                explanation: "Secure your own safety first, then help others after shaking stops."
            }
        ]
    },
    mall: {
        title: "🏪 Shopping Mall Emergency",
        description: "You're shopping in a crowded mall when an earthquake begins. People are screaming and rushing toward exits. What's your best action?",
        choices: [
            {
                text: "Follow the crowd to the nearest exit",
                correct: false,
                explanation: "Crowds can cause trampling. Find cover first, then exit safely when possible."
            },
            {
                text: "Take cover under a sturdy table or against an interior wall",
                correct: true,
                explanation: "Excellent choice! Avoid crowds, find sturdy cover, and protect yourself."
            },
            {
                text: "Lie flat on the ground to avoid falling",
                correct: false,
                explanation: "You'd be vulnerable to trampling and falling objects. Seek proper cover."
            },
            {
                text: "Try to help fallen shoppers",
                correct: false,
                explanation: "Ensure your safety first. Help others after the shaking stops."
            }
        ]
    },
    school: {
        title: "🏫 School Classroom Emergency",
        description: "You're teaching a class of 25 students when an earthquake strikes. The children are frightened and looking to you for guidance. What's your immediate response?",
        choices: [
            {
                text: "Tell students to get under their desks immediately",
                correct: true,
                explanation: "Perfect! Quick, clear instructions to take cover. Then protect yourself too."
            },
            {
                text: "Lead students outside in a line",
                correct: false,
                explanation: "Don't move during shaking. Take cover first, evacuate after shaking stops."
            },
            {
                text: "Tell students to stay calm while you assess the situation",
                correct: false,
                explanation: "Action is needed immediately. Clear cover instructions come first."
            },
            {
                text: "Open the classroom door and wait",
                correct: false,
                explanation: "Taking cover is the priority. Door opening can wait until after protection."
            }
        ]
    }
};

let currentScenario = null;
let currentScore = 0;

// Start Scenario
function startScenario(scenarioId) {
    if (!scenarios[scenarioId]) return;
    
    currentScenario = scenarioId;
    currentScore = 0;
    
    const scenario = scenarios[scenarioId];
    
    // Show scenario player
    document.getElementById('scenario-player').classList.remove('hidden');
    
    // Update scenario content
    document.getElementById('scenario-title').textContent = scenario.title;
    document.getElementById('scenario-description').textContent = scenario.description;
    document.getElementById('scenario-score').textContent = `Score: ${currentScore}`;
    
    // Clear previous feedback
    document.getElementById('scenario-feedback').classList.add('hidden');
    
    // Create choice buttons
    const choicesContainer = document.getElementById('scenario-choices');
    choicesContainer.innerHTML = '';
    
    scenario.choices.forEach((choice, index) => {
        const button = document.createElement('button');
        button.className = 'choice-btn';
        button.textContent = `${String.fromCharCode(65 + index)}. ${choice.text}`;
        button.onclick = () => selectChoice(index);
        choicesContainer.appendChild(button);
    });
    
    // Scroll to scenario player
    document.getElementById('scenario-player').scrollIntoView({ behavior: 'smooth' });
}

// Select Choice
function selectChoice(choiceIndex) {
    if (!currentScenario) return;
    
    const scenario = scenarios[currentScenario];
    const choice = scenario.choices[choiceIndex];
    
    // Remove previous selections
    document.querySelectorAll('.choice-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    
    // Mark selected choice
    document.querySelectorAll('.choice-btn')[choiceIndex].classList.add('selected');
    
    // Show feedback
    const feedbackDiv = document.getElementById('scenario-feedback');
    feedbackDiv.classList.remove('hidden', 'incorrect');
    
    if (choice.correct) {
        currentScore += 10;
        feedbackDiv.innerHTML = `
            <h4>✅ Correct!</h4>
            <p>${choice.explanation}</p>
            <button onclick="nextScenario()" class="btn-primary" style="margin-top: 1rem;">Next Scenario</button>
        `;
    } else {
        feedbackDiv.classList.add('incorrect');
        feedbackDiv.innerHTML = `
            <h4>❌ Not the best choice</h4>
            <p>${choice.explanation}</p>
            <button onclick="tryAgain()" class="btn-secondary" style="margin-top: 1rem;">Try Again</button>
        `;
    }
    
    // Update score
    document.getElementById('scenario-score').textContent = `Score: ${currentScore}`;
}

// Try Again
function tryAgain() {
    document.getElementById('scenario-feedback').classList.add('hidden');
    document.querySelectorAll('.choice-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
}

// Next Scenario
function nextScenario() {
    const scenarioIds = Object.keys(scenarios);
    const currentIndex = scenarioIds.indexOf(currentScenario);
    
    if (currentIndex < scenarioIds.length - 1) {
        const nextId = scenarioIds[currentIndex + 1];
        startScenario(nextId);
    } else {
        // All scenarios completed
        showCompletion();
    }
}

// Show Completion
function showCompletion() {
    const feedbackDiv = document.getElementById('scenario-feedback');
    feedbackDiv.classList.remove('hidden', 'incorrect');
    feedbackDiv.innerHTML = `
        <h4>🎉 All Scenarios Completed!</h4>
        <p>Final Score: ${currentScore}/40</p>
        <p><strong>Great job learning earthquake safety!</strong></p>
        <p>Remember: In a real emergency, always prioritize your safety first, then help others.</p>
        <button onclick="exitScenario()" class="btn-primary" style="margin-top: 1rem;">Back to Scenarios</button>
    `;
}

// Exit Scenario
function exitScenario() {
    document.getElementById('scenario-player').classList.add('hidden');
    currentScenario = null;
    currentScore = 0;
}

// AI Advisor Chat
function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message
    addMessage(message, 'user');
    
    // Clear input
    input.value = '';
    
    // Simulate AI response
    setTimeout(() => {
        const response = generateAIResponse(message);
        addMessage(response, 'bot');
    }, 1000);
}

// Add Message to Chat
function addMessage(message, type) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    if (type === 'bot') {
        messageDiv.innerHTML = `
            <i class="fas fa-robot"></i>
            <div class="message-content">
                <p>${message}</p>
            </div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="message-content">
                <p>${message}</p>
            </div>
        `;
    }
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Generate AI Response (Demo Mode)
function generateAIResponse(userMessage) {
    const responses = {
        'earthquake': 'During an earthquake: DROP to your hands and knees, take COVER under a sturdy desk or table, and HOLD ON until the shaking stops. Stay where you are - don\'t run outside during the shaking.',
        'emergency kit': 'Essential earthquake emergency kit items: Water (1 gallon per person per day for 3 days), non-perishable food, flashlight, first aid kit, whistle, radio, phone chargers, medications, and important documents.',
        'bangkok': 'Bangkok emergency numbers: General Emergency 191, Medical Emergency 1669, Fire Department 199. Major hospitals include Siriraj, Chulalongkorn, and Bumrungrad.',
        'myanmar': 'Myanmar emergency numbers: Emergency 999, Medical 192, Fire 191. In Yangon, major hospitals include Yangon General Hospital and North Okkalapa Hospital.',
        'building': 'After an earthquake, check for structural damage: Look for cracks in walls, broken gas lines (smell), electrical damage, and water leaks. If in doubt, evacuate and have professionals inspect.',
        'prepare': 'Earthquake preparation: Create emergency plan, identify safe spots in each room, secure heavy furniture, practice drop/cover/hold drills, keep emergency supplies, and know how to shut off utilities.',
        'default': 'I\'m here to help with earthquake safety questions! Ask me about emergency procedures, preparedness tips, regional resources for Thailand/Myanmar, or building safety assessments.'
    };
    
    const lowerMessage = userMessage.toLowerCase();
    
    for (const [key, response] of Object.entries(responses)) {
        if (lowerMessage.includes(key)) {
            return response;
        }
    }
    
    return responses.default;
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    // Show first tab by default
    showTab('simulator');
    
    // Add enter key support for chat
    document.getElementById('chat-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
}); 