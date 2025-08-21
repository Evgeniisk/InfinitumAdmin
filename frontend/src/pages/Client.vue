<template>
<p class="text-muted mb-3 mt-2">Manage client details</p>
<form>
    <div v-if="Client.ClientType === 'Client_Company'" class="mb-3">
        <label for="Name" class="form-label">Name:</label>
        <input id="InputName" class="form-control" aria-describedby="nameHelp" v-model="Client.CompanyName">
    </div>
    <div v-if="Client.ClientType === 'Client_Individual'" class="row g-3">
        <div class="col">
            <label for="inputFirstName" class="form-label">First name</label>
            <input type="text" name="first_name" class="form-control" placeholder="First Name" aria-label="First name" v-model="Client.Fname">
        </div>
        <div class="col">
            <label for="inputLastName" class="form-label">Last Name</label>
            <input type="text" name="last_name" class="form-control" placeholder="Last Name" aria-label="Last name" v-model="Client.Lname">
        </div>
    </div>
    <div class="mb-3">
        <label for="inputEmail" class="form-label">Email address</label>
        <input v-if="Client.ClientType === 'Client_Company'" type="email" name="email" class="form-control" placeholder="example@gmail.com" aria-label="Email address" v-model="Client.CompanyEmail">
        <input v-else-if="Client.ClientType === 'Client_Individual'" type="email" name="email" class="form-control" placeholder="example@gmail.com" aria-label="Email address" v-model="Client.ClientEmail">
    </div>
    <div class="mb-3">
        <label for="inputPhone" class="form-label">Phone</label>
        <input type="text" name="phone" class="form-control" placeholder="+447550406170" aria-label="Phone number" v-model="Client.Phone">
    </div>
    <div class="mb-3">
        <label for="inputAddress" class="form-label">Address</label>
        <textarea type="text" class="form-control" id="address" rows="5" v-model="Client.address"></textarea>
    </div>
    <div v-if="Client.ClientType === 'Client_Company'" class="mb-3">
        <label for="Signer" class="form-label">Signer of Documents</label>
        <select v-model="Client.IndividualId" class="form-select">
            <option value="">Please select this option if you don't want to select anyone for now</option>
            <option v-for="client in ClientsIndividuals" :key="client.id" :value="client.id">
                {{ client.Fname }} {{ client.Lname }}
            </option>
        </select>
    </div>
    <div class="mb-3">
        <label for="RelatedContacts" class="form-label">Select to modify related contacts:</label>
        <!--vue multiselect tag-->
        <multiselect v-model="SelectedContacts" :options="filteredClients" filter :multiple="true" :close-on-select="false" track-by="compositeKey" :custom-label="contactLabel" :maxSelectedLabels="3" class="w-full md:w-20rem">
            <template #option="{ option }">
                {{ option.CompanyName ? option.CompanyName : option.Fname + ' ' + option.Lname }}
            </template>
        </multiselect>
    </div>
    <div class="mb-12">
        <label for="PrimaryContact" class="form-label">Related Contacts:</label>
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Client Type</th>
                    <th scope="col">Name</th>
                    <th scope="col">Email</th>
                    <th scope="col">Phone</th>
                    <th scope="col">
                        <div class="d-flex align-items-center">
                            <span>Templates</span>
                            <span class="d-inline-block ms-2" tabindex="0" data-bs-toggle="popover" data-bs-trigger="hover focus" data-bs-title="The information of the chosen related contact will be used to replace placeholders in templates." data-bs-content="You can only choose one company and one individual from this list. Their information will be used to replace paceholders in your templates. Please refer to the templates page for more information.">
                                <img src="/src/assets/info-circle.svg" alt="Info">
                            </span>
                        </div>
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="client in SelectedContacts" :key="`${client.id}|${client.ClientType}`" @click="goToClient(`${client.id}|${client.ClientType}`)" style="cursor: pointer;">
                    <td>
                        <span>{{ client.id }}</span>
                    </td>
                    <td>
                        <span v-if="client.ClientType === 'Client_company'">Company</span>
                        <span v-else-if="client.ClientType === 'Client_Individual'">Individual</span>
                    </td>
                    <td>
                        <span v-if="client.ClientType === 'Client_Individual'">{{ client.Fname }} {{ client.Lname }}</span>
                        <span v-else-if="client.ClientType === 'Client_company'">{{ client.CompanyName }}</span>
                    </td>
                    <td>
                        <span v-if="client.ClientType === 'Client_company'">{{ client.CompanyEmail }}</span>
                        <span v-else-if="client.ClientType === 'Client_Individual'">{{ client.ClientEmail }}</span>
                    </td>
                    <td>
                        <span>{{ client.Phone }}</span>
                    </td>
                    <td>
                        <div class="form-check" v-if="client.ClientType === 'Client_company'">
                            <input class="form-check-input" type="checkbox" :id="`company-radio-${client.id}`" v-model="client.selected" @click.stop="companyCheck(client)"/>
                        </div>
                        <div class="form-check" v-else-if="client.ClientType === 'Client_Individual'">
                            <input class="form-check-input" type="checkbox" :id="`individual-radio-${client.id}`" v-model="client.selected" @click.stop="individualCheck(client)"/>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    <div class="d-grid gap-2">
        <button type="button" class="btn btn-success" @click="save()" :disabled="!form_change()">Save</button>
    </div>
