<script setup>
import { ref, nextTick, onMounted, watch } from 'vue';
import '../assets/home.css';

const modelInput = ref('google/flan-t5-base');
const promptInput = ref('');
const messages = ref([]);
const temperature = ref(0.1);
const maxLength = ref(100);
const isLoading = ref(false);
const chatAreaRef = ref(null);

const scrollToBottom = async () => {
  await nextTick();
  if (chatAreaRef.value) {
    chatAreaRef.value.scrollTop = chatAreaRef.value.scrollHeight;
  }
};

watch(messages, () => {
  scrollToBottom();
}, { deep: true });

const sendPrompt = async () => {
    if (!promptInput.value.trim() || isLoading.value) return;
    
    const promptToSend = promptInput.value;
    
    promptInput.value = "";

    messages.value.push({ text: promptToSend, sender: 'user' });
    
    isLoading.value = true;
    
    messages.value.push({ isTyping: true, sender: 'bot' });
    
    try {
        const res = await fetch('http://localhost:8000/infer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model_name: modelInput.value,
                prompt: promptToSend,
                max_length: maxLength.value,
                temperature: temperature.value
            })
        });
        const data = await res.json();
        
        messages.value.pop()
        messages.value.push({ text: data.response, sender: 'bot' });
        console.log(`Response: ${data.response}`);

    } catch (error) {
        console.error(`Error hitting API URI: ${error}`);
        messages.value.pop();
        messages.value.push({ text: "Error: Couldn't get a response from the server.", sender: 'bot' });

    } finally {
        isLoading.value = false;
        scrollToBottom();
    }
};

onMounted(() => {
    const inputEl = document.querySelector('.chat-input input');
    if (inputEl) inputEl.focus();
});
</script>

<template>
    <main>
        <h1>Fend. Interact with tons of LLM models from HuggingFace effortlessly</h1>
        <div class="chat-container">
            <div class="chat-area" ref="chatAreaRef">
                <div v-for="(message, index) in messages" :key="index" :class="['message', message.sender]">
                    <div v-if="message.isTyping" class="typing-indicator">
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                    </div>
                    <template v-else>{{ message.text }}</template>
                </div>
            </div>
        </div>
        <div class="chat-controls">
            <div class="chat-input">
                <input 
                    v-model="promptInput" 
                    type="text" 
                    placeholder="Type your message..." 
                    @keyup.enter="sendPrompt" 
                    :disabled="isLoading" 
                />
                <button @click="sendPrompt" :disabled="isLoading">
                    {{ isLoading ? 'Sending...' : 'Send' }}
                </button>
            </div>
        </div>
        <div class="controls">
            <div class="model-select">
                <label for="model">Model:</label>
                <input v-model="modelInput" type="text" id="model" placeholder="e.g., google/flan-t5-base" />
            </div>
            <div class="params">
                <label for="temperature">Temperature: {{ temperature }}</label>
                <input v-model="temperature" type="range" id="temperature" min="0.1" max="1.0" step="0.1" />
                <label for="maxLength">Max Length: {{ maxLength }}</label>
                <input v-model="maxLength" type="number" id="maxLength" min="10" max="500" step="10" />
            </div>
        </div>
    </main>
</template>