<script setup lang="ts">
import Sidebar from '../components/layout/Sidebar.vue'
import TaskGroup from '../components/tasks/TaskGroup.vue'
import setCSRFHeader, { request, endpoints, debounce } from '../utils'
import { TTaskRoom, TTaskGroup } from '../store'
import { ref, computed, reactive, watch } from 'vue'
import { useStore } from 'vuex'

const { getters, commit } = useStore()

const taskRoom = computed((): TTaskRoom => getters.taskRoom)
const roomsNames = ref<string[]>([])
const newTaskGroupData = reactive<{ name: string, description: string }>({ name: '', description: '' })
const username = ref<string>('')
const findUserModal = ref<boolean>(false)
const foundedUsers = ref<string[]>([])
const checkedFoundedUser = ref<string | null>(null)
const showFoundedUserSpin = ref<boolean>(false)

watch(findUserModal, (_, prev) => { if (prev) username.value = ''; foundedUsers.value = []; checkedFoundedUser.value = null })

request.get(endpoints.room)
    .then(response => {
        if (response.data.rooms) {
            roomsNames.value = response.data.rooms as string[]
        }
    })
    .catch(err => {
        console.log(err)
    })

enum UserActions {
    DELETE = 'remove',
    APPEND = 'append',
    FINDUSER = 'find'
}

type TMember = {
    label: string,
    key: string,
    children?: any[],
}

const members = computed<TMember[]>((): TMember[] => {
    const owner = getters.taskRoom.owner_username
    const appendButton = [{ 
        label: 'Append user', 
        key: `${UserActions.FINDUSER}_`,
    }]
    const members = getters.roomMembers.map((member: string): TMember => {
        const options: TMember = { key: member, label: member }

        if (owner !== member) options.children = [
            { 
                label: 'Remove user', 
                key: `${UserActions.DELETE}_${member}`,
            }
        ]
        
        return options
    })

    return appendButton.concat(members)
})

const appendTaskGroup = async (): Promise<void> => {
    const payload = { groupName: newTaskGroupData.name, groupDescription: newTaskGroupData.description }

    try {
        const response = await request.post(
            endpoints.taskGroup, 
            { roomId: taskRoom.value.id, ...payload }, 
            { headers: {...setCSRFHeader()} }
        )
        if (response.data.success && response.data.taskGroup) {
            commit('appendTaskGroup', response.data.taskGroup as TTaskGroup)
        }
    } catch (error) {
        console.error(error)

    }

    newTaskGroupData.name = ''
    newTaskGroupData.description = ''
}

const deleteRoom = async (): Promise<void> => {
    const roomId = getters.roomId

    try {
        const response = await request.delete(endpoints.room, { data: { roomId }, headers: { ...setCSRFHeader() } })
        if (response.data.success) {
            const roomName = getters.taskRoom.room_name
            roomsNames.value = roomsNames.value?.filter(name => name !== roomName)
            commit('clearStore')
        }
    } catch (error) {
        console.error(error)
    }
}

// Handel dropdown logic
const handleSelect = async (key: string): Promise<void> => {
    const [ actionType, memberUserName ] = key.split('_')
    const roomId = taskRoom.value.id

    if (actionType === UserActions.DELETE) {
        try {
            const response = await request.delete(endpoints.members, { data: { roomId,  memberUserName }, headers: { ...setCSRFHeader() } })
            if (response.data.success) {
                const members = getters.roomMembers.filter((username: string) => username !== memberUserName).join(',')
                commit('updateRoomMembers', { members })
            }
        } catch (error) {
            console.error(error)
        }
    }

    if (actionType === UserActions.APPEND) {
        const usernameValue = checkedFoundedUser.value || memberUserName
        if (usernameValue.trim().length === 0) return
        
        try {
            const response = await request.put(endpoints.members, { roomId, memberUserName: usernameValue }, { headers: { ...setCSRFHeader() } })
            if (response.data.success) {
                const members = Array.from(getters.roomMembers)
                members.push(usernameValue)
                commit('updateRoomMembers', { members: members.join(',') })
                username.value = ''
                findUserModal.value = false
            }
        } catch(error) {
            console.error(error)
        }
    }

    if (actionType === UserActions.FINDUSER) findUserModal.value = true
}

