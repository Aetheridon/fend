<script setup>
import { ref } from 'vue';
import '../assets/home.css';

const modelInput = ref('google/flan-t5-base');
const promptInput = ref('');
const messages = ref([]);
const temperature = ref(0.1);
const maxLength = ref(100);

const sendPrompt = async () => {
    if (!promptInput.value.trim()) return;

    messages.value.push({ text: promptInput.value, sender: 'user' });

    try {
        const res = await fetch('http://localhost:8000/infer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model_name: modelInput.value,
                prompt: promptInput.value,
                max_length: maxLength.value,
                temperature: temperature.value
            })
        });
        const data = await res.json();
        
        messages.value.push({ text: data.response, sender: 'bot' });
        console.log(`Response: ${data.response}`);
    } catch (error) {
        console.error(`Error hitting API URI: ${error}`);
        messages.value.push({ text: "Error: Couldn't get a response from the server.", sender: 'bot' });
    }

    promptInput.value = '';
};
</script>

<template>
    <main>
        <h1>Fend. Interact with tons of LLM models from HuggingFace effortlessly</h1>
        <div class="chat-container">
            <div class="chat-area">
                <!-- Render messages dynamically -->
                <div v-for="(message, index) in messages" :key="index" :class="['message', message.sender]">
                    {{ message.text }}
                </div>
                <!-- Chat input -->
                <div class="chat-input">
                    <input v-model="promptInput" type="text" placeholder="Type your message..." @keyup.enter="sendPrompt" />
                    <button @click="sendPrompt">Send</button>
                </div>
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