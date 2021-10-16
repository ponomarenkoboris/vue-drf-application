import { createRouter, createWebHistory } from 'vue-router'
import { request, endpoints } from '../utils'
import App from '../App.vue'

const routes = [
    {
        name: 'App',
        path: '/',
        component: App
    },
    {
        name: 'Authorization',
        path: '/auth',
        component: () => import(/* webpackChunkName: "authorization" */ '../views/AuthorizationView.vue')
    },
    {
        name: 'TaskView',
        path: '/tasks',
        component: () => import(/* webpackChunkName: "task-view" */ '../views/TaskView.vue')
    },
    {
        name: 'Chat',
        path: '/chat',
        component: () => import(/* webpackChunkName: "chat" */ '../views/ChatView.vue')
    },
    {
        name: 'Settings',
        path: '/settings',
        component: () => import(/* webpackChunkName: "settings" */ '../views/SettingsView.vue')
    },
    {
        name: 'TextEditor',
        path: '/text-editor',
        component: () => import(/* webpackChunkName: "text-editor" */ '../views/TextEditor.vue')
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, _, next) => {
    if (to.path !== '/auth') {
        request.get(endpoints.checkAuth)
            .then((res: { data: any }) => {
                res.data?.isAuthenticated === 'success' ? next() : next({ name: 'Authorization' })
            })
            .catch(() => next({ name: 'Authorization' }))
    }
    else next()
})

export default router