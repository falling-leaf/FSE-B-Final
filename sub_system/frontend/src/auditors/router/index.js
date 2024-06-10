import { createRouter, createWebHistory} from 'vue-router'
import Check from "@/auditors/components/Check.vue";
//import 自定义组件名 from 路径
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [

        {
            path: '/',
            redirect: '/auditors/check'
        },
        {
            path: '/auditors/check',
            component: Check,
        }
    ]
})

export default router