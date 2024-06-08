import { createRouter, createWebHistory} from 'vue-router'
import Home from "@/manager/components/home.vue";
import Admin from '../components/Admin.vue'
//import 自定义组件名 from 路径
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [

        {
            path: '/',
            redirect: '/manager'
        },
        {
            path: '/manager/cashier',
            component: Home,
        },
        {
            path: '/admin/foreign',
            component: Admin
        },
    ]
})

export default router