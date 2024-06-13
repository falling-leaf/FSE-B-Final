import { createRouter, createWebHistory} from 'vue-router'
import Creditcard from "../components/credit_user.vue";
//import 自定义组件名 from 路径
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [

        {
            path: '/',
            redirect: '/credit_user'
        },
        {
            path: '/credit_user',
            component: Creditcard,
        }
    ]
})

export default router