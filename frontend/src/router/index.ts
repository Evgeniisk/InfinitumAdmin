// index.html provides a mounting point with <div id="app"> and loads main.ts
// main.ts Creates the Vue app, adds Pinia and Vue Router, and mounts the app to #app in index.html
// App.vue is the root layout with <router-link> for navigation and <RouterView> to render routed components.
// router/index.ts (this file) declares which components to show for which URL paths and route names.

//imports the functions to create a router and the history mode
import { createRouter, createWebHistory } from 'vue-router'

//Defines route components, thats to export default create component in the script of each component I can import them like this:
import Dashboard from '../pages/Dashboard.vue';
import Jobs from '../pages/Jobs.vue';
import Clients from '../pages/Clients.vue';
import TemplatesNav from '../pages/TemplatesNavPage.vue';
import Client from '../pages/Client.vue';
import ClientPageNav from '../pages/ClientPageNav.vue';
import ClientsContracts from '../pages/ClientsContracts.vue';
import ClientsInvoices from '../pages/ClientsInvoices.vue';
import TemplatesCompany from '../pages/TemplatesCompany.vue';
import TemplatesIndividual from '../pages/TemplatesIndividual.vue';

//Sets the base URL depending on the environment (development or production)
// Vite exposes environment variables via import.meta.env
let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

//Creates the Vue Router instance
const router = createRouter({
    
    //history: createWebHistory(base),
    history: createWebHistory('/app/'), //This is for production

    //Route to component mappings
    routes: [
        {
            path: '/',             //URL path (e.g., http://localhost:5173/)
            name: 'DashboardPage',     //Named route used in <router-link>
            component: Dashboard    //The component shown when this path is in the url bar
        },
        {
            path: '/Jobs/',       //URL path (e.g., http://localhost:5173/Jobs/)
            name: 'JobsPage',    //Used in router-link to navigate
            component: Jobs   //THe component shown when this path is in the url bar
        },
        {
            path: '/Clients/',
            name: 'ClientsPage',
            component: Clients
        },
        {
            path: '/Templates',
            name: 'TemplatesPage',
            component: TemplatesNav,
            children: [
                {
                    path: '',
                    redirect: {name: 'TemplatesCompany'},
                },
                {
                    path: 'Company',
                    name: 'TemplatesCompany',
                    component: TemplatesCompany
                },
                {
                    path: 'Individual',
                    name: 'TemplatesIndividual',
                    component: TemplatesIndividual
                },
            ]
        },
        {
            path:'/Client',
            name: 'ClientPageNav',
            component: ClientPageNav,
            children: [
                {
                    path: '',
                    redirect: {name: 'ClientPage'}
                },
                {
                    path: 'info',
                    name: 'ClientPage',
                    component: Client,
                },
                {
                    path: 'contracts',
                    name: 'ClientsContracts',
                    component: ClientsContracts,
                },
                {
                    path: 'invoices',
                    name: 'ClientsInvoices',
                    component: ClientsInvoices,
                },
            ]
        },
    ]
})

// Exports the router so it can be imported in main.ts file
export default router