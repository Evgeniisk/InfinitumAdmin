<template>
    <div class="d-flex justify-content-between align-items-center mb-3">
        <div>
            <p class="text-muted mb-0">Manage client records and view contact details.</p>
        </div>
    </div>
<button v-if="sortedClients.length !== 0" class="btn btn-sm btn-success mb-3" data-bs-toggle="modal" data-bs-target="#addClientIndividualModal" @click="setClientType('Client_Individual')">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-plus" viewBox="0 0 16 16">
      <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
    </svg> Add Client
</button>
<div>
    <input type="text" class="form-control mb-3" placeholder="Search..." v-model="searchQuery"/>
</div>
<table class="table">
    <thead>
        <tr>
            <th scope="col">#</th>
            <th scope="col">Client Type</th>
            <th scope="col">Name</th>
            <th scope="col">Email</th>
            <th scope="col">Phone</th>
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
            </tr>
        </template>
        <template v-else-if="sortedClients.length === 0">
            <tr>
                <td colspan="5" class="text-center py-4">
                    <p class="mb-3">No clients found.</p>
                    <button class="btn btn-sm btn-success mb-3" data-bs-toggle="modal" data-bs-target="#addClientIndividualModal" @click="setClientType('Client_Individual')">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-plus" viewBox="0 0 16 16">
                            <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
                        </svg> Add First Client
                    </button>
                </td>
            </tr>
        </template>
        <template v-else>
            <tr v-for="Client in sortedClients" :key="`${Client.id}|${Client.ClientType}`" @click="goToClient(`${Client.id}|${Client.ClientType}`)" style="cursor: pointer;">
                <td>
                    <span>{{ Client.id }}</span>
                </td>
                <td>
                    <span v-if="Client.ClientType === 'Client_company'">Company</span>
                    <span v-else-if="Client.ClientType === 'Client_Individual'">Individual</span>
                </td>
                <td>
                    <span v-if="Client.ClientType === 'Client_Individual'">{{ Client.Fname }} {{ Client.Lname }}</span>
                    <span v-else-if="Client.ClientType === 'Client_company'">{{ Client.CompanyName }}</span>
                </td>
                <td>
                    <span v-if="Client.ClientType === 'Client_company'">{{ Client.CompanyEmail }}</span>
                    <span v-else-if="Client.ClientType === 'Client_Individual'">{{ Client.ClientEmail }}</span>
                </td>
                <td>
                    <span>{{ Client.Phone }}</span>
                </td>
            </tr>
        </template>
    </tbody>
</table>

<!--Modal for adding a client (client individual)-->
<div class="modal fade" id="addClientIndividualModal" tabindex="-1" aria-labelledby="addClientIndividualModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header position-relative">
                <h5 class="modal-title">Individual</h5>
                <button type="button" class="btn btn-primary position-absolute start-50 translate-middle-x" style="top: 20%; transform: translateX(-50%) translateY(-50%);" @click="setClientType('Client_Company'); SwitchToCompanyModal();" data-bs-dismiss="modal">Add Client Company</button>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <div class="container-fluid">
                    <div class="row">
                        <div class="col-8 col-sm-6">
                            <label for="FName" class="form-label">First Name</label>
                            <input v-model="newClient.Fname" type="text" class="form-control" id="Fname">
                        </div>
                        <div class="col-8 col-sm-6">
                            <label for="Lname" class="form-label">Last Name</label>
                            <input v-model="newClient.Lname" type="text" class="form-control" id="Lname">
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="ClientIndividualEmail" class="form-label">Email</label>
                        <input v-model="newClient.ClientEmail" type="email" class="form-control" id="ClientIndividualEmail">
                    </div>
                    <div class="mb-3">
                        <label for="PhoneIndividual" class="form-label">Phone</label>
                        <input v-model="newClient.Phone" type="text" class="form-control" id="Phone">
                    </div>
                    <div class="mb-3">
                        <label for="addressIndividual" class="form-label">Address</label>
                        <textarea v-model="newClient.address" class="form-control" id="address" rows="5"></textarea>
                    </div>
                    <div class="mb-3">
                        <label for="PrimaryContact" class="form-label">Related Contacts</label>
                        <multiselect v-model ="SelectedContacts" :options="clients" filter :multiple="true" :close-on-select="false" track-by="compositeKey" :custom-label="contactLabel" :maxSelectedLabels="3" class="w-full md:w-20rem">
                            <template #option="{ option }">
                                {{ option.CompanyName ? option.CompanyName : option.Fname + ' ' + option.Lname }}
                            </template>
                        </multiselect>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-danger" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-success" @click="createClientIndividual()" data-bs-dismiss="modal">Save</button>
            </div>
        </div>
    </div>
