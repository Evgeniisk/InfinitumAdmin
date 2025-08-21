<template>
<div>
    <ul class="nav nav-pills nav-fill mb-3">
        <li class="nav-item">
            <router-link id="CompanyTemplates" class="nav-link" :class="{ active: $route.name === 'TemplatesCompany'}" :to="{name: 'TemplatesCompany'}">
                Company
            </router-link>
        </li>
        <li class="nav-item">
            <router-link id="IndividualTemplates" class="nav-link" :class="{ active: $route.name === 'TemplatesIndividual'}" :to="{name: 'TemplatesIndividual'}">
                Individual
            </router-link>
        </li>
    </ul>
</div>

<RouterView class="flex-shrink-0 border rounded bg-warning p-4" />

</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";

const baseURL = import.meta.env.VITE_API_URL;

export default defineComponent({
    components: { RouterView },
    created() {
        //checks if the route name is TemplatesPage (this components route name)
        if (this.$route.name === 'TemplatesPage') {
            //replaces the url to change it's name to TemplatesCompany to route the user to TemplatesCompany as soon as they access this component
            this.$router.replace({ name: 'TemplatesCompany', params: this.$route.params, query: this.$route.query})
        }
    },
    });
</script>

<style scoped>

</style>