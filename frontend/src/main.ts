//main.ts creates the Vue app, installs routing and state management, and then mounts everything into <div id="app"></div> using app.mount('#app').

// Imports the Vue 3 function to create a new application instance.
import { createApp } from 'vue'
// imports the root Vue component
import App from './App.vue'
// imports the Vue Router instance (used to handle navigation between different pages/views)
import router from './router'
import Multiselect from 'vue-multiselect' //imports vue multiselect
import 'vue-multiselect/dist/vue-multiselect.css' //imports vue multiselect css package
//imports the function to create a new Pinia store (state management library)
import { createPinia } from 'pinia'
//Imports Bootstrap's CSS and JS for styling and interactive UI components
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
// Initialises the Pinia store, so it can be used across my app. (I didn't use it)
const pinia = createPinia()
// Creates a Vue application instance using the App component as the root.
const app = createApp(App)
// Registers the router plugin with the app, enabling navigation (e.g., using <router-view>)
app.use(router)
// Registers Pinia for global state manegement (I didn't use it)
app.use(pinia)
// Mounts the Vue app to the <div id="app"></div> in my index.html
// This is where all the Vue components will be rendered
app.component('Multiselect', Multiselect)
app.mount('#app')