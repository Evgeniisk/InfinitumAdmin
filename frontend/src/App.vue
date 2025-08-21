<!-- This App.vue file is the root component of my Vue app. It's the first component rendered after my app is mounted to <div id="app"> in index.html by main.ts -->
<template>
    <main class="container-fluid pt-4 d-flex flex-column min-vh-100">
        <!-- Bootstrap classes: wraps content in a Bootstrap container with top padding. -->
        <div class="position-relative">
            <nav class="navbar navbar-expand-lg navbar-light px-3">
                <div class="container-fluid d-flex justify-content-between align-items-center">
                    <router-link
                        class="navbar-brand"
                        :to="{name: 'DashboardPage'}"
                    >
                        <img src="/src/assets/Project_logo.svg" width="100" height="100" alt="">
                    </router-link>
                    <p class="mb-0 d-flex align-items-center">{{ workplace }}</p>
                    <div class="d-flex flex-grow-1 justify-content-center align-items-center">
                        <button class="navbar-toggler" type="button" @click="toggleNavbar()" aria-label="Toggle navigation">
                            <span class="navbar-toggler-icon"></span>
                        </button>
                    </div>

                    <div class="collapse navbar-collapse justify-content-center mt-2" id="navbarSupportedContent" ref="navbarCollapse">
                        <ul class="navbar-nav me-auto">
                            <li class="nav-item">
                                <router-link id="Clients" class="nav-link" :to="{name: 'ClientsPage'}" @click="collapseNavbar()">
                                    Clients
                                </router-link>
                            </li>
                            <li class="nav-item">
                                <router-link id="Jobs" class="nav-link" :to="{name: 'JobsPage'}" @click="collapseNavbar()">
                                    My Jobs
                                </router-link>
                            </li>
                            <li class="nav-item">
                                <router-link id="Templates" class="nav-link" :to="{name: 'TemplatesCompany'}" @click="collapseNavbar()">
                                    Templates
                                </router-link>
                            </li>
                        </ul>
                    </div>

                    <div class="d-flex align-items-center gap-2" style="top: 0; bottom: 0; margin: auto; height: 40px;">
                        <button id="SettingsButton" type="button" class="btn btn-primary d-flex align-items-center gap-1" data-bs-toggle="offcanvas" data-bs-target="#offcanvasTop" aria-controls="offcanvasTop">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-gear" viewBox="0 0 16 16">
                                <path d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492M5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0"/>
                                <path d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.291-.16c.764-.415 1.6.42 1.184 1.185l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.319.094a1.873 1.873 0 0 0-1.115 2.693l.16.291c.415.764-.42 1.6-1.185 1.184l-.291-.159a1.873 1.873 0 0 0-2.693 1.116l-.094.318c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.692-1.115l-.292.16c-.764.415-1.6-.42-1.184-1.185l.159-.291A1.873 1.873 0 0 0 1.945 8.93l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094A1.873 1.873 0 0 0 3.06 4.377l-.16-.292c-.415-.764.42-1.6 1.185-1.184l.292.159a1.873 1.873 0 0 0 2.692-1.115z"/>
                            </svg> Settings
                        </button>
                        <button id="LogoutButton" type="button" class="btn btn-light ms-2" data-bs-toggle="modal" data-bs-target="#LogOutModal">
                            Log out <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-box-arrow-right" viewBox="0 0 16 16">
                                <path fill-rule="evenodd" d="M10 12.5a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v2a.5.5 0 0 0 1 0v-2A1.5 1.5 0 0 0 9.5 2h-8A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h8a1.5 1.5 0 0 0 1.5-1.5v-2a.5.5 0 0 0-1 0z"/>
                                <path fill-rule="evenodd" d="M15.854 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L14.293 7.5H5.5a.5.5 0 0 0 0 1h8.793l-2.147 2.146a.5.5 0 0 0 .708.708z"/>
                            </svg>
                        </button>
                    </div>

                </div>
            </nav>
        </div>
        <!-- the <router-link> is a Vue Router component that renderes as an <a> tag. -->
        <!-- :to="{name: 'Main Page'} uses named routes for navigation. -->
        <!-- When clicked, it updates the URL and changes the view without reloading the page. This is because the <RouterView> renders the MainPage.vue-->
        <RouterView v-slot="{ Component }" class="flex-shrink-0 border rounded bg-warning p-4" >
            <!--Recives emitted events from child components and passes replies to those events (Refer to ClientPageNav.vue page)-->
            <component :is="Component" @loading="handleLoading" @check-docuSign-status="handleCheckDocuSign"/>
        </RouterView>
        <!-- <RouterView> tag is the placeholder where the component for the current route will be rendered. -->
        <!-- In our case it is style with Bootstrap (border, rounded, bg-warning, p-4) -->
        <!-- It acts like a dynamic <div> that updates when the route changes. -->
        <div v-if="isLoading" class="loading-overlay">
            <div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    </main>
    <footer class="bg-light text-center text-muted py-3 mt-3">
        &#169; 2025 InfinitumAdmin. All rights reserved.
    </footer>
    <!-- Log Out confirmation modal -->
    <div class="modal fade" id="LogOutModal" tabindex="-1" aria-labelledby="LogOutModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="LogOutModalLabel">Log Out</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-12">
                        <label for="Confirmation Message" class="form-label">Are you sure you want to log out?</label>
                        <label for="Session and Cookies disclamer" class="form-label">It will destroy all the sessions and cookies and you will need to log in again to access your account.</label>
                        <div class="d-flex justify-content-center align-items-center gap-3 mt-3">
                            <button id="LogOutConfirm" type="button" class="btn btn-success" @click="logout" data-bs-dismiss="modal">Yes, log me out</button>
                            <button type="button" class="btn btn-danger" data-bs-dismiss="modal">No, keep me logged in</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!--Settings canvas-->
    <div class="offcanvas offcanvas-top custom-offcanvas-height offcanvas-dialog offcanvas-dialog-scrollable" data-bs-backdrop="static" tabindex="-1" id="offcanvasTop" aria-labelledby="offcanvasTopLabel">
        <div class="offcanvas-header">
            <h5 class="offcanvas-title" id="offcanvasTopLabel">Settings</h5>
            <button type="button" id="closecanvasbutton" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
            <ul class="nav nav-pills" id="pills-tab" role="tablist">
                <li class="nav-item" role="presentation">
                    <button class="nav-link active" id="pills-AccessControl-tab" data-bs-toggle="pill" data-bs-target="#pills-AccessControl" type="button" role="tab" aria-controls="pills-AccessControl" aria-selected="false">Access Control</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="pills-IntegrationsAPIs-tab" data-bs-toggle="pill" data-bs-target="#pills-IntegrationsAPIs" type="button" role="tab" aria-controls="pills-IntegrationsAPIs" aria-selected="false">Integrations & APIs</button>
                </li>
            </ul>
            <div class="tab-content" id="pills-tabContent">
                <!--STRIPE TESTING TESTING TESTING-->
                <div class="tab-pane fade show active" id="pills-AccessControl" role="tabpanel" aria-labelledby="pills-AccessControl-tab" tabindex="0">
                    <button id="InviteUser" class="btn btn-sm btn-success mb-3" data-bs-toggle="modal" data-bs-target="#InviteUserModal">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-plus" viewBox="0 0 16 16">
                            <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
                        </svg> Invite User
                    </button>
                    <table class="table">
                        <thead>
                            <tr>
                                <th scope="col">#</th>
                                <th scope="col">Name</th>
                                <th scope="col">Email</th>
                                <th scope="col">Position</th>
                                <th scope="col">Admin</th>
                                <th scope="col">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="User in AllUsers" :key="User.id" :class="{'table-danger': User.status == 'invited', 'table-success': User.status === 'active', 'table-primary': User.status === 'inactive', 'clickable-row': User.status === 'active'}">
                                <td>
                                    <span>{{ User.id }}</span>
                                </td>
                                <td>
                                    <span>{{ User.Fname }} {{ User.Lname }}</span>
                                </td>
                                <td>
                                    <span>{{ User.email }}</span>
                                </td>
                                <td>
                                    <span>{{ User.position }}</span>
                                </td>
                                <td>
                                    <span v-if="User.Company_Admin === false">
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" value="" id="checkDisabled" disabled>
                                            <label class="form-check-label" for="checkDisabled">
                                                Company Admin
                                            </label>
                                        </div>
                                    </span>
                                    <span v-else>
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" value="" id="checkCheckedDisabled" checked disabled>
                                            <label class="form-check-label" for="checkCheckDisabled">
                                                Company Admin
                                            </label>
                                        </div>
                                    </span>
                                </td>
                                <td>
                                    <div v-if="!User.superuser">
                                        <button @click="user.id = User.id; user.status = User.status" class="btn btn-sm btn-danger" data-bs-toggle="modal" data-bs-target="#ConfirmationModal">
                                            <img src="/src/assets/person-x.svg" width="20" height="20" alt="">
                                        </button>
                                    </div>
                                    <div v-else>
                                        <button class="btn btn-sm btn-danger" disabled>
                                            <img src="/src/assets/person-x.svg" width="20" height="20" alt="">
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="tab-pane fade" id="pills-IntegrationsAPIs" role="tabpanel" aria-labelledby="pills-IntegrationsAPIs-tab" tabindex="0">
                    <h2 class="mb-4">Digital Signature Platforms:</h2>
                    <img src="/src/assets/DocuSign_Logo_0.svg" width="200" height="50" alt="">
                    <label class="form-check form-switch fs-4 d-flex align-items-center">
                        <input class="form-check-input me-2" type="checkbox" role="switch" id="docuSignSwitch" v-model="DocuSign.connected" @change="handleDocuSignToggle" style="width: 1.8em; height: 0.8em;">
                        <span class="form-check-label" for="docuSignSwitch">
                            {{ DocuSign.connected ? 'Connected to DocuSign' : 'Not Connected' }}
                        </span>
                    </label>
                </div>
            </div>
        </div>
    </div>


    <!--Confirmation Modal-->
    <div class="modal fade" id="ConfirmationModal" tabindex="-1" aria-labelledby="ConfirmationModal" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="InviteUserModalLabel">Are you sure you want to delete this user?</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p>If you delete this user they will loose access to the shared company account and database.</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-danger" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="Delete_User()">Delete User</button>
                </div>
            </div>
        </div>
    </div>


    <!--Invite User Modal-->
    <div class="modal fade" id="InviteUserModal" tabindex="-1" aria-labelledby="InviteUserModal" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="InviteUserModalLabel">Invite a user to join you on this platform</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="row g-3">
                        <div class="col-6">
                            <label for="Fname" class="form-label">First Name</label>
                            <input v-model="Invited_user.Fname" type="text" class="form-control" id="InputFname" aria-describedby="FnameHelp">
                        </div>
                        <div class="col-6">
                            <label for="Lname" class="form-label">Last Name</label>
                            <input v-model="Invited_user.Lname" type="text" class="form-control" id="InputLname" aria-describedby="LnameHelp">
                        </div>
                        <div class="col-12">
                            <label for="Email" class="form-label">Email</label>
                            <input v-model="Invited_user.email" type="email" class="form-control" id="InputEmail" aria-describedby="EmailHelp" required>
                        </div>
                        <div class="col-12">
                            <label for="Position" class="form-label">Position</label>
                            <input v-model="Invited_user.position" type="text" class="form-control" id="InputPosition" aria-describedby="PositionHelp">
                        </div>
                        <div class="col-12">
                            <div class="form-check">
                                <input v-model="Invited_user.Company_Admin" class="form-check-input" type="checkbox" id="checkDefault" checked disabled>
                                <label class="form-check-label" for="checkDefault">
                                    Company Admin
                                </label>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-danger" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" id="submitbutton" class="btn btn-success" data-bs-dismiss="modal" @click="Invite_User()">Invite User</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";
