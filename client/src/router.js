import Vue from 'vue';
import Router from 'vue-router';
import Ping from './components/Ping.vue';
import Search from './components/Search.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/search',
      name: 'Search',
      component: Search
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping
    },
    {
      path: '/location/:placeid',
      name: 'Location',
      component: Location
    }
  ],
});