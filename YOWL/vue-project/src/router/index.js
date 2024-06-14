import { createRouter, createWebHistory } from 'vue-router'
import Yowl from '../views/YOWL.vue'
import Addpost from '../views/Addpost.vue'
import signin from '../views/signin.vue'
import signup from '../views/signup.vue'
import comments from '../components/ModalView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
        {
      path: '/',
      name: 'home',
      component: Yowl
    },

    {
      path: '/post',
      name: 'post',
      component: Addpost
    },

    {
      path: '/signin',
      name: 'signin',
      component: signin
    },

    {
      path: '/signup',
      name: 'signup',
      component: signup
    },

    {
      path: '/sport',
      name: 'sport',
      component: Yowl
    },

    {
      path: '/tech',
      name: 'tech',
      component: Yowl
    },

    {
      path: '/gaming',
      name: 'gaming',
      component: Yowl
    },

    {
      path: '/photography',
      name: 'photography',
      component: Yowl
    },
    
    {
      path: '/music',
      name: 'music',
      component: Yowl
    },
        
    {
      path: '/art',
      name: 'art',
      component: Yowl
    },
            
    {
      path: '/more',
      name: 'more',
      component: Yowl
    },

    {
      path: '/comments',
      name: 'comments',
      component: comments
    },
  ]
})

export default router
