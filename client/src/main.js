import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import * as VueGoogleMaps from 'vue2-google-maps'
import { GOOGLE_MAPS_API_KEY } from './creds';

Vue.config.productionTip = false

Vue.use(VueGoogleMaps, {
  load: {
    key: GOOGLE_MAPS_API_KEY,
    libraries: "places"
  },
  installComponents: true,
});

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')