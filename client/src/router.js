import Vue from 'vue';
import Router from 'vue-router';
import Ping from './components/Ping.vue';
import profile from './components/profile.vue';
import login from './components/login.vue';
import signup from './components/signup.vue';
import logout from './components/logout.vue';
Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
    {
      path: '/profile',
      name: 'profile',
      component: profile,
    },
    {
      path: '/login',
      name: 'login',
      component: login,
    },
    {
      path: '/logout',
      name: 'logout',
      component: logout,
    }, 
    {
      path: '/signup',
      name: 'signup',
      component: signup,
    }

  ],
});