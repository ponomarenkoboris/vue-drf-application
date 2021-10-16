<script lang="ts" setup>
import { PropType, reactive, ref } from 'vue'
import setCSRFHeader, { request, endpoints } from '../../utils';
import { useStore } from 'vuex'

const props = defineProps({
    roomsNames: {
        required: true,
        type: Array as PropType<string[]>,
    },
    place: {
        type: String,
        required: true
    }
})

type TRoomData = {
    roomName: string,
    roomDescription: string
}

const store = useStore()
const roomData = reactive<TRoomData>({ roomName: '', roomDescription: '' })
const showModal = ref<boolean>(false)
const searchName = ref<string>('')

const renderRoom = async (roomName: string): Promise<void> => {
    if (props.place === 'tasks') {

        const validRoomName: string = roomName.replaceAll(' ', '&')

        try {
            const response = await request.get(endpoints.room + validRoomName)
            if (response.data.room) {
                const { room } = response.data
                store.commit('changeRoom', { room })
            }
        } catch (error) {
            console.error(error)
        }

    }
}

const createRoom = async (): Promise<void> => {
    if (roomData.roomName.trim().length === 0 || roomData.roomDescription.trim().length === 0) return

    try {
        const response = await request.post(endpoints.room, roomData, { headers: { ...setCSRFHeader() }})
        if (response.data.success) {
            props.roomsNames.push(roomData.roomName)
            showModal.value = false
            roomData.roomName = ''
            roomData.roomDescription = ''
        }
    } catch (error) {
        console.error(error)
    }
}

</script>
<template>
    <n-layout-sider
        content-style="padding: 24px;"
        :native-scrollbar="false"
        bordered
    >   
        <n-button 
            type="primary" 
            block 
            style="margin-bottom: 10px;"
            @click="() => showModal = true"
        >
            Create Room
        </n-button>
        <n-modal 
            class="custom-card" 
            v-model:show="showModal" 
            preset="card" style="width: 600px" 
            title="Creating room" 
            :bordered="false" 
            size="huge" 
            :segmented="{
                content: 'soft',
                footer: 'soft'
            }"
        >
            <n-form>
                <n-input 
                    style="margin-bottom: 20px; height: 40px;" 
                    type="text" 
                    placeholder="Enter room name" 
                    v-model:value="roomData.roomName" 
                />
                <n-input 
                    style="height: 40px;" 
                    type="text" 
                    placeholder="Enter room description" 
                    v-model:value="roomData.roomDescription" 
                />
            </n-form>
            <template #footer>
                <n-space justify="center">
                    <n-button 
                        type="primary" 
                        @click="createRoom"
                    >
                        Create room
                    </n-button>
                </n-space>
            </template>
        </n-modal>
        <n-input 
            placeholder="Search"
            v-model:value="searchName"
        />
        <div v-if="roomsNames">
            <n-card 
                v-for="(roomName, idx) in roomsNames" 
                :key="idx"
                hoverable
                :class="roomName.indexOf(searchName) !== -1 ? 'card_wrapper' : 'hide'"
                @click="renderRoom(roomName)"
            >
                <n-h2 v-if="!searchName">{{ roomName }}</n-h2>
                <n-h2 v-else>
                    {{ roomName.slice(0, roomName.search(searchName)) }}<mark>{{ roomName.slice(roomName.search(searchName), roomName.search(searchName) + searchName.length) }}</mark>{{ roomName.slice(roomName.search(searchName) + searchName.length) }}
                </n-h2>
            </n-card>
        </div>
        <div v-else>
            <n-h2>You have not enter in room</n-h2>
        </div>
    </n-layout-sider>
</template>
<style lang="scss" scoped>
.card_wrapper {
    margin-top: 10px;
    cursor: pointer;
    text-align: center;

    .n-card__content > .n-h2 {
        margin: 0;
    }
}
.hide {
    display: none;
}
</style>