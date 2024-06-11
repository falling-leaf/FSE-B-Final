import { createRouter, createWebHistory} from 'vue-router'
import Check from "@/loan_manager/components/IssueLoan.vue";
//import 自定义组件名 from 路径
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [

        {
            path: '/',
            redirect: '/loan_manager/issue'
        },
        {
            path: '/loan_manager/issue',
            component: Check,
        }
    ]
})

export default router