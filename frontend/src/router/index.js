import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

// 頁面元件 (Lazy Loading)
const LoginView = () => import('../views/LoginView.vue')
const MainLayout = () => import('../layouts/MainLayout.vue')
const BoardListView = () => import('../views/BoardListView.vue')
const BoardDetailView = () => import('../views/BoardDetailView.vue')
const StatsView = () => import('../views/StatsView.vue')
const AdminDashboardView = () => import('../views/AdminDashboardView.vue')
const UserManagementView = () => import('../views/UserManagementView.vue')

const routes = [
    {
        path: '/login',
        name: 'Login',
        component: LoginView,
        meta: { requiresAuth: false }
    },
    {
        path: '/',
        component: MainLayout,
        meta: { requiresAuth: true },
        children: [
            {
                path: '',
                redirect: '/boards'
            },
            {
                path: 'boards',
                name: 'BoardList',
                component: BoardListView
            },
            {
                path: 'boards/:id',
                name: 'BoardDetail',
                component: BoardDetailView
            },
            {
                path: 'boards/:id/stats',
                name: 'BoardStats',
                component: StatsView
            },
            // Admin Only
            {
                path: 'admin/dashboard',
                name: 'AdminDashboard',
                component: AdminDashboardView,
                meta: { requiresAdmin: true }
            },
            {
                path: 'admin/users',
                name: 'UserManagement',
                component: UserManagementView,
                meta: { requiresAdmin: true }
            }
        ]
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// 路由守衛
router.beforeEach((to, from, next) => {
    // 需要在 Pinia 初始化後才能使用 store
    // 這裡使用延遲載入
    import('../stores/authStore').then(({ useAuthStore }) => {
        const authStore = useAuthStore()

        // 需要登入的頁面
        if (to.meta.requiresAuth && !authStore.isLoggedIn) {
            next('/login')
            return
        }

        // 已登入時不能進入登入頁
        if (to.path === '/login' && authStore.isLoggedIn) {
            next('/boards')
            return
        }

        // 需要 Admin 權限的頁面
        if (to.meta.requiresAdmin && !authStore.isAdmin) {
            next('/boards')
            return
        }

        next()
    })
})

export default router
