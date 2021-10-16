import axios from 'axios'

type TEndpoints = {
    csrf: string,
    registaration: string,
    login: string,
    logout: string,
    deleteAccount: string,
    updateAccount: string,
    userInfo: string,
    checkAuth: string,
    searchUser: string, 
    members: string,
    room: string,
    task: string,
    taskGroup: string
}

export function getCookie(name: string): string | null {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export const endpoints: TEndpoints = {
    csrf: 'account/csrf-token/',
    registaration: 'account/registration/',
    login: 'account/login/',
    logout: 'account/logout/',
    deleteAccount: 'account/delete-account/',
    updateAccount: 'account/update-account/',
    userInfo: 'account/user-info/',
    checkAuth: 'account/check-auth/',
    searchUser: 'account/search-user/',
    room: 'tasks/room/',
    members: 'tasks/members/',
    task: 'tasks/task/',
    taskGroup: 'tasks/task-groups/'
}

type CSRFHeader = { ['X-CSRFToken']: string }
const setCSRFHeader = (): CSRFHeader => ({ 'X-CSRFToken': getCookie('csrftoken') as string})
export default setCSRFHeader

export const request = axios.create({
    baseURL: 'http://127.0.0.1:8000/',
    withCredentials: true
})

export const debounce = (callback: Function, ms: number = 200): () => void => {
    let timeout: ReturnType<typeof setTimeout>
    return (): void => {
        clearTimeout(timeout)
        timeout = setTimeout(() => callback(), ms)
    }
}