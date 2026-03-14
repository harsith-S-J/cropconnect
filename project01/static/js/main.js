// Modal toggling
function toggleModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal.classList.contains('show')) {
        modal.classList.remove('show');
        setTimeout(() => modal.style.display = 'none', 300);
    } else {
        modal.style.display = 'flex';
        // forced reflow for transition
        void modal.offsetWidth;
        modal.classList.add('show');
    }
}

// Close modal when clicking outside of it
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        toggleModal(event.target.id);
    }
}

// Table filtering
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('tableSearch');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const filter = searchInput.value.toLowerCase();
            const table = document.getElementById('cropsTable');
            const trs = table.getElementsByTagName('tr');

            // Start from index 1 to skip header
            for (let i = 1; i < trs.length; i++) {
                // Ignore the empty state row
                if (trs[i].querySelector('.empty-state')) continue;

                let tdText = trs[i].textContent || trs[i].innerText;
                if (tdText.toLowerCase().indexOf(filter) > -1) {
                    trs[i].style.display = "";
                } else {
                    trs[i].style.display = "none";
                }
            }
        });
    }

    // Auto-dismiss flashes after 5s
    setTimeout(function() {
        const flashes = document.querySelectorAll('.alert');
        flashes.forEach(flash => {
            flash.style.opacity = '0';
            flash.style.transition = 'opacity 0.5s ease-out';
            setTimeout(() => flash.remove(), 500);
        });
    }, 5000);
});

// AI Assistant Logic
function toggleAIChat() {
    const chatWindow = document.getElementById('aiChatWindow');
    chatWindow.classList.toggle('open');
}

function handleAIKeyPress(event) {
    if (event.key === 'Enter') {
        sendAIMessage();
    }
}

function sendAIMessage() {
    const input = document.getElementById('aiInput');
    const msg = input.value.trim();
    if (!msg) return;

    const messagesContainer = document.getElementById('aiMessages');

    // Add User Message
    const userMsgDiv = document.createElement('div');
    userMsgDiv.className = 'ai-msg msg-user';
    userMsgDiv.textContent = msg;
    messagesContainer.appendChild(userMsgDiv);
    
    input.value = '';
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    // Simulate AI Response
    setTimeout(() => {
        const aiMsgDiv = document.createElement('div');
        aiMsgDiv.className = 'ai-msg msg-system';
        
        // Very basic mock responses based on keywords
        const lowerMsg = msg.toLowerCase();
        if (lowerMsg.includes('predict') || lowerMsg.includes('yield')) {
            aiMsgDiv.textContent = "Based on regional data in your location, expected yields for this season are projected to be 15% higher than last year if current protection strategies are maintained.";
        } else if (lowerMsg.includes('weather') || lowerMsg.includes('rain')) {
            aiMsgDiv.textContent = "Forecasts indicate moderate rainfall over the next two weeks. Ensure adequate drainage for newly planted crops.";
        } else if (lowerMsg.includes('price') || lowerMsg.includes('market')) {
            aiMsgDiv.textContent = "Currently, local market demand is high for Wheat and Corn. Consider these if you are planning your next cycle.";
        } else {
            aiMsgDiv.textContent = "That's an excellent question. To give you the most accurate agricultural analysis, I'm currently reviewing regional cultivation trends. Can you provide more specifics about your farm's soil or current crop phase?";
        }

        messagesContainer.appendChild(aiMsgDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }, 1000);
}
