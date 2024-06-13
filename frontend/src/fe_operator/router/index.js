import { createRouter, createWebHistory} from 'vue-router'
import Operator from '../components/Operator.vue'
import Addcurrency from '../components/add_currency.vue'
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: '/FExchange/operator'
        },
        {
            path: '/FExchange/operator',
            component: Operator
        },
        {
            path: '/FExchange/operator/addcurrency',
            component: Addcurrency
        },

    ],
})

export default router