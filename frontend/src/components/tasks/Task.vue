<script setup lang="ts">
import { useStore } from 'vuex'
import { TrashCan } from '@vicons/carbon'
import setCSRFHeader, { request, endpoints } from '../../utils'

const props = defineProps({
    groupIndex: [Number, String, Symbol],
    groupId: Number,
    taskIdx: [Number, String, Symbol],
    id: Number,
    title: String,
    description: String,
    completed: Boolean,
    dateCreated: {
        required: true,
        type: Date
    }
})

const store = useStore()

const updateTaskStatus = async (): Promise<void> => {
    const payload = { groupIdx: props.groupIndex, taskIdx: props.taskIdx, status: !props.completed }
    
    try {
        const response = await request.put(
            endpoints.task,
            { roomId: store.getters.roomId, taskStatus: payload.status, taskId: props.id, taskGroupId: props.groupId },
            { headers: { ...setCSRFHeader() } }
        )
        if (response.data.success) {
            store.commit('updateTaskStatus', payload)
        }
    } catch (error) {
        console.error(error)
    }
}

const removeTask = async (event: MouseEvent): Promise<void> => {
    event.stopPropagation()
    const payload = { groupIdx: props.groupIndex, taskId: props.id }

    try {
        const response = await request.delete(
            endpoints.task,
            { 
                data: { roomId: store.getters.roomId, taskGroupId: props.groupId, taskId: props.id },
                headers: { ...setCSRFHeader() }
            }
        )
        if (response.data.success) {
            store.commit('removeTask', payload)
        }
    } catch (error) {
        console.error()
    }
}
</script>
<template>
    <n-card :title="title" :class="completed ? 'task compoleted__task' : 'task'" @click="updateTaskStatus">
        <template #header-extra>
            <n-tag style="margin-left: 10px;" :class="completed ? 'task__tag' : ''" :type="completed ? 'success' : 'error'">{{ completed ? 'Done' : 'In Progress' }}</n-tag>
        </template>
        <p>{{ description }}</p>
        <template #footer>
            <n-space justify="space-between" class="card__footer">
                <p>Date created: {{ dateCreated.toLocaleDateString() }}</p>
                <n-button type="error" ghost @click="removeTask($event)">
                    <n-icon size="15">
                        <TrashCan />
                    </n-icon>
                </n-button>
            </n-space>
        </template>
    </n-card>
</template>

<style lang="scss" scoped>
.task {
    margin-bottom: 10px;
    cursor: pointer;
    transition: all 0.3s linear;

    .task__tag {
        display: none;
    }

    .card__footer {
        visibility: hidden;
    }

    &:hover {
        background-color: #f7f7f7;
        transform: scale(1.1, 1.1);

        .card__footer {
            visibility: visible;
        }
        .task__tag {
            display: block;
        }
    }
}

.compoleted__task {
    background-color: rgba(24, 160, 88, 0.75);
}
</style>