import * as bootstrap from 'bootstrap';
import {CookieHandle} from '@/utils.js';

const baseURL = import.meta.env.VITE_API_URL;

export default defineComponent({
    components: { RouterView },
    data(){
        return {
            Invited_Users: [],
            Active_Users: [],
            Inactive_Users: [],
            Invited_user: {
                Fname: '',
                Lname: '',
                email: '',
                position: '',
                Company_Admin: true,
            },
            user: {
                id: '',
                status: '',
            },
            DocuSign: {
                connected: false,
            },
            isLoading: false,
            workplace: "",
        }
    },
    async mounted() {
        const csrftoken = CookieHandle('csrftoken');
        const response3 = await fetch(`${baseURL}/api/workplace/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            credentials: 'include'
        });
        const data3 = await response3.json();
        this.workplace = data3.name;

        const response = await fetch(`${baseURL}/api/Users/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            credentials: 'include'
        });
        const data = await response.json();
        this.Invited_Users = data.Invited_Users;
        this.Inactive_Users = data.Inactive_Users;
        this.Active_Users = data.Active_Users;

        const response2 = await fetch(`${baseURL}/api/token_confirmation/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            credentials: 'include'
        });
        const data2 = await response2.json();
        this.DocuSign = data2;
    },
    computed: {
        AllUsers() {
            const invited = this.Invited_Users.map(user => ({
                ...user,
                status: 'invited',
            }));
            const active = this.Active_Users.map(user => ({
                ...user,
                status: 'active',
            }));
            const inactive = this.Inactive_Users.map(user => ({
                ...user,
                status: 'inactive',
            }));
            return [...invited, ...active, ...inactive];
        },
    },
    methods: {
        async logout() {
            const csrftoken = CookieHandle('csrftoken');
            const response = await fetch(`${baseURL}/api/logout/`, {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
                },
                credentials: 'include'
            });

            if (response.ok) {
                const data = await response.json();
                if (data.success === true) {
                    window.location.replace(`${baseURL}/LoginPage/`)
                } else {
                    console.error('Logout Failed');
                }
            }
        },
        async Invite_User() {
            const csrftoken = CookieHandle('csrftoken');
            const response = await fetch(`${baseURL}/api/invite_user`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(this.Invited_user),
                credentials: "include"
            });
            const data = await response.json();
            this.Invited_user = data;
            this.Invited_Users.push(this.Invited_user)
        },
        async Delete_User() {
            const csrftoken = CookieHandle('csrftoken');
            const response = await fetch(`${baseURL}/api/Users/`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(this.user),
                credentials: 'include',
            });
            const data = await response.json();
            if (this.user.status == 'invited'){
                //Loops through the indexes and values of the Invited_Users array
                for (const [index, invited_user] of this.Invited_Users.entries()){
                    if (invited_user.id === this.user.id){
                        //Removes the the user from the invited users array by finding it's index and removing one user starting from the index
                        this.Invited_Users.splice(index, 1);
                        break;
                    }
                }
            } else {
                //Loops through the indexes and values of the Invited_Users array
                for(const [index, inactive_user] of this.Inactive_Users.entries()){
                    if (inactive_user.id == this.user.id){
                        //Removes the the user from the invited users array by finding it's index and removing one user starting from the index
                        this.Inactive_Users.splice(index, 1);
                        break;
                    }
                }
                //Loops through the indexes and values of the Invited_Users array
                for (const [index, active_user] of this.Active_Users.entries()) {
                    if (active_user.id == this.user.id){
                        //Removes the the user from the invited users array by finding it's index and removing one user starting from the index
                        this.Active_Users.splice(index, 1);
                        break;
                    }
                }
            }
            
        },
        handleDocuSignToggle() {
            if (this.DocuSign.connected) {
                this.connectToDocuSign();
            } else {
                this.disconnectFromDocuSign();
            }
        },
        connectToDocuSign() {
            const clientId = '52b550e2-fb88-4a19-953c-b3abf8dc52db'; //This is ok to be open to the public according to DocuSign
            //Redirect uri to be provided to DocuSign must be url encoded according to docusign
            const redirectUri = encodeURIComponent('http://localhost:8000/api/docusign/callback/');
            //DocuSign response type the code tells DocuSign to use authorisation code grant flow
            const responseType = 'code';
            //The permission I need to request to use this account
            const scope = 'signature';
            //DocuSign Rest API url with relevant query params
            const authUrl = `https://account-d.docusign.com/oauth/auth?response_type=${responseType}&scope=${scope}&client_id=${clientId}&redirect_uri=${redirectUri}`;
            //Redirects the user to the url above
            window.location.href = authUrl;
        },
        async disconnectFromDocuSign() {
            const csrftoken = CookieHandle('csrftoken');
            const response = await fetch(`${baseURL}/api/docusign/disconnect/`, {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    'X-CSRFToken': csrftoken
                },
                credentials: 'include'
            });
            if (response.ok) {
                this.DocuSign.connected = false;
            } else {
                console.error('Failed to disconnect from DocuSign');
            }
        },
        handleLoading(value) {
            console.log('Received loading event with:', value) //used for debugging
            this.isLoading = value;
        },
        handleCheckDocuSign(callback) {
            const status = this.DocuSign.connected;
            //Checks if a function emitted this event 
            if (typeof callback === 'function') {
                //If it is, calls that function which emitted this event and passes it the status variable
                callback(status);
            }
        },
        collapseNavbar() {
            //Gets the navbar element
            const el = this.$refs.navbarCollapse;
            //If the navbar exists and is currently expanded
            if (el && el.classList.contains('show')) {
                //checks if there is an existing boostrap Collapse instance and if there is collapses the navbar
                bootstrap.Collapse.getInstance(el)?.hide();
            }
        },
        toggleNavbar() {
            //Gets the navbar element
            const el = this.$refs.navbarCollapse;
            //If the navbar is currently expanded
            if (el.classList.contains('show')) {
                //checks if there is an existing bootstrap Collapse instance and if there is collapses the navbar
                bootstrap.Collapse.getInstance(el)?.hide();
            } else {
                //If the navbar isnt currently expanded this creates a new bootrap collapse instance for the navbar to be able to close it after expansion
                new bootstrap.Collapse(el);
            }
        }
    },
});


