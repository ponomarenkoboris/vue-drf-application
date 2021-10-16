<script lang="ts" setup>
defineProps({
    sender: String,
    message: String,
    type: String
})
const currentUsername = localStorage.getItem('username')
</script>
<template>
    <div :class="sender !== currentUsername ? 'member_message' : 'message_owner'">
        <div 
            class="message"
            :style="{ backgroundColor: sender !== currentUsername ? '#d5d8de' : 'rgba(24, 160, 88, 0.6)'}"
        >
            <p class="message_sender">{{ sender }}</p>
            <p class="message_text-message">{{ message }}</p>
        </div>
    </div>
</template>
<style lang="scss" scope>
.message_owner {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 15px;
}

.member_message {
    display: flex;
    margin-bottom: 15px;
}

.message {
    max-width: 800px;
    padding: 5px 10px;
    background-color: aqua;
    border-radius: 10px;

    .message_sender {
        font-size: 15px;
        font-weight: bold;
        margin: 0;
    }

    .message_text-message {
        margin: 0;
        word-wrap: break-word;
    }
}
</style>