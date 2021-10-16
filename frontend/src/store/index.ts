import { createStore } from 'vuex'

export type TTask = {
    id: number,
    title: string,
    description: string,
    completed: boolean,
    date_created: Date
}

export type TTaskGroup = {
    id: number,
    group_name: string,
    group_description: string,
    tasks: TTask[]
}

export type TTaskRoom = {
    id: number,
    room_name: string,
    room_description: string,
    owner_username: string,
    members: string,
    task_groups: TTaskGroup[]
}

const store = createStore({
    state: (): { taskRoom: TTaskRoom } => ({
        taskRoom: {} as TTaskRoom
    }),
    mutations: {
        clearStore(state: { taskRoom: TTaskRoom }): void {
            state.taskRoom = {} as TTaskRoom
        },
        updateRoomMembers(state: { taskRoom: TTaskRoom }, { members }: { members: string }): void {
            state.taskRoom.members = members
        },
        changeRoom(state, { room }: { room: TTaskRoom}): void {
            state.taskRoom = { ...room }
        },
        updateTaskStatus(state, { groupIdx, taskIdx, status }: { groupIdx: number, taskIdx: number, status: boolean }): void {
            state.taskRoom.task_groups[groupIdx].tasks[taskIdx].completed = status
        },
        appendTask(state, payload: { task: TTask, taskGroupId: number }): void {
            for (let group of state.taskRoom.task_groups) {
                if (group.id === payload.taskGroupId) {
                    group.tasks.push(payload.task)
                    break;
                }
            }
        },
        removeTask(state, { groupIdx, taskId }: { groupIdx: number, taskId: number }): void {
            state.taskRoom.task_groups[groupIdx].tasks = state.taskRoom.task_groups[groupIdx].tasks.filter(({ id }) => id !== taskId)
        },
        appendTaskGroup(state, payload: TTaskGroup): void {
            state.taskRoom.task_groups.push(payload)
        },
        removeTaskGroup(state, { taskGroupId }: { taskGroupId: number }): void {
            state.taskRoom.task_groups = state.taskRoom.task_groups.filter(({ id }) => id !== taskGroupId)
        }
    },
    getters: {
        taskRoom: (state): TTaskRoom => state.taskRoom,
        roomId: (state): number => state.taskRoom.id,
        roomMembers: (state): string[] => state.taskRoom.members.split(',')
    }
})

export default store