</script>
<!-- Uses TypeScript (lang="ts") -->
<!-- Imports defineComponent from Vue (standard for defining components with TypeScipt). -->
<!-- Registers RouterView so it can be used in the template. -->

<style>
nav{
    background-color: rgb(255, 255, 255);
}
.navbar {
            padding-top: 0.01rem;
            padding-bottom: 0.01rem;
        }
.navbar .navbar-brand {
            padding: 0;
            margin: 0;
        }
.navbar .navbar-brand img {
            height: 100px;
            width: auto;
        }

.offcanvas-top.custom-offcanvas-height {
    height: 50vh !important;
    max-height: 50vh !important;
    overflow: hidden;
}

.offcanvas-header {
    position: sticky;
    top: 0;
    z-index: 1;
    background-color: white;
}

.offcanvas-body {
    display: flex;
    flex-direction: column;
    height: 100%;
    padding: 0;
}

.offcanvas-body .d-flex.align-items-start{
    flex: 1;
    overflow: hidden;
    display: flex;
    width: 100%;
}

.offcanvas-body > .nav {
    justify-content: center;
    display: flex;
    margin-top: 1rem;
    flex-wrap: wrap;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(255, 255, 255, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}
footer {
    width: 100vw;
}


</style>

<!-- Empty for now. Scoped means styles (when added) will only apply to this component, not globally. -->

<!-- index.html contains <div id="app"></div> and loads main.ts -->
<!-- main.ts creates the Vue app with App.vue as the root component. It is the first component loaded after main.ts mounts the app to index.html -->
<!-- This App.vue is the root layout and controller of routing. -->
<!-- Inside this App.vue file I defined navigation using <router-link>.; The selected route's component is displayed in <RouterView>. -->
<!-- Routes are defined in router/index.ts, using route names like 'Main Page' and 'Other Page'. -->
<!-- Routing logic depends on the route definition in the src/router/index.ts file -->