// Get founded users list
const getUsersList = async (): Promise<void> => {
    if (username.value.trim().length === 0) return
    showFoundedUserSpin.value = true

    try {
        const response = await request.post(endpoints.searchUser, { username: username.value }, { headers: { ...setCSRFHeader() } })
        if (response.data.success && response.data.users) {
            foundedUsers.value = response.data.users as string[]
        }
    } catch (error) {
        console.error(error)
    }

    showFoundedUserSpin.value = false
}

const debGetUserList = debounce(getUsersList, 1000)

</script>
<template>
    <n-layout style="height: 90vh;">
        <n-layout-header
            style="height: 50px;"
            bordered
        >
            <n-space v-if="taskRoom.id" justify="center">
                <n-h2>
                    Name: <n-gradient-text type="success">{{ taskRoom.room_name }}</n-gradient-text>
                </n-h2>
                <n-h2>
                    Description: <n-gradient-text type="success">{{ taskRoom.room_description }}</n-gradient-text>
                </n-h2>
                <n-button type="error" ghost @click="deleteRoom">Delete room</n-button>
                <n-dropdown
                    @select="handleSelect"
                    trigger="hover" 
                    :options="members"
                    :show-arrow="true"
                    size="huge"
                >
                    <n-button>Users list</n-button>
                </n-dropdown>
                
            </n-space>
        </n-layout-header>
        <n-modal
            class="custom-card"
            v-model:show="findUserModal"
            preset="card"
            style="max-width: 600px"
            title="Append user to the room"
            :bordered="false"
            :segmented="{
                content: 'soft',
                footer: 'soft'
            }"
        >
            <n-form>
                <n-input 
                    v-model:value="username" 
                    placeholder="Enter username" 
                    @input="debGetUserList"
                />
            </n-form>
            <div class="radio_wrapper">
                <n-spin :show="showFoundedUserSpin">
                    <n-radio 
                        class="radio_item"
                        v-for="(username, idx) in foundedUsers" 
                        :key="idx"
                        :checked="checkedFoundedUser === username"
                        @change="() => checkedFoundedUser = username"
                    >
                        {{ username }}
                    </n-radio>
                </n-spin>
            </div>
            <template #footer>
                <n-button 
                    type="primary" 
                    block 
                    @click="handleSelect(`${UserActions.APPEND}_${username}`)"
                >
                    Appned user
                </n-button>
            </template>
        </n-modal>
        <n-layout position="absolute" style="top: 40px; bottom: 64px;" has-sider>
            <Sidebar place="tasks" :roomsNames="roomsNames"/>
            <n-layout 
                content-style="padding: 24px;" 
                :native-scrollbar="false"
            >   
                <n-space>
                    <TaskGroup 
                        v-for="(taskGroup, groupIdx) in taskRoom.task_groups" 
                        :key="taskGroup.id"
                        :groupIndex="groupIdx"
                        :groupId="taskGroup.id"
                        :groupName="taskGroup.group_name"
                        :groupDescription="taskGroup.group_description"
                        :tasks="taskGroup.tasks"
                    />
                </n-space>
            </n-layout>
        </n-layout>
        <n-layout-footer
            position="absolute"
            style="height: 64px; padding: 24px;"
            bordered
        >
            <n-space v-if="taskRoom.id" justify="center">
                <n-form style="display: flex; margin-right: 10px;">
                    <n-input 
                        style="margin-right: 10px;"
                        placeholder="Group title" 
                        v-model:value="newTaskGroupData.name"
                    />
                    <n-input 
                        placeholder="Group description" 
                        v-model:value="newTaskGroupData.description"
                    />
                </n-form>
                <n-button type="primary" @click="appendTaskGroup">Create new task Group</n-button>
            </n-space>
        </n-layout-footer>
    </n-layout>
</template>
<style lang="scss" setup>
.radio_wrapper {
    display: flex;
    flex-direction: column;
    margin-top: 20px;
    min-height: 20px;

    .radio_item {
        margin-bottom: 10px;
        font-size: 15px;

        &:last-child {
            margin-bottom: 0px;
        }
    }
}
</style>