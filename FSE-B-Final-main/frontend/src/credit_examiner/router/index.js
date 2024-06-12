import { createRouter, createWebHistory} from 'vue-router'
//import 自定义组件名 from 路径
import Unchecked from '../components/unchecked.vue'
import Checked from '../components/checked.vue'
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: '/credit_examiner'
        },
        {
            path: '/credit_examiner/checked',
            component: Checked,
        },
        {
            path: '/credit_examiner/unchecked',
            component: Unchecked,
        },
    ],
})

export default router