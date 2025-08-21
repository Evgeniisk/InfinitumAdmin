<template>
<div>
    <ul class="nav nav-tabs nav-fill">
        <li class="nav-item">
            <router-link class="nav-link" :class="{ active: $route.name === 'ClientPage'}" :to="{name: 'ClientPage', query: {ClientType: client.ClientType, id: client.id}}">
                Client Info
            </router-link>
        </li>
        <li class="nav-item">
            <router-link class="nav-link" :class="{ active: $route.name === 'ClientsContracts'}" :to="{name: 'ClientsContracts', query: {ClientType: client.ClientType, id: client.id}}">
                Contracts
            </router-link>
        </li>
        <li class="nav-item">
            <router-link class="nav-link" :class="{ active: $route.name === 'ClientsInvoices'}" :to="{name: 'ClientsInvoices', query: {ClientType: client.ClientType, id: client.id}}">
                Invoices
            </router-link>
        </li>
    </ul>
</div>
<!--The v-slot and :is used to make sure view router renders the changing route by key properly-->
<RouterView v-slot="{ Component }" :key="`${$route.query.ClientType}-${$route.query.id}`" class="flex-shrink-0 border rounded bg-warning p-4" >
    <!--Listens for events emitted from the child component (refer to ClientContracts.vue page' "Create" and "HandleAddContractClick" methods) and when it receives the emits from the child, it emits those events to the parent component (refer to app.vue)-->
    <component :is="Component" @loading="$emit('loading', $event)" @check-docuSign-status="$emit('check-docuSign-status', $event)"/>
</RouterView>

</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";

const baseURL = import.meta.env.VITE_API_URL;

export default defineComponent({
    components: { RouterView },
    data() {
        return {
            client: {
                ClientType: '',
                id: 0,
            },
        };
    },
    //created() is Vue Options API hook function which executes the code inide before this component (page) is mounted to the DOM so it needs to be used to replace routing to so that another component can be mounted to the DOM when the user clicks to access this component (page)
    created() {
        //Assigns the ClientType url query to this.client.ClientType
        this.client.ClientType = this.$route.query.ClientType;
        //Assigns the id url query to this.client.id
        this.client.id = this.$route.query.id;
        //checks if the route name is ClientPageName (this components route name)
        if (this.$route.name === 'ClientPageNav') {
            //replaces the url to change it's name to ClientPage to route the user to ClientPage as soon as they access this component
            this.$router.replace({ name: 'ClientPage', query: this.$route.query})
        }
    },
    });
</script>

<style scoped>

</style>