<script setup>
import { ref } from 'vue';
import '../assets/home.css';

const modelInput = ref('google/flan-t5-base');

const getLLMResults = async (modelName) => {
    try {
        const res = await fetch(`http://localhost:8000/llm/?model_name=${modelName}`);
        const data = await res.json();
        console.log(data);
    } catch (error) {
        console.log(`got err hitting API URI: ${error}`);
    }
};

</script>

<template>
    <main>
        <h1>Fend. Interact with tons of LLM models from HuggingFace effortlessly</h1>
        <div class="chat-container">
            <div class="chat-area">
                <!-- Static example messages, will be replaced when backend is up and running -->
                <div class="message user">Hi there!</div>
                <div class="message bot">Hello! How can I assist you today?</div>
                <div class="chat-input">
                    <input type="text" placeholder="Type your prompt here..." />
                    <button>Send</button>
                </div>
            </div>
        </div>
        <div class="controls">
            <div class="model-select">
                <label for="model">Model:</label>
                <input 
                    type="text" 
                    id="model" 
                    v-model="modelInput" 
                    placeholder="e.g., google/flan-t5-base" 
                />
                <button @click="getLLMResults(modelInput)">Set model</button>
            </div>
            <div class="params">
                <label for="temperature">Temperature: 0.1</label>
                <input type="range" id="temperature" min="0.1" max="1.0" step="0.1" value="0.1" />
                <label for="maxLength">Max Length: 100</label>
                <input type="number" id="maxLength" min="10" max="500" step="10" value="100" />
            </div>
        </div>
    </main>
</template>