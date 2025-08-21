<template>
    <div class="container py-1">
        <div class="card shadow rounded-4 p-4">
            <h1>Welcome to Infinitum Admin.</h1>
            <p>You are logged in to the administrative dashboard of InfinitumAdmin - your application for managing users, clients, invoices, contracts, templates and system configurations.</p>

            <hr class="my-4"/>

            <h5 class="mb-3">From here, you can:</h5>
            <ul>
                <li>
                    <router-link :to="{name: 'ClientsPage'}">
                        Manage your clients
                    </router-link>
                </li>
                <li>
                    <router-link :to="{name: 'JobsPage'}">
                        Manage your jobs
                    </router-link>
                </li>
                <li>
                    <router-link :to="{name: 'TemplatesCompany'}">
                        Manage your templates
                    </router-link>
                </li>
            </ul>

            <h5 class="mb-3">Key Information</h5>
            <ul class="ps-3">
                <li class="mb-2">Click the <strong>Settings</strong> button in the top-right corner to invite and manage users with access to your account.</li>
                <li class="mb-2">Connect your <strong>DocuSign</strong> account via Settings to sign and send contracts.</li>
                <li class="mb-2">Upload <strong>contract, invoice, and email templates</strong> to automate communications with clients.</li>
                <li class="mb-2">Add and manage client details, create and track contracts and invoices.</li>
                <li class="mb-2">Assign jobs from invoice/contract items to yourself or coworkers.</li>
                <li class="mb-2">Track assigned jobs and their deadlines in the <strong>My Jobs</strong> page with start and finish dates.</li>
                <li class="mb-2">InfinitumAdmin helps automate admin workflows and personalize the experience for your clients.</li>
            </ul>

            <p class="mt-4 fw-semibold">Start exploring the features to discover how InfinitumAdmin can support your business.</p>
        </div>
    </div>

<!--DocuSignAuthenticationStatusModal-->
<div class="modal fade" id="statusModal" tabindex="-1" aria-labelledby="statusModalLabel" aria-hidden="true" ref="modalRef">
    <div class="modal-dialog">
        <div class="modal-content">
            <div :class="['modal-header', modalSuccess ? 'bg-success' : 'bg-danger']">
                <h5 class="modal-title text-white" id="statusModalLabel">
                    {{ modalSuccess ? 'Connection Successful' : 'Connection Failed' }}
                </h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                {{ modalSuccess ? 'Your Docusign account has been connected successfully.' : 'There was a problem connecting your DocuSign account.' }}
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            </div>
        </div>
    </div>
</div>
</template>

<script lang="ts">

import { defineComponent, ref } from "vue";
import { useRoute } from 'vue-router';
import { Modal } from 'bootstrap';

const baseUrl = `${import.meta.env.VITE_API_URL}/main`;

export default defineComponent({
    data() {
        return {
            modalSuccess: false,
        }
    },
    async mounted() {
        //Gets the success parameter in the query
        const successParam = this.$route.query.success
        //Gets the references to the modal
        const modalElement = this.$refs.modalRef

        if (successParam === 'true' || successParam === 'false') {
            //Sets the modal Success component to true if the success Param is true
            //Otherwise keeps it default (false)
            this.modalSuccess = successParam == 'true'
            //Delays the modal display by 2 seconds
            setTimeout(() => {
                //Initialises the bootstrap modal
                const modal = new Modal(modalElement)
                modal.show()
                //Removes the the query parameters from the url
                this.$router.replace({
                    path: this.$route.path,
                    query: {}
                })
            }, 200);
        }
    },
})

</script>

<style scoped>

</style>