import { createApp } from 'vue'
// Imports the Vue 3 function to create a new application instance.
import App from './App.vue'
// imports the root Vue component (usually defined the layout and structure of your app)
import router from './router'
// imports the Vue Router instance (used to handle navigation between different pages/views)
import { createPinia } from 'pinia'
//imports the function to create a new Pinia store (state management library, similar to Vuex)
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
//Imports Bootstrap's CSS and JS for styling and interactive UI components
const pinia = createPinia()
// Initialises the Pinia store, so it can be used across my app.
const app = createApp(App)
// Creates a Vue application instance using the App component as the root.
app.use(router)
// Registers the router plugin with the app, enabling navigation (e.g., using <router-view>)
app.use(pinia)
// Registers Pinia for global state manegement
app.mount('#app')
// Mounts the Vue app to the <div id="app"></div> in my index.html
// This is where all the Vue components will be rendered

//main.ts created the Vue app, installs routing and state management, and then mounts everything into <div id="app"></div> using app.mount('#app').