<template>
<div class="d-flex justify-content-between align-items-center mb-2">
        <div>
            <p class="text-muted mb-0">View and track your jobs and their progress.</p>
        </div>
    </div>
<table class="table">
    <thead>
        <tr>
            <th>#</th>
            <th>Client</th>
            <th>Job Name</th>
            <th>Value</th>
            <th>Created</th>
            <th>Started</th>
            <th>Completed</th>
            <th>Deadline</th>
            <th></th>
            <th v-if="hasStartedColumn"></th>
        </tr>
    </thead>
    <tbody>
        <template v-if="loading">
            <tr v-for="n in 20" :key="n" class="placeholder-glow">
                <td><span class="placeholder col-12"></span></td>
                <td><span class="placeholder col-12"></span></td>
                <td><span class="placeholder col-12"></span></td>
                <td><span class="placeholder col-12"></span></td>
                <td><span class="placeholder col-12"></span></td>
                <td><span class="placeholder col-12"></span></td>
                <td><span class="placeholder col-12"></span></td>
                <td><span class="placeholder col-12"></span></td>
                <td><span class="placeholder col-12"></span></td>
            </tr>
        </template>
        <template v-else-if="jobs.length === 0">
            <tr>
                <td colspan="9" class="text-muted p-0">
                    <div class="d-flex flex-column justify-content-center align-items-center" style="height: 100%; min-height: 300px;">
                        <i class="bi bi-box-seam fs-1 mb-2"></i><br>
                        <strong>You don't have any jobs yet.</strong>
                        <p class="mb-0">This table gets populated with assignments from newly created contracts or invoices.</p>
                    </div>
                </td>
            </tr>
        </template>
        <template v-else>
            <tr v-for="Job in jobs" :key="Job.id">
                <td>
                    <span>{{ Job.id }}</span>
                </td>
                <td>
                    <router-link v-if="Job.ContractItem?.contract.client_company" :to="{ name: 'ClientPageNav', query: { id: Job.ContractItem.contract.client_company.id, ClientType: Job.ContractItem.contract.client_company.ClientType}}" style="cursor: pointer;">
                        <span v-if="Job.ContractItem?.contract.client_company.CompanyName">{{ Job.ContractItem.contract.client_company.CompanyName }}</span>
                    </router-link>
                    <router-link v-else-if="Job.ContractItem?.contract.client_individual" :to="{ name: 'ClientPageNav', query: { id: Job.ContractItem.contract.client_individual.id, ClientType: Job.ContractItem.contract.client_individual.ClientType}}" style="cursor: pointer;">
                        <span v-if="Job.ContractItem?.contract.client_individual">{{ Job.ContractItem.contract.client_individual.Fname }} {{ Job.ContractItem.contract.client_individual.Lname }}</span>
                    </router-link>
                    <router-link v-else-if="Job.InvoiceItem?.invoice_summary.billed_to_individual" :to="{ name: 'ClientPageNav', query: { id: Job.InvoiceItem.invoice_summary.billed_to_individual.id, ClientType: Job.InvoiceItem.invoice_summary.billed_to_individual.ClientType}}" style="cursor: pointer;">
                        <span v-if="Job.InvoiceItem?.invoice_summary.billed_to_individual">{{ Job.InvoiceItem.invoice_summary.billed_to_individual.Fname }} {{ Job.InvoiceItem.invoice_summary.billed_to_individual.Lname }}</span>
                    </router-link>
                    <router-link v-else-if="Job.InvoiceItem?.invoice_summary.billed_to_company" :to="{ name: 'ClientPageNav', query: { id: Job.InvoiceItem?.invoice_summary.billed_to_company.id, ClientType: Job.InvoiceItem?.invoice_summary.billed_to_company.ClientType}}" style="cursor: pointer;">
                        <span v-if="Job.InvoiceItem?.invoice_summary.billed_to_company">{{ Job.InvoiceItem.invoice_summary.billed_to_company.CompanyName }}</span>
                    </router-link>
                    <span v-else></span>
                </td>
                <td>
                    <span v-if="Job.InvoiceItem">{{ Job.InvoiceItem.Name }}</span>
                    <span v-else-if="Job.ContractItem">{{ Job.ContractItem.ItemName }}</span>
                </td>
                <td>
                    <span v-if="Job.InvoiceItem">{{ Job.InvoiceItem.Price }}</span>
                    <span v-else-if="Job.ContractItem">{{ Job.ContractItem.Price }}</span>
                </td>
                <td>
                    <span>{{ Job.created_at }}</span>
                </td>
                <td>
                    <span v-if="!Job.started_at">Not Started</span>
                    <span v-else>{{ Job.started_at }}</span>
                </td>
                <td>
                    <span v-if="!Job.completed_at">Not Completed</span>
                    <span v-else>{{ Job.completed_at }}</span>
                </td>
                <td>
                    <span>{{ Job.Deadline }}</span>
                </td>
                <td>
                    <button v-if="!Job.started_at" class="btn btn-sm btn-primary" @click="StartJob(Job.id)">
                        Start
                    </button>
                    <button v-else-if="Job.started_at && !Job.completed_at" class="btn btn-sm btn-success" @click="FinishJob(Job.id)">
                        Finished
                    </button>
                    <button v-else-if="Job.started_at && Job.completed_at" class="btn btn-sm btn-danger" data-bs-toggle="modal" data-bs-target="#didntfinishmodal" @click="Selected_Job = Job.id">
                        Didn't finish
                    </button>
                </td>
                <td v-if="Job.started_at">
                    <button v-if="Job.started_at && !Job.completed_at" class="btn btn-sm btn-danger" data-bs-toggle="modal" data-bs-target="#didntstartmodal" @click="Selected_Job = Job.id">
                        Didn't start
                    </button>
                </td>
            </tr>
        </template>
    </tbody>
