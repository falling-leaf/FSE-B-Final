import { createRouter, createWebHistory} from 'vue-router'
import Creditcard from "../components/creditcard.vue";
//import 自定义组件名 from 路径
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [

        {
            path: '/',
            redirect: '/user/creditcard'
        },
        {
            path: '/user/creditcard',
            component: Creditcard,
        }
    ]
})

export default router