import { createRouter, createWebHistory} from 'vue-router'
import creditcard from '../components/creditcard.vue'
import Admin from '../components/Admin.vue'
import home from "../components/home.vue"
import LoanManager from "../components/LoanManager.vue"
import Auditors from "../components/Auditors.vue"

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
            component: home,
        },
        {
            path: '/admin/foreign',
            component: Admin
        },
        {
            path: '/manager/loanManager',
            component: LoanManager
        },
        {
            path: '/manager/auditors',
            component: Auditors
        },
        {
            path:'/manager/credit',
            component: creditcard,
        }
    ]
})

export default router