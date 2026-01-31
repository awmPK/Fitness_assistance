import { createRouter, createWebHistory } from 'vue-router'
import ChatView from '@/views/ChatView.vue'
import ProfileView from '@/views/ProfileView.vue'

const routes = [
  {
    path: '/',
    name: 'Chat',
    component: ChatView,
    meta: {
      title: 'AI助手 - 智能对话'
    }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfileView,
    meta: {
      title: '个人中心'
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: {
      title: '登录'
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/RegisterView.vue'),
    meta: {
      title: '注册'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Navigation guards
router.beforeEach((to, from, next) => {
  // Set page title
  document.title = to.meta.title as string || 'Fitness AI'
  
  // Check authentication (simplified - in real app would check token)
  const publicPages = ['/login', '/register']
  const authRequired = !publicPages.includes(to.path)
  
  if (authRequired && !localStorage.getItem('token')) {
    next('/login')
  } else {
    next()
  }
})

export default router