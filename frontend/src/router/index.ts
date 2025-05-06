// Example of how to use Vue Router

import { createRouter, createWebHistory } from 'vue-router'
//import the function to create a router and the history mode

// 1. Define route components.
// These can be imported from other files
import LandingPage from '../pages/LandingPage.vue';
import SignupLoginPage from '../pages/LoginPage.vue';
import SecurityInfoPage from '../pages/SecurityInfoPage.vue';
//import the Vue components that will be shown in on different routes.

//Set the base URL depending on the environment (development or production)
// Vite exposes environment variables via import.meta.env
let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''
// In development, import.meta.env.BASE_URL is usually '/', so the app runs from the root.
// In production, setting base = '' ensures routes work correctly even if deployed in a subfolder or behind a proxy.

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.

//Creating the Vue Router instance
const router = createRouter({
    //Using HTML5 history mode (no hash in the URL) and se the base path.
    history: createWebHistory(base),

    //Definining route-to-component mappings
    routes: [
        {
            path: '/',             // URL path (e.g., http://localhost:5173/)
            name: 'Landing Page',     // Named route used in <router-link>
            component: LandingPage    // The component to render
        },
        {
            path: '/Login/',       // URL path (e.g., http://localhost:5173/other/)
            name: 'Login Page',    // Used in router-link to navigate
            component: SignupLoginPage   // Component shown when this path is active
        },
        {
            path: '/SecurityInfo/',
            name: 'Security Info Page',
            component: SecurityInfoPage
        },
    ]
})

// Export the router so it can be imported in main.ts
export default router

// index.html provides a mounting point with <div id="app"> and loads main.ts
// main.ts Creates the Vue app, adds Pinia and Vue Router, and mounts the app to #app in index.html
// App.vue Root layout with <router-link> for navigation and <RouterView> to render routed components.
// router/index.ts (this file) declares which components to show for which URL paths and route names.
