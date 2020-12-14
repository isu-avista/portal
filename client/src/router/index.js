import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '@/views/Home.vue';
import Login from '@/views/Login.vue';
import Profile from '@/views/Profile.vue';
import isValidJwt from '@/utils';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue'),
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
];

const router = new VueRouter({
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
