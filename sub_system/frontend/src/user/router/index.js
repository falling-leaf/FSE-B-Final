import { createRouter, createWebHistory} from 'vue-router'
//import 自定义组件名 from 路径
import ApplyLoan from '@/user/components/Applyloan.vue'
import Withdrawal from '@/user/components/withdrawal.vue'
import Query from '@/user/components/query.vue'
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: '/user'
        },
        {
            path: '/user/loan',
            component: ApplyLoan
        },
        {
            path: '/user/withdrawal',
            component: Withdrawal
        },
        {
            path: '/user/query',
            component: Query,
        },
    ],
})

export default router