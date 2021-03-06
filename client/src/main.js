import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue';
import VueApexCharts from 'vue-apexcharts';
import VeeValidate from 'vee-validate';
import Vue from 'vue';
import router from './router';
import store from './store';
import App from './App.vue';

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);
Vue.use(VueApexCharts);
Vue.use(VeeValidate);

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