</table>

<!--modal for didn't start-->
<div class="modal fade" id="didntstartmodal" tabindex="-1" aria-labelledby="didntstartmodal" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Are you sure you didn't start the job?</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <p>If you save changes, the previous timestamp of job start will be deleted forever.</p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary" @click="reverseJobStart(Selected_Job)" data-bs-dismiss="modal">Save changes</button>
            </div>
        </div>
    </div>
</div>

<!--modal for haven't finished-->
<div class="modal fade" id="didntfinishmodal" tabindex="-1" aria-labelledby="didntfinishmodal" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Are you sure you didn't finish the job?</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <p>If you save changes, the previous timestamp of job finish will be deleted forever.</p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary" @click="reverseJobFinish(Selected_Job)" data-bs-dismiss="modal">Save changes</button>
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

const baseUrl = `${import.meta.env.VITE_API_URL}/main`;

export default defineComponent({
    components: { RouterView },
    data() {
        return {
            title: 'List of Jobs',
            jobs: [],
            Selected_Job: null,
            loading: true,
        };
    },
    async mounted() {
        const csrftoken = CookieHandle('csrftoken');
        const response = await fetch(`${baseUrl}/api/jobs/`, {
            method: 'GET',
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            credentials: 'include'
        })
        const data = await response.json()
        this.jobs = data.Jobs;
        this.loading = false;
    },
    methods: {
        async StartJob(Job_id){
            const csrftoken = CookieHandle('csrftoken');
            //Finds a job entry in the jobs array based on the passed Job_id and stores it in the job variable
            const job = this.jobs.find(job => job.id === Job_id)
            const response = await fetch(`${baseUrl}/api/jobs/`, {
                method: 'PUT',
                headers: {
                    "Content-Type": "application/json",
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({Job: job, Started: true, Finished: false}),
                credentials: 'include'
            })
            const data = await response.json()
            job.started_at = data.started_at;
        },
        async reverseJobStart(Job_id){
            const csrftoken = CookieHandle('csrftoken');
            //Finds a job entry in the jobs array based on the passed Job_id and stores it in the job variable
            const job = this.jobs.find(job => job.id === Job_id)
            const response = await fetch(`${baseUrl}/api/jobs/`, {
                method: 'PUT',
                headers: {
                    "Content-Type": "application/json",
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({Job: job, Started: false, Finished: false}),
                credentials: 'include'
            })
            const data = await response.json()
            job.started_at = data.started_at;
        },
        async FinishJob(Job_id){
            const csrftoken = CookieHandle('csrftoken');
            //Finds a job entry in the jobs array based on the passed Job_id and stores it in the job variable
            const job = this.jobs.find(job => job.id === Job_id)
            const response = await fetch(`${baseUrl}/api/jobs/`, {
                method: 'PUT',
                headers: {
                    "Content-Type": "application/json",
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({Job: job, Started: true, Finished: true}),
                credentials: 'include'
            })
            const data = await response.json()
            job.completed_at = data.completed_at;
        },
        async reverseJobFinish(Job_id){
            const csrftoken = CookieHandle('csrftoken');
            //Finds a job entry in the jobs array based on the passed Job_id and stores it in the job variable
            const job = this.jobs.find(job => job.id === Job_id)
            const response = await fetch(`${baseUrl}/api/jobs/`, {
                method: 'PUT',
                headers: {
                    "Content-Type": "application/json",
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({Job: job, Started: true, Finished: false}),
                credentials: 'include'
            })
            const data = await response.json()
            job.completed_at = data.completed_at;
        },
    },
    computed: {
        //Checks if any job in the jobs array has a started_at value
        hasStartedColumn() {
            return this.jobs.some(job => job.started_at);
        },
        //Checks if any job in the jobs array has a completed_at value
        hasCompletedColumn() {
            return this.jobs.some(job => job.completed_at);
        },
    },
})
</script>

<style scoped>

</style>