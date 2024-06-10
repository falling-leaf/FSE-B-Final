import { createRouter, createWebHistory} from 'vue-router'
import Check from "@/manager/components/IssueLoan.vue";
//import 自定义组件名 from 路径
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [

        {
            path: '/',
            redirect: '/manager/issue'
        },
        {
            path: '/manager/issue',
            component: Check,
        }
    ]
})

export default router