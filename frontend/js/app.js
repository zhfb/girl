let config = null;
let ws = null;
let isGenerating = false;

const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const settingsBtn = document.getElementById('settingsBtn');
const settingsModal = document.getElementById('settingsModal');
const closeModal = document.getElementById('closeModal');
const saveSettingsBtn = document.getElementById('saveSettingsBtn');
const clearChatBtn = document.getElementById('clearChatBtn');

const modelSelect = document.getElementById('modelSelect');
const apiKey = document.getElementById('apiKey');
const apiBase = document.getElementById('apiBase');
const modelName = document.getElementById('modelName');
const charName = document.getElementById('charName');
const charPersonality = document.getElementById('charPersonality');

async function loadConfig() {
    try {
        const response = await fetch('/api/config');
        config = await response.json();
        populateSettings();
    } catch (e) {
        console.error('加载配置失败:', e);
    }
}

function populateSettings() {
    if (!config) return;
    
    modelSelect.value = config.active_llm || 'deepseek';
    
    const llmConfig = config.llm_models?.[config.active_llm] || {};
    apiKey.value = llmConfig.api_key || '';
    apiBase.value = llmConfig.api_base || '';
    modelName.value = llmConfig.model || '';
    charName.value = config.character?.name || '';
    
    const personality = config.character?.personality || [];
    charPersonality.value = personality.join(',');
}

async function saveConfig() {
    if (!config) {
        await loadConfig();
    }
    
    config.active_llm = modelSelect.value;
    
    if (!config.llm_models) {
        config.llm_models = {};
    }
    config.llm_models[modelSelect.value] = {
        api_key: apiKey.value,
        api_base: apiBase.value,
        model: modelName.value,
        temperature: 0.7,
        max_tokens: 2000
    };
    
    if (!config.character) {
        config.character = {};
    }
    config.character.name = charName.value;
    config.character.personality = charPersonality.value.split(',').map(s => s.trim()).filter(s => s);
    
    try {
        await fetch('/api/config', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(config)
        });
        alert('设置已保存！');
        hideSettingsModal();
    } catch (e) {
        alert('保存失败: ' + e.message);
    }
}

function showSettingsModal() {
    settingsModal.classList.add('show');
    populateSettings();
}

function hideSettingsModal() {
    settingsModal.classList.remove('show');
}

function addMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.textContent = role === 'user' ? '😊' : '🤖';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const paragraphs = content.split('\n').filter(p => p.trim());
    paragraphs.forEach(p => {
        const pEl = document.createElement('p');
        pEl.textContent = p;
        contentDiv.appendChild(pEl);
    });
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function addTypingIndicator() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    messageDiv.id = 'typing-indicator';
    
    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.textContent = '🤖';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const indicator = document.createElement('div');
    indicator.className = 'typing-indicator';
    indicator.innerHTML = '<span></span><span></span><span></span>';
    
    contentDiv.appendChild(indicator);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}

function updateLastAssistantMessage(content) {
    const messages = chatMessages.querySelectorAll('.message.assistant');
    if (messages.length > 0) {
        const lastMessage = messages[messages.length - 1];
        const contentDiv = lastMessage.querySelector('.message-content');
        contentDiv.innerHTML = '';
        
        const paragraphs = content.split('\n').filter(p => p.trim());
        paragraphs.forEach(p => {
            const pEl = document.createElement('p');
            pEl.textContent = p;
            contentDiv.appendChild(pEl);
        });
        scrollToBottom();
    }
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function connectWebSocket() {
    const wsUrl = `ws://${window.location.host}/ws/chat`;
    ws = new WebSocket(wsUrl);
    
    let currentContent = '';
    
    ws.onopen = () => {
        console.log('WebSocket连接成功');
    };
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        switch (data.type) {
            case 'start':
                removeTypingIndicator();
                currentContent = '';
                addMessage('assistant', '');
                break;
            case 'chunk':
                currentContent += data.content;
                updateLastAssistantMessage(currentContent);
                break;
            case 'done':
                isGenerating = false;
                sendBtn.disabled = false;
                break;
            case 'error':
                removeTypingIndicator();
                alert(data.message);
                isGenerating = false;
                sendBtn.disabled = false;
                break;
        }
    };
    
    ws.onerror = (error) => {
        console.error('WebSocket错误:', error);
    };
    
    ws.onclose = () => {
        console.log('WebSocket连接关闭');
        setTimeout(connectWebSocket, 3000);
    };
}

async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message || isGenerating) return;
    
    if (!ws || ws.readyState !== WebSocket.OPEN) {
        alert('连接未就绪，请稍候...');
        return;
    }
    
    addMessage('user', message);
    messageInput.value = '';
    
    isGenerating = true;
    sendBtn.disabled = true;
    addTypingIndicator();
    
    ws.send(JSON.stringify({ message }));
}

async function clearChat() {
    if (confirm('确定要清空对话历史吗？')) {
        try {
            await fetch('/api/chat/clear', { method: 'POST' });
            chatMessages.innerHTML = `
                <div class="message assistant">
                    <div class="avatar">🤖</div>
                    <div class="message-content">
                        <p>你好呀！我是你的AI女友，很高兴认识你！</p>
                    </div>
                </div>
            `;
            hideSettingsModal();
        } catch (e) {
            alert('清空失败: ' + e.message);
        }
    }
}

settingsBtn.addEventListener('click', showSettingsModal);
closeModal.addEventListener('click', hideSettingsModal);
saveSettingsBtn.addEventListener('click', saveConfig);
clearChatBtn.addEventListener('click', clearChat);
sendBtn.addEventListener('click', sendMessage);

messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

settingsModal.addEventListener('click', (e) => {
    if (e.target === settingsModal) {
        hideSettingsModal();
    }
});

document.addEventListener('DOMContentLoaded', () => {
    loadConfig();
    connectWebSocket();
});
