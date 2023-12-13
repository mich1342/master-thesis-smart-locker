import { createWebHashHistory, createRouter } from "vue-router"
import Home from '../routes/Home.vue'
import Assign from '../routes/Assign.vue'
import Pick from '../routes/Pick.vue'

const routes = [
    {
        path: '/',
        component: Home
    },
    {
        path: '/pick',
        component: Pick
    },
    {
        path: '/assign',
        component: Assign
    },
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router