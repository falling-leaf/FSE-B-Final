import { createRouter, createWebHistory} from 'vue-router'
import LoanManager from "../components/LoanManager.vue"
import Auditors from "../components/Auditors.vue"

//import 自定义组件名 from 路径
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [

        {
            path: '/manager/loanManager',
            component: LoanManager
        },
        {
            path: '/manager/auditors',
            component: Auditors
        }
    ]
})

export default router