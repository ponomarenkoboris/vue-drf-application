<script lang="ts" setup>
import Message from '../components/chat/Message.vue'
import { useStore } from 'vuex'
import { ref } from 'vue'

const { getters } = useStore()
const chatMessages = ref<any[]>([])
const messageInput = ref<string>('')

const host = window.location.host.split(':')[1] === '3000' ? '127.0.0.1:8000' : window.location.host
const roomName = getters.taskRoom.room_name ? getters.taskRoom.room_name.replaceAll(' ', '_') : null
let chatSocket: null | WebSocket = null

if (roomName) {
    chatSocket = new WebSocket(`ws://${host}/ws/chat/${roomName}/`)
    
    chatSocket.onmessage = (e) => {
        const data = JSON.parse(e.data)
        if (data.room) {
            data.room.messages.forEach((message: any) => chatMessages.value.push(message))
        } else chatMessages.value.push(data)
    }
    
    chatSocket.onclose = (e) => {
        console.error('Chat socket closed unexpectedly');
    }
    
}

const sendMessage = () => {
    if (messageInput.value.trim().length === 0) return
    if (chatSocket) {
        chatSocket.send(JSON.stringify({
            'type': 'chat_message',
            'sender': localStorage.getItem('username'),
            'message': messageInput.value
        }))
        messageInput.value = ''
    }
}


</script>
<template>
    <n-layout
        v-if="chatSocket"
        style="height: 90vh;"
    >
        <n-layout-header 
            style="height: 64px; padding: 24px;" 
            bordered
        >
            <n-h2>
                <n-gradient-text :size="24" type="success">{{ getters.taskRoom.room_name }}</n-gradient-text>
            </n-h2>
        </n-layout-header>
        <n-layout 
            position="absolute" 
            style="top: 64px; bottom: 64px;" 
            :native-scrollbar="false"
        >
            <n-layout content-style="padding: 24px;" :native-scrollbar="false">
                <Message
                    v-for="(message, idx) in chatMessages" 
                    :key="idx"
                    :sender="message.sender"
                    :message="message.message"
                    :type="message.type"
                />
            </n-layout>
        </n-layout>
        <n-layout-footer
            position="absolute"
            style="height: 64px; padding: 24px;"
            bordered
        >
            <n-form class="message_form">
                <n-input 
                    class="message_input" 
                    placeholder="Type message"
                    v-model:value="messageInput"
                    @keydown.enter="sendMessage"
                />
                <n-button type="primary" @click="sendMessage">Send message</n-button>
            </n-form>
        </n-layout-footer>
    </n-layout>
    <n-space v-else justify="center">
        <n-h2>Enter in a room!</n-h2>
    </n-space>
</template>
<style lang="scss" scoped>
.message_form {
    display: flex;

    .message_input {
        margin-right: 10px;
    }
}
</style>