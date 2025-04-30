<!-- This App.vue file is the root component of my Vue app. It's the first component rendered after my app is mounted to <div id="app"> in index.html by main.ts -->
<template>
    <main class="container pt-4">
        <!-- Bootstrap classes: wraps content in a Bootstrap container with top padding. -->
        <div>
            <router-link
                class=""
                :to="{name: 'Landing Page'}"
            >
                Landing Page
            </router-link>
            |
            <router-link
                class=""
                :to="{name: 'Signup/Login Page'}"
            >
                Signup/Login Page
            </router-link>
        </div>
        <!-- the <router-link> is a Vue Router component that renderes as an <a> tag. -->
        <!-- :to="{name: 'Main Page'} uses named routes for navigation. -->
        <!-- When clicked, it updates the URL and changes the view without reloading the page. This is because the <RouterView> renders the MainPage.vue-->
        <RouterView class="flex-shrink-0 border rounded bg-warning p-4" />
        <!-- <RouterView> tag is the placeholder where the component for the current route will be rendered. -->
        <!-- In our case it is style with Bootstrap (border, rounded, bg-warning, p-4) -->
        <!-- It acts like a dynamic <div> that updates when the route changes. -->
    </main>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";

export default defineComponent({
    components: { RouterView },
});

</script>
<!-- Uses TypeScript (lang="ts") -->
<!-- Imports defineComponent from Vue (standard for defining components with TypeScipt). -->
<!-- Registers RouterView so it can be used in the template. -->

<style scoped>
</style>

<!-- Empty for now. Scoped means styles (when added) will only apply to this component, not globally. -->

<!-- index.html contains <div id="app"></div> and loads main.ts -->
<!-- main.ts creates the Vue app with App.vue as the root component. It is the first component loaded after main.ts mounts the app to index.html -->
<!-- This App.vue is the root layout and controller of routing. -->
<!-- Inside this App.vue file I defined navigation using <router-link>.; The selected route's component is displayed in <RouterView>. -->
<!-- Routes are defined in router/index.ts, using route names like 'Main Page' and 'Other Page'. -->
<!-- Routing logic depends on the route definition in the src/router/index.ts file -->