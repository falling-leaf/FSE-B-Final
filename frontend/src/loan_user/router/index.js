import { createRouter, createWebHistory} from 'vue-router'
//import 自定义组件名 from 路径
import ApplyLoan from '@/loan_user/components/Applyloan.vue'
import Withdrawal from '@/loan_user/components/withdrawal.vue'
import Query from '@/loan_user/components/query.vue'
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: '/loan_user'
        },
        {
            path: '/loan_user/loan',
            component: ApplyLoan
        },
        {
            path: '/loan_user/withdrawal',
            component: Withdrawal
        },
        {
            path: '/loan_user/query',
            component: Query,
        },
    ],
})

export default router