</form>

</template>

<script lang="ts">

import { defineComponent } from "vue";
import { RouterView } from "vue-router";
import { Popover } from 'bootstrap';
import {CookieHandle} from '@/utils.js';

//This is a dynamic url that import a development server url from .env.development file when the development server is run and imports the production url when the npm run build is run for production
const baseUrl = `${import.meta.env.VITE_API_URL}/main`;

export default defineComponent({
    components: {RouterView},
    data(){
        return {
            title: 'Client Profile',
            clients: [],
            ClientsIndividuals: [],
            Client: {
                ClientType: "",
                id: Number,
                CompanyName: '',
                Fname: '',
                Lname: '',
                CompanyEmail: '',
                ClientEmail: '',
                Phone: '',
                address: '',
                IndividualId: '',
            },
            OriginalClient:{
                ClientType: "",
                id: Number,
                CompanyName: '',
                Fname: '',
                Lname: '',
                CompanyEmail: '',
                ClientEmail: '',
                Phone: '',
                address: '',
                IndividualId: '',
            },
            PrimaryContact: {
                to_type: '',
                to_id: '',
                to_Fname: '',
                to_Lname: '',
                to_CompanyName: '',
                Email: '',
                Phone: '',
                address: '',
            },
            SelectedContacts: [],
            OriginallySelectedContacts: [],
        };
    },
    async mounted() {
        const csrftoken = CookieHandle('csrftoken');
        //initialises bootstrap popovers
        const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
        [...popoverTriggerList].forEach(el => new Popover(el));

        const response1 = await fetch(`${baseUrl}/api/client/`, {
            method: 'GET',
            headers: {
                'Url-Header': window.location.href,
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            credentials: 'include',
        })
        const data1 = await response1.json()
        this.Client = data1;
        this.OriginalClient = JSON.parse(JSON.stringify(data1));

        const response2 = await fetch(`${baseUrl}/api/clients/`, {
            method: 'GET',
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            credentials:'include'
        })
        const data2 = await response2.json()
        this.clients = data2.clients;
        //This flters by clients who have a client type and whos client type is client_individual when converted to lower case
        this.ClientsIndividuals = this.clients.filter(client => client.ClientType && client.ClientType.toLowerCase() === 'client_individual');
        //this map function keeps all the existing attributes each client has in the clients array and adds a composite key attribute to each client to be used to uniquely identify them
        //the addition of this composite key attribute had to be done to track the clients added and removed in vue multiselect as the clients in the array don't have an attribute with a unique value for vue multiselect to track them by
        this.clients = data2.clients.map(client => ({
            ...client,
            compositeKey: `${client.id}-${client.ClientType.toLowerCase()}`
        }));

        const response3 = await fetch(`${baseUrl}/api/represents/now/`,{
            method: 'GET',
            headers: {
                'Url-Header': window.location.href,
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            credentials: 'include',
        });
        const data3 = await response3.json();
        if (response3.status === 200) {
            //this extracts the selected clients who represent the main client the user is on and creates an array of their id and type used as unique identifiers
            const selectedKeys = data3.representslist.map(item => `${item.to_id}-${item.to_type.toLowerCase()}`);
            //this filters the clients in the clients array only if they include the composite key that is in the selected keys array created above
            //For each matched client by the filter function it finds the matching client in the represents list to the clients list by id and client type and stores the array in the matchingItem contant
            this.SelectedContacts = this.clients.filter(client => selectedKeys.includes(client.compositeKey)).map(client => {const matchingItem = data3.representslist.find(item => item.to_id === client.id && item.to_type.toLowerCase() === client.ClientType.toLowerCase());
                //Then it stores each client with it's original attributes and adds an additional selected attribute which set to selected if the client has a matching item and to false if it doesn't
                return {
                    ...client,
                    selected: matchingItem ? matchingItem.selected : false
                };
            });
            //this new selected contracys with the selected flag you could call it is stored as a deep copy in the originallyselectedcontacts component
            this.OriginallySelectedContacts = JSON.parse(JSON.stringify(this.SelectedContacts));
        }
    },
    computed: {
        //This functions makes sure that the client that is being edited cannot be selected as it's own selected contact
        filteredClients() {
            //It filters the client by excluding the current client being edited from the list
            return this.clients.filter(client => {
                return !(client.id === this.Client.id && client.ClientType.toLowerCase() === this.Client.ClientType.toLowerCase());
            });
        },
    },
    methods: {
        async save() {
            const csrftoken = CookieHandle('csrftoken');
            if (JSON.stringify(this.SelectedContacts) != JSON.stringify(this.OriginallySelectedContacts)) {
                // collects information about selected contacts for this client and this clients information and sends it to the backend
                let selected_contacts = [];
                for(let contact of this.SelectedContacts) {
                    const to_id = contact.id
                    const to_type = contact.ClientType
                    const selected = contact.selected
                    selected_contacts.push({to_id: to_id, to_type: to_type, selected: selected})
                }
                const repBody = {
                    from_type: this.Client.ClientType,
                    from_id: this.Client.id,
                    selected_contacts: selected_contacts
                }
                const response = await fetch(`${baseUrl}/api/represents/now/`, {
                    method: 'PUT',
                    headers: {
                        'Url-Header': window.location.href,
                        "Content-Type": "application/json",
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify(repBody),
                    credentials: 'include',
                });
                const data = await response.json();
                //this extracts the selected clients who represent the main client the user is on and creates an array of their is and type used as unique identifiers
                const selectedKeys = data.Represents.map(item => `${item.to_id}-${item.to_type.toLowerCase()}`);
                //this filters the clients in the clients array only if they include the composite key that is in the selected keys array created above
                //For each matched client by the filter function it finds the matching client in the represents list to the clients list by id and client type and stores the array in the matchingItem contant
                this.SelectedContacts = this.clients.filter(client => selectedKeys.includes(client.compositeKey)).map(client => {const matchingItem = data.Represents.find(item => item.to_id === client.id && item.to_type.toLowerCase() === client.ClientType.toLowerCase());
                    //Then it stores each client with it's original attributes and adds an additional selected attribute which set to selected if the client has a matching item and to false if it doesn't
                    return {
                        ...client,
                        selected: matchingItem ? matchingItem.selected : false
                    };
                });
                //this new selected contracys with the selected flag you could call it is stored as a deep copy in the originallyselectedcontacts component
                this.OriginallySelectedContacts = JSON.parse(JSON.stringify(this.SelectedContacts));
            }

            
            if (JSON.stringify(this.Client) !== JSON.stringify(this.OriginalClient)) {
                await fetch(`${baseUrl}/api/client/`, {
                    method: 'PUT',
                    headers: {
                        'Url-Header': window.location.href,
                        "Content-Type": "application/json",
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify(this.Client),
                    credentials: 'include'
                });
                this.OriginalClient = JSON.parse(JSON.stringify(this.Client));
            }
        },
        goToClient(client) {
            const [id, type] = client.split('|')
            this.$router.push({ name: this.$route.name, query: { ClientType: type, id: id} });
        },
        form_change() {
            if (JSON.stringify(this.SelectedContacts) !== JSON.stringify(this.OriginallySelectedContacts) || JSON.stringify(this.Client) !== JSON.stringify(this.OriginalClient)) {
                return true
            } else {
                return false
            }
        },
        //This function makes sure that for any company client type only one company can be selected to be the representative to be used in templates
        companyCheck(selectedClient) {
            //It loops over every client in selected contact
            for (let client of this.SelectedContacts) {
                //if the client type of the client is client company
                if (client.ClientType === 'Client_company') {
                    //this assigned the selected attribute of the current client in the loop to it's id, compares it with the selected client id passed to this function if they match is switches the selected value to the opposite of what it was before
                    //If they don't match, i.e. it is not the selected client it sets it's selected attribute to false
                    client.selected = client.id === selectedClient.id ? !client.selected : false;
                }
            }
        },
        //This function makes sure that for any company client type only one company can be selected to be the representative to be used in templates
        individualCheck(selectedClient) {
            //It loops over every client in selected contact
            for (let client of this.SelectedContacts) {
                //if the client type of the client is client company
                if (client.ClientType === 'Client_Individual') {
                    //this assigned the selected attribute of the current client in the loop to it's id, compares it with the selected client id passed to this function if they match is switches the selected value to the opposite of what it was before
                    //If they don't match, i.e. it is not the selected client it sets it's selected attribute to false
                    client.selected = client.id === selectedClient.id ? !client.selected : false;
                }
            }
        },
        contactLabel(option) {
            //this returns company name of the selected contact if it has that attribute, if it doesnt it returns attributes of client individual
            return option.CompanyName ? option.CompanyName : option.Fname + ' ' + option.Lname;
        },
    },
});

</script>

<style scoped>

</style>