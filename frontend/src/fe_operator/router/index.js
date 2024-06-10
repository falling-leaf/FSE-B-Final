import { createRouter, createWebHistory} from 'vue-router'
import Operator from '../components/Operator.vue'
import Addcurrency from '../components/add_currency.vue'
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: '/FExchange_operator'
        },
        {
            path: '/FExchange_operator',
            component: Operator
        },
        {
            path: '/FExchange_operator/addcurrency',
            component: Addcurrency
        },

    ],
})

export default router