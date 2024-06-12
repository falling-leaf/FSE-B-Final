import { createRouter, createWebHistory} from 'vue-router'
import User from '../components/User.vue'
import Currency from '../components/Currency.vue'
import Buy from '../components/Buy.vue'
import Sell from '../components/Sell.vue'
import History from '../components/History.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: '/FExchange/user'
        },
        {
            path: '/FExchange/user',
            component: User
        },
        {
            path: '/FExchange/user/currency',
            component: Currency
        },
        {
            path: '/FExchange/user/buy',
            component: Buy
        },
        {
            path: '/FExchange/user/sell',
            component: Sell
        },
        {
            path: '/FExchange/user/history',
            component: History
        },
    ],
})

export default router