<script setup>
import '../assets/home.css';
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
                <input type="text" id="model" placeholder="e.g., google/flan-t5-base" />
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