</div>

<!--Modal for adding a client (client company)-->
<div class="modal fade" id="addClientCompanyModal" tabindex="-1" aria-labelledby="addClientCompanyModalLabel" aria-hidden="true" >
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header position-relative">
                <h5 class="modal-title">Company</h5>
                <button type="button" class="btn btn-primary position-absolute start-50 translate-middle-x" style="top: 20%; transform: translateX(-50%) translateY(-50%);" @click="setClientType('Client_Individual'); SwitchToIndividualModal();" data-bs-dismiss="modal">Add Client Individual</button>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <div class="container-fluid">
                    <div class="mb-3">
                        <label for="ClientCompanyName" class="form-label">Name</label>
                        <input v-model="newClient.CompanyName" type="text" class="form-control" id="ClientCompanyName">
                    </div>
                    <div class="mb-3">
                        <label for="ClientCompanyEmail" class="form-label">Email</label>
                        <input v-model="newClient.CompanyEmail" type="email" class="form-control" id="ClientCompanyEmail">
                    </div>
                    <div class="mb-3">
                        <label for="PhoneCompany" class="form-label">Phone</label>
                        <input v-model="newClient.Phone" type="text" class="form-control" id="ClientCompanyPhone">
                    </div>
                    <div class="mb-3">
                        <label for="addressCompany" class="form-label">Address</label>
                        <textarea v-model="newClient.address" class="form-control" id="ClientCompanyaddress" rows="5"></textarea>
                    </div>
                    <div class="mb-3">
                        <label for="Signer" class="form-label">Signer of Documents</label>
                        <select v-model="newClient.IndividualId" id="Signer" class="form-select">
                            <option selected>Choose the person who will sign document on behalf of this company</option>
                            <option v-for="client in ClientsIndividuals" :key="client.id" :value="client.id">
                                {{ client.Fname }} {{ client.Lname }}
                            </option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="ClientCompanyPrimary Contact" class="form-label">Related Contacts</label>
                        <multiselect v-model ="SelectedContacts" :options="clients" filter :multiple="true" :close-on-select="false" track-by="compositeKey" :custom-label="contactLabel" :maxSelectedLabels="3" class="w-full md:w-20rem">
                            <template #option="{ option }">
                                {{ option.CompanyName ? option.CompanyName : option.Fname + ' ' + option.Lname }}
                            </template>
                        </multiselect>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-danger" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-success" @click="createClientCompany()" data-bs-dismiss="modal">Save</button>
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
            title: 'List of Clients',
            clients: [],
            ClientsIndividuals: [],
            loading: true,
            newClient: {
                ClientType: '',
                id: '',
                CompanyName: '',
                Fname: '',
                Lname: '',
                CompanyEmail: '',
                ClientEmail: '',
                Phone: '',
                address: '',
                IndividualId: '',
            },
            SelectedContacts: [],
            searchQuery: '',
        };
    },
    async mounted() {
        const csrftoken = CookieHandle('csrftoken');
        const response = await fetch(`${baseUrl}/api/clients/`, {
            method: 'GET',
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            credentials: 'include'
        })
        const data = await response.json();
        this.clients = data.clients;
        //Filters the client array to only include clients with client type of client individual
        this.ClientsIndividuals = this.clients.filter(client => client.ClientType && client.ClientType.toLowerCase() === 'client_individual');
        //Creates a new array for clients with all their original attributes but also adding attribute of composite keys to them used for tracking clients in vue multiselect
        this.clients = data.clients.map(client => ({
            ...client,
            compositeKey: `${client.id}-${client.ClientType}`
        }));
        this.loading = false
    },
    computed: {
        sortedClients() {
            const query = this.searchQuery.toLowerCase();
            if (!query) {
                return this.clients;
            }
            //Creates a shallow copy of the clients array
            return [...this.clients].sort((a, b) => {
                //gives a client a score (index) in the query
                const aScore = this.clientMatchScore(a, query);
                const bScore = this.clientMatchScore(b, query);
                //Sorts the clients by the query, the higher the index the more to the top the client will be in the clients list and in the table
                return aScore - bScore;
            });
        },
    },
    methods: {
        async createClientIndividual() {
            const csrftoken = CookieHandle('csrftoken');
            this.newClient.ClientType='Client_Individual'
            const response = await fetch(`${baseUrl}/api/clients/`, {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(this.newClient),
                credentials: 'include'
            })
            const newClient = await response.json()
            this.clients.push(newClient)

            if (this.SelectedContacts.length !== 0) {
                // collects information about selected contacts for the created client and the creaated clients information and sends it to the backend
                let selected_contacts = [];
                for(let contact of this.SelectedContacts) {
                    const to_id = contact.id
                    const to_type = contact.ClientType
                    selected_contacts.push({to_id: to_id, to_type: to_type})
                }
                const repBody = {
                    from_type: newClient.ClientType,
                    from_id: newClient.id,
                    selected_contacts: selected_contacts
                }
                const response = await fetch(`${baseUrl}/api/represents/now/`, {
                    method: 'POST',
                    headers: {
                        "Content-Type": "application/json",
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify(repBody),
                    credentials: 'include'
                });
            }
            this.SelectedContacts.length = 0;
            const data = await response.json();
        },
        async createClientCompany() {
            const csrftoken = CookieHandle('csrftoken');
            this.newClient.ClientType = 'Client_Company';
            const response = await fetch(`${baseUrl}/api/clients/`, {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(this.newClient),
                credentials: 'include'
            })
            const newClient = await response.json()
            this.clients.push(newClient)

            if (this.SelectedContacts.length !== 0) {
                // collects information about selected contacts for the created client and the creaated clients information and sends it to the backend
                let selected_contacts = [];
                for(let contact of this.SelectedContacts) {
                    const to_id = contact.id
                    const to_type = contact.ClientType
                    selected_contacts.push({to_id: to_id, to_type: to_type})
                }
                const repBody = {
                    from_type: newClient.ClientType,
                    from_id: newClient.id,
                    selected_contacts: selected_contacts
                }
                const response1 = await fetch(`${baseUrl}/api/represents/now/`, {
                    method: 'POST',
                    headers: {
                        "Content-Type": "application/json",
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify(repBody),
                    credentials: 'include'
                });
            }
            this.SelectedContacts.length = 0;
            const data1 = await response1.json();
        },
        setClientType(type) {
            this.newClient.ClientType = type;
        },
        goToClient(client) {
            const [id, type] = client.split('|')
            this.$router.push({ name: 'ClientPageNav', query: { ClientType: type, id: id} });
        },
        SwitchToCompanyModal() {
            const targetModalEl = document.getElementById('addClientCompanyModal');
            //Gets or creates a Bootstrap modal instance associated with the element above
            const targetModal = bootstrap.Modal.getOrCreateInstance(targetModalEl);
            targetModal.show();
        },
        SwitchToIndividualModal() {
            const targetModalEl = document.getElementById('addClientIndividualModal');
            //Gets or creates a Bootstrap modal instance associated with the element above
            const targetModal = bootstrap.Modal.getOrCreateInstance(targetModalEl);
            targetModal.show();
        },
        clientMatchScore(client, query) {
            const fields = [
                //Is the client type is individal makes the array value individual else makes it company
                client.ClientType === 'Client_Individual' ? 'Individual' : 'Company',
                client.Fname,
                client.Lname,
                client.CompanyName,
                client.CompanyEmail,
                client.ClientEmail,
                client.Phone
            ];
            //Combines all the fields that are not empty into one lower case string
            const combined = fields.filter(Boolean).join(' ').toLowerCase();
            //Finds the index of the of the passed query in the combined string
            const index = combined.indexOf(query);
            //If the the index is not found, returns JavaScript Infinity to make the client in the send of the sorted list
            if (index === -1) {
                return Infinity;  // No match, push to end
            } else {
                //If the index is found, returns the index of the passed query
                return index;  // Sooner in text = more relevant
            }
        },
        contactLabel(option) {
            return option.CompanyName ? option.CompanyName : option.Fname + ' ' + option.Lname;
        },
    }
})

</script>

<style scoped>

</style>