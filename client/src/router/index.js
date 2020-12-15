import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/views/Home.vue';
import About from '@/views/About.vue';
import Login from '@/views/Login.vue';
import Profile from '@/views/Profile.vue';
import Config from '@/views/Config.vue';
import Actions from '@/views/Actions.vue';
import Issues from '@/views/Issues.vue';
import Monitor from '@/views/Monitor.vue';
import isValidJwt from '@/utils';

Vue.use(Router);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/about',
    name: 'About',
    component: About,
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    // component: () => import(/* webpackChunkName: "about" */ '../views/About.vue'),
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
  },
  {
    path: '/monitor',
    name: 'Monitor',
    component: Monitor,
  },
  {
    path: '/config',
    name: 'Config',
    component: Config,
  },
  {
    path: '/issues',
    name: 'Issues',
    component: Issues,
  },
  {
    path: '/actions',
    name: 'Actions',
    component: Actions,
  },
];

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  const publicPages = ['/login', '/about'];
  const adminPages = ['/config'];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = localStorage.getItem('user');

  // trying to access a restricted page + not logged in
  // redirect to login page
  if (authRequired && !loggedIn) {
    next('/login');
  } else {
    const user = JSON.parse(localStorage.getItem('user'));
    if (user && user.token && !isValidJwt(user.token)) {
      next('/login');
    } else if (adminPages.includes(to.path) && user.role === 'ADMIN') {
      next();
    } else if (adminPages.includes(to.path) && user.role !== 'ADMIN') {
      next(from);
    } else {
      next();
    }
  }
});

export default router;
