<script lang="ts" setup>
import Task from './Task.vue'
import { FilterRemove, Add } from '@vicons/carbon'
import { ref, reactive, PropType } from 'vue'
import { useStore } from 'vuex'
import setCSRFHeader, { request, endpoints } from '../../utils'
import { TTask } from '../../store'

const props = defineProps({
    groupIndex: Number,
    groupId: Number,
    groupName: String,
    groupDescription: String,
    tasks: Array as PropType<TTask[]>
})

const store = useStore()
const showModal = ref<boolean>(false)

type newTaskDataType = { title: string, description: string }
const newTaskData = reactive<newTaskDataType>({ title: '', description: '' })

const createNewTask = async (): Promise<void> => {

    try {
        const response = await request.post(
            endpoints.task,
            { 
                roomId: store.getters.roomId, 
                taskTitle: newTaskData.title, 
                taskDescription: newTaskData.description, 
                taskGroupId: props.groupId 
            },
            { headers: { ...setCSRFHeader() } }
        )
        if (response.data.success && response.data.task) {
            store.commit('appendTask', { task: {...response.data.task as TTask}, taskGroupId: props.groupId })
            showModal.value = false
            newTaskData.title = ''
            newTaskData.description = ''
        }
    } catch (error) {
        console.error(error)
    }
}

const removeTaskGroup = async (): Promise<void> => {
    const payload = { taskGroupId: props.groupId }

    try {
        const response = await request.delete(
            endpoints.taskGroup,
            {
                data: { roomId: store.getters.roomId, ...payload },
                headers: { ...setCSRFHeader() }
            }
        )
        if (response.data.success) {
            store.commit('removeTaskGroup', payload)
        }
    } catch (error) {
        console.error(error)
    }
}

</script>
<template>
    <n-card :title="groupName">
        <template #header-extra>
            <n-button type="error" ghost @click="removeTaskGroup">
                <n-icon>
                    <FilterRemove />
                </n-icon>
            </n-button>
        </template>
        <h2>
            <strong>{{ groupDescription }}</strong>
        </h2>
        
        <Task
            v-for="(task, taskIdx) in tasks"
            :groupIndex="groupIndex"
            :groupId="groupId"
            :taskIdx="taskIdx" 
            :id="task.id" 
            :title="task.title" 
            :description="task.description" 
            :completed="task.completed" 
            :dateCreated="new Date(task.date_created)" 
        />
        
        <template #action>
            <n-space justify="center">
                <n-button @click="() => showModal = true">
                    Append new task
                    <n-icon>
                        <Add />
                    </n-icon>
                </n-button>
                <n-modal 
                    class="custom-card" 
                    v-model:show="showModal" 
                    preset="card" style="width: 600px" 
                    title="Creating task" 
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
                            placeholder="Enter task title" 
                            v-model:value="newTaskData.title" 
                        />
                        <n-input 
                            style="height: 40px;" 
                            type="text" 
                            placeholder="Enter task description" 
                            v-model:value="newTaskData.description" 
                        />
                    </n-form>
                    <template #footer>
                        <n-space justify="center">
                            <n-button 
                                type="primary" 
                                @click="createNewTask"
                            >
                                Submit
                            </n-button>
                        </n-space>
                    </template>
                </n-modal>
            </n-space>
        </template>
    </n-card>
</template>