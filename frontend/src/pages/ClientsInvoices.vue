<template>
<p class="text-muted mb-3 mt-2 text-center">Create and manage invoices for this client.</p>
<button v-if="invoices.length !== 0" class="btn btn-sm btn-success mb-3" @click="handleAddInvoiceClick" >
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-plus" viewBox="0 0 16 16">
      <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
    </svg> Add Invoice
</button>
<div>
    <input type="text" class="form-control mb-3" placeholder="Search..." v-model="searchTerm"/>
</div>
<table class="table">
    <thead>
        <tr>
            <th scope="col">#</th>
            <th scope="col">id</th>
            <th scope="col">Price</th>
            <th scope="col">VAT</th>
            <th scope="col">Total</th>
            <th scope="col">Completed Value</th>
            <th scope="col">Paid</th>
            <th scope="col">Download</th>
            <th scope="col">Delete</th>
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
        <template v-else-if="invoices.length === 0">
            <tr>
                <td colspan="9" class="text-center py-4">
                    <p class="mb-3">No invoices found.</p>
                    <button class="btn btn-sm btn-success mb-3" @click="handleAddInvoiceClick">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-plus" viewBox="0 0 16 16">
                            <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
                        </svg> Add First Invoice
                    </button>
                </td>
            </tr>
        </template>
        <template v-else>
            <tr v-for="invoice in invoices" :key="invoice.id" @click="goToInvoice(invoice.id)" style="cursor: pointer;">
                <td>
                    <span>{{ invoice.invoice.id }}</span>
                </td>
                <td>
                    <span>{{ invoice.invoice.identifier }}</span>
                </td>
                <td>
                    <span>{{ invoice.invoice.InvoiceSummary.Total_price }}</span>
                </td>
                <td>
                    <span>{{ invoice.invoice.InvoiceSummary.Total_VAT }}</span>
                </td>
                <td>
                    <span>{{ invoice.invoice.InvoiceSummary.Total_with_VAT }}</span>
                </td>
                <td>
                    <span>{{ invoice.invoice.Completed_Value }}</span>
                </td>
                <td>
                    <button v-if="!invoice.invoice.Paid" class="btn btn-sm btn-success" @click="Paid(invoice.invoice.id)">
                        Paid
                    </button>
                    <button v-else class="btn btn-sm btn-danger" @click="NotPaid(invoice.invoice.id)">
                        Haven't Paid
                    </button>
                </td>
                <td>
                    <a :href="`${baseURL}${invoice.invoice.filePath}`" download>
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-download" viewBox="0 0 16 16">
                            <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5"/>
                            <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708z"/>
                        </svg>
                    </a>
                </td>
                <td>
                    <div>
                        <button class="btn btn-sm btn-danger" @click="DeleteEntryInvoice(invoice.invoice.id)">
                            <img src="/src/assets/trash.svg" width="20" height="20" alt="" style="filter: brightness(0) invert(1)">
                        </button>
                    </div>
                </td>
            </tr>
        </template>
    </tbody>
</table>

<div class="modal fade" id="InvoiceTemplateErrorModal" tabindex="-1" aria-labelledby="InvoiceTemplateErrorModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title" id="InvoiceTemplateErrorModalLabel">Invoice template missing</h2>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <p>You have't uploaded an invoice template for this client type.</p>
                <p>In order to use this feature, you have to upload an invoice template for this client type.</p>
                <p>Please head over to Templates page and upload an invoice template for this client type.</p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Understood</button>
            </div>
        </div>
    </div>
</div>

<!--Modal for adding an invoice-->
<div class="modal fade" id="addClientInvoiceModal" tabindex="-1" aria-labelledby="addClientInvoiceModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-xl modal-dialog-centered" style="max-width: 95vw;">
        <div class="modal-content">
            <div class="modal-header">
                <h1 class="modal-title fs-5" id="addClientInvoiceModalLabel">Invoice</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <div class="row g-3">
                    <div v-for="(item, index) in ProductsOrServices" :key="index" class="col-12">
                        <div class="row mb-3">
                            <div class="col-3">
                                <label class="form-label">Service or Product Name</label>
                                <input v-model="item.Name" type="text" class="form-control" placeholder="Example_name" aria-label="ServiceOrProductName">
                            </div>
                            <div class="col-2">
                                <label class="form-label">Price</label>
                                <input v-model.number="item.Price" type="number" class="form-control" placeholder="100.20" step="0.01" @input="controlDecimalPlaces(item, $event)">
                            </div>
                            <div class="col-2">
                                <label class="form-label">VAT</label>
                                <select v-model="item.Selected_VAT_Rate" id="VAT" class="form-select" @change="Calculate_VAT(item)">
                                    <option value="">No VAT</option>
                                    <option v-for="VAT_Rate in VAT_Rates" :key="index" :value="VAT_Rate">
                                        {{ VAT_Rate }}
                                    </option>
                                </select>
                            </div>
                            <div class="col-1">
                                <label class="form-label">Total</label>
                                <p>{{ item.Total_price }}</p>
                            </div>
                            <div class="col-2">
                                <label class="form-label">Assign as a job</label>
                                <Multiselect v-model="item.Employees" :options="Users" filter optionLabel="name" :multiple="true" :close-on-select="false" track-by="id" label="Fname" placeholder="Select users" :maxSelectedLabels="3" class="w-full md:w-20rem">
                                    <template #option="{ option }">
                                        {{ option.Fname }} {{ option.Lname }} {{ (option.position) }}
                                    </template>
                                </Multiselect>
                            </div>
                            <div class="col-1">
                                <label class="form-label">Deadline</label>
                                <input v-model="item.Deadline" type="date" class="form-control">
                            </div>
                            <div class="col-auto">
                                <label class="form-label">Delete</label>
                                <div>
                                    <button class="btn btn-sm btn-danger" @click="DeleteEntry(index)">
                                        <img src="/src/assets/trash.svg" width="20" height="20" alt="" style="filter: brightness(0) invert(1)">
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="d-grid gap-2 mb-4">
                        <button class="btn btn-success" @click="addProductOrService();">Add Row</button>
                    </div>
                    <hr class="w-100 my-3">
                    <div class="col-3">
                        <h1>Total:</h1>
                    </div>
                    <div class="col-2">
                        <label class="form-label">Price</label>
                        <p>{{ Calculate_Total.Price }}</p>
                    </div>
                    <div class="col-2">
                        <label class="form-label">VAT</label>
                        <p>{{ Calculate_Total.VAT }}</p>
                    </div>
                    <div class="col-2">
                        <label class="form-label">Total</label>
                        <p>{{ Calculate_Total.Price_with_VAT }}</p>
                    </div>
                    <div class="col-3">
                        <label class="form-label">Number of people assigned for this invoice:</label>
                        <p>{{ Total_number_of_employees }}</p>
                    </div>
                    <hr class="w-100 my-3">
                </div>
                <div class="row g-3">
                    <div class="col">
                        <div class="form-check form-switch">
                            <input v-model="invoiceScheduleEnabled" class="form-check-input" type="checkbox" role="switch" id="checkNativeSwitch" @change="onInvoiceScheduleChange; MainClientEmailInvoice('all');" checked switch>
                            <label class="form-check-label" for="checkNativeSwitch">Create an invoice schedule</label>
                        </div>
                    </div>
                    <div class="col">
                        <label class="form-label">Invoice schedule:</label>
                        <div class="input-group">
                            <select v-model="invoice.invoice_schedule" class="form-select" :disabled="!invoiceScheduleEnabled">
                                <option value="0">One Invoice</option>
                                <option v-if="(invoice.how_long === '0' && invoice.invoice_schedule === '0') || ['1', '2', '3', '4', '5', ''].includes(invoice.how_long)" value="1">Daily</option>
                                <option v-if="(invoice.how_long === '0' && invoice.invoice_schedule === '0') || ['2', '3', '4', '5', ''].includes(invoice.how_long)" value="2">Weekly</option>
                                <option v-if="(invoice.how_long === '0' && invoice.invoice_schedule === '0') || ['3', '4', '5', ''].includes(invoice.how_long)" value="3">Monthly</option>
                                <option v-if="(invoice.how_long === '0' && invoice.invoice_schedule === '0') || ['4', '5', ''].includes(invoice.how_long)" value="4">Quarterly</option>
                                <option v-if="(invoice.how_long === '0' && invoice.invoice_schedule === '0') || ['5', ''].includes(invoice.how_long)" value="5">Yearly</option>
                            </select>
                            <select v-model="invoice.how_long" class="form-select" :disabled="!invoiceScheduleEnabled">
                                <option value="0">None</option>
                                <option v-if="(invoice.how_long === '0' && invoice.invoice_schedule === '0') || ['1', ''].includes(invoice.invoice_schedule)" value="1">for 1 week</option>
                                <option v-if="(invoice.how_long === '0' && invoice.invoice_schedule === '0') || ['1', '2', ''].includes(invoice.invoice_schedule)" value="2">for 1 month</option>
                                <option v-if="(invoice.how_long === '0' && invoice.invoice_schedule === '0') || ['1', '2', '3', ''].includes(invoice.invoice_schedule)" value="3">for 1 quarter</option>
                                <option v-if="(invoice.how_long === '0' && invoice.invoice_schedule === '0') || ['1', '2', '3', '4', ''].includes(invoice.invoice_schedule)" value="4">for 1 year</option>
                                <option v-if="(invoice.how_long === '0' && invoice.invoice_schedule === '0') || ['1', '2', '3', '4', '5', ''].includes(invoice.invoice_schedule)" value="5">for 5 years</option>
                            </select>
                        </div>
                    </div>
                    <div class="col">
                        <label class="form-label">Automated reminders?</label>
                        <div class="input-group">
                            <select v-model="invoice.no_of_reminders" class="form-select" :disabled="!invoiceScheduleEnabled">
                                <option value="0">no reminders</option>
                                <option value="1">1 reminder</option>
                                <option value="2">2 reminders</option>
                                <option value="3">3 reminders</option>
                                <option value="4">4 reminders</option>
                                <option value="5">5 reminders</option>
                                <option value="6">6 reminders</option>
                                <option value="7">7 reminders</option>
                                <option value="8">8 reminders</option>
                                <option value="9">9 reminders</option>
                                <option value="10">10 reminders</option>
                            </select>
                            <select v-model="invoice.frequency_of_reminders" class="form-select" :disabled="!invoiceScheduleEnabled">
                                <option v-if="['0'].includes(invoice.no_of_reminders)" value="0">None</option>
                                <option v-if="['0', '1'].includes(invoice.invoice_schedule) && !(['0'].includes(invoice.no_of_reminders))" value="1">Per Day</option>
                                <option v-if="['0', '2'].includes(invoice.invoice_schedule) && !(['0'].includes(invoice.no_of_reminders))" value="2">Per Week</option>
                                <option v-if="['0', '3'].includes(invoice.invoice_schedule) && !(['0'].includes(invoice.no_of_reminders))" value="3">Per Month</option>
                                <option v-if="['0', '4'].includes(invoice.invoice_schedule) && !(['0'].includes(invoice.no_of_reminders))" value="4">Per Quarter</option>
                                <option v-if="['0', '5'].includes(invoice.invoice_schedule) && !(['0'].includes(invoice.no_of_reminders))" value="5">Per Year</option>
                            </select>
                        </div>
                    </div>
                    <p class="mt-5">If you don't want the invoices to be sent to anyone, but still want them to be generated, unselect all of the fields below.</p>
                    <div class="row g-3">
                        <label class="form-label">Select if you want to send invoices to this client:</label>
                        <div class="col">
                            <div class="form-check form-switch">
                                <input v-model="MainContactTo" :disabled="!invoiceScheduleEnabled" class="form-check-input" type="checkbox" role="switch" id="checkNativeSwitchMainTo" @change="MainClientEmailInvoice('to'); selectionDate = new Date();" switch>
                                <label class="form-label">To</label>
                            </div>
                        </div>
                        <div class="col">
                            <div class="form-check form-switch">
                                <input v-model="MainContactCC" :disabled="!invoiceScheduleEnabled" class="form-check-input" type="checkbox" role="switch" id="checkNativeSwitch" @change="MainClientEmailInvoice('cc'); selectionDate = new Date();" switch>
                                <label class="form-label">CC</label>
                            </div>
                        </div>
                        <div class="col">
                            <div class="form-check form-switch">
                                <input v-model="MainContactBcc" :disabled="!invoiceScheduleEnabled" class="form-check-input" type="checkbox" role="switch" id="checkNativeSwitch" @change="MainClientEmailInvoice('bcc'); selectionDate = new Date();" switch>
                                <label class="form-label">Bcc</label>
                            </div>
                        </div>
                    </div>
                    <div class="row g-3">
                        <label class="form-label">Select the related contacts you want to send invoices to:</label>
                        <div class="col">
                            <label class="form-label">To</label>
                            <Multiselect v-model ="SelectedContactsInvoicesTo" :options="filteredClientsForTo" filter :disabled="!invoiceScheduleEnabled" :multiple="true" :close-on-select="false" track-by="compositeKey" :custom-label="contactLabel" :maxSelectedLabels="3" class="w-full md:w-20rem">
                                <template #option="{ option }">
                                    {{ option.CompanyName ? option.CompanyName : option.Fname + ' ' + option.Lname }}
                                </template>
                            </Multiselect>
                        </div>
                        <div class="col">
                            <label class="form-label">CC</label>
                            <Multiselect v-model ="SelectedContactsInvoicesCC" :options="filteredClientsForCC" filter :disabled="!invoiceScheduleEnabled" :multiple="true" :close-on-select="false" track-by="compositeKey" :custom-label="contactLabel" :maxSelectedLabels="3" class="w-full md:w-20rem">
                                <template #option="{ option }">
                                    {{ option.CompanyName ? option.CompanyName : option.Fname + ' ' + option.Lname }}
                                </template>
                            </Multiselect>
                        </div>
                        <div class="col">
                            <label class="form-label">Bcc</label>
                            <Multiselect v-model ="SelectedContactsInvoicesBcc" :options="filteredClientsForBcc" filter :disabled="!invoiceScheduleEnabled" :multiple="true" :close-on-select="false" track-by="compositeKey" :custom-label="contactLabel" :maxSelectedLabels="3" class="w-full md:w-20rem">
                                <template #option="{ option }">
                                    {{ option.CompanyName ? option.CompanyName : option.Fname + ' ' + option.Lname }}
                                </template>
                            </Multiselect>
                        </div>
                    </div>
                    <div class="row g-3">
                        <label class="form-label">Select the related users you want to send invoices to:</label>
                        <div class="col">
                            <label class="form-label">To</label>
                            <Multiselect v-model ="SelectedUsersInvoicesTo" :options="filteredUsersForTo" filter optionLabel="name" :disabled="!invoiceScheduleEnabled" :multiple="true" :close-on-select="false" track-by="id" label="Fname" placeholder="Select users" :maxSelectedLabels="3" class="w-full md:w-20rem">
                                <template #option="{ option }">
                                    {{ option.Fname }} {{ option.Lname }} {{ (option.position) }}
                                </template>
                            </Multiselect>
                        </div>
                        <div class="col">
                            <label class="form-label">CC</label>
                            <Multiselect v-model ="SelectedUsersInvoicesCC" :options="filteredUsersForCC" filter optionLabel="name" :disabled="!invoiceScheduleEnabled" :multiple="true" :close-on-select="false" track-by="id" label="Fname" placeholder="Select users" :maxSelectedLabels="3" class="w-full md:w-20rem">
                                <template #option="{ option }">
                                    {{ option.Fname }} {{ option.Lname }} {{ (option.position) }}
                                </template>
                            </Multiselect>
                        </div>
                        <div class="col">
                            <label class="form-label">Bcc</label>
                            <Multiselect v-model ="SelectedUsersInvoicesBcc" :options="filteredUsersForBcc" filter optionLabel="name" :disabled="!invoiceScheduleEnabled" :multiple="true" :close-on-select="false" track-by="id" label="Fname" placeholder="Select users" :maxSelectedLabels="3" class="w-full md:w-20rem">
                                <template #option="{ option }">
                                    {{ option.Fname }} {{ option.Lname }} {{ (option.position) }}
                                </template>
                            </Multiselect>
                        </div>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-danger" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-success" @click="Create()" data-bs-dismiss="modal">Create</button>
            </div>
        </div>
    </div>
</div>

<!-- Invoice Delete Confirmation Modal -->
<div class="modal fade" id="DeleteInvoiceConfirmationModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="DeleteInvoiceConfirmationModalLabel">Delete invoice</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <p>Are you sure you want to delete this invoice?</p>
                <p>This action will result in termination of all invoice automations that this invoice relates to.</p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-danger" data-bs-dismiss="modal">No</button>
                <button type="button" id="confirmbutton" class="btn btn-success" data-bs-dismiss="modal">Yes</button>
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
const baseURL = import.meta.env.VITE_API_URL

export default defineComponent({
    components: {RouterView},
    data(){
        return {
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
            },
            invoices: [],
            VAT_Rates: ['0%', '5%', '20%'],
            ProductsOrServices: [
                {
                    Name: '',
                    Price: null,
                    Selected_VAT_Rate: '',
                    Total_price: null,
                    VAT: null,
                    Deadline: '',
                    Employees: [],
                }
            ],
            Total: {
                Price: 0,
                VAT: 0,
                Price_with_VAT: 0,
            },
            Users: [],
            invoiceScheduleEnabled: true,
            invoice: {
                invoice_schedule: '0',
                how_long: '0',
                no_of_reminders: '0',
                frequency_of_reminders: '0',
            },
            SelectedContactsInvoicesTo: [],
            SelectedContactsInvoicesCC: [],
            SelectedContactsInvoicesBcc: [],
            SelectedContactsContractCC: [],
            SelectedUsersContractCC: [],
            SelectedUsersInvoicesTo: [],
            SelectedUsersInvoicesCC: [],
            SelectedUsersInvoicesBcc: [],
            SelectedContacts: [],
            OriginallySelectedContacts: [],
            clients: [],
            MainContactTo: true,
            MainContactCC: false,
            MainContactBcc: false,
            baseURL: import.meta.env.VITE_API_URL,
            FileInvoiceName: "",
            loading: true,
        };
    },
    async mounted() {
        const csrftoken = CookieHandle('csrftoken');
        //For tracking the date the invoice was created
        this.selectionDate = new Date();
        const response1 = await fetch(`${baseUrl}/api/invoice/`, {
            method: 'GET',
            headers: {
                'Url-Header': window.location.href,
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            credentials: 'include',
        })
        const data1 = await response1.json();
        const combinedInvoices = [];
        const invoiceMap = {};
        //This response from the backend is a very nested json object so I process it like this here
        for (const entry of data1.InvoicesToInvoiceItems) {
            const invoiceId = entry.invoice.id;
            
            if(!(invoiceId in invoiceMap)) {
                //Makes a deep copy of the invoice component in each entry
                const invoiceCopy = structuredClone(entry.invoice);
                //stores this entry's invoice_item in the invoice copy invoice items attribute
                invoiceCopy.invoice_items = [entry.invoice_item];
                //Pushes the modified invoice copy into the combined invoices list
                combinedInvoices.push({invoice: invoiceCopy});
                //Stores the value of this invoice in the invoice map
                invoiceMap[invoiceId] = combinedInvoices.length - 1;
            } else {
                //If the invoice is in the invoiceMap already, pushes the invoice item to it
                combinedInvoices[invoiceMap[invoiceId]].invoice.invoice_items.push(entry.invoice_item);
            }
        }
        //Stores the restructure invoices data in the invoices component
        this.invoices = combinedInvoices;
        //lopps through each invoice in the invoices array and logs their file File Urls to the console (used for debugging)
        this.invoices.forEach(inv => {
            console.log('Invoice File URL:', `${baseURL}${inv.invoice.filePath}`);
        });

        const response2 = await fetch(`${baseUrl}/api/client/`, {
            method: 'GET',
            headers: {
                'Url-Header': window.location.href,
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            credentials: 'include',
        })
        const data2 = await response2.json();
        this.Client = data2;

        const response3 = await fetch(`${baseURL}/api/Users/`, {
            method: 'GET',
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            credentials: 'include',
        })
        const data3 = await response3.json();
        this.Users = data3.Active_Users;

        const response4 = await fetch(`${baseUrl}/api/clients/`, {
            method: 'GET',
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            credentials:'include'
        })
        const data4 = await response4.json()
        this.clients = data4.clients;
        //This filters the clients in the clients array to filter for clients with individual client type
        this.ClientsIndividuals = this.clients.filter(client => client.ClientType && client.ClientType.toLowerCase() === 'client_individual');
        //This creates a new array of clients with all their original attributes take from the response and adds a new composite key attribute used for tracking clients in vue multiselect
        this.clients = data4.clients.map(client => ({
            ...client,
            compositeKey: `${client.id}-${client.ClientType.toLowerCase()}`
        }));

        const response5 = await fetch(`${baseUrl}/api/represents/now/`,{
            method: 'GET',
            headers: {
                'Url-Header': window.location.href,
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            credentials: 'include',
        });
        const data5 = await response5.json();
        if (response5.status === 200) {
            //this extracts the selected clients who represent the main client the user is on and creates an array of their id and type used as unique identifiers
            const selectedKeys = data5.representslist.map(item => `${item.to_id}-${item.to_type.toLowerCase()}`);
            //This assigns the selected clients by filtering the clients from the clients whos compositekey attribute is included in the selectedkeys array
            this.SelectedContacts = this.clients.filter(client => selectedKeys.includes(client.compositeKey));
            this.OriginallySelectedContacts = JSON.parse(JSON.stringify(this.SelectedContacts));
        }

        const response7 = await fetch(`${baseUrl}/api/invoice-upload/`, {
            method: 'GET',
            headers: {
                'Url-Header': window.location.href,
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            credentials: 'include'
        });
        if (response7.status === 200) {
            const data7 = await response7.json();
            this.FileInvoiceName = data7.FileName;
        }

        this.loading = false;
    },
    computed: {
        Calculate_Total() {
            let totalPrice = 0;
            let totalVAT = 0;
            let totalWithVAT = 0;
            //This loops through each item in products or services
            for (const item of this.ProductsOrServices) {
                //Adds its price and vat to the total accumulators
                totalPrice += item.Price || 0;
                totalVAT += item.VAT || 0;
                //Convers the items total price into a number
                const total = Number(item.Total_price);
                //Adds this to the totalWith VAT if the value is a valid number (is not nan) else it adds 0
                totalWithVAT += isNaN(total) ? 0 : total;
            }
            //Returns the totals formatted to two decimal places
            return {
                Price: totalPrice.toFixed(2),
                VAT: totalVAT.toFixed(2),
                Price_with_VAT: totalWithVAT.toFixed(2),
            };
        },
        invoice_Summary() {
            //Tables to convert the selected values into what they mean
            const scheduleMap = {
                '0': 'One Invoice',
                '1': 'Daily',
                '2': 'Weekly',
                '3': 'Monthly',
                '4': 'Quarterly',
                '5': 'Yearly'
            };
            const durationMap = {
                '0': 'none',
                '1': 'for 1 week',
                '2': 'for 1 month',
                '3': 'for 1 quarter',
                '4': 'for 1 year',
                '5': 'for 5 years'
            };
            const reminderFreqMap = {
                '0': 'None',
                '1': 'Per Day',
                '2': 'Per Week',
                '3': 'Per Month',
                '4': 'Per Quarter',
                '5': 'Per Year'
            };
            //Initialises the starting date and the ending dates the invoice was created
            //When initialised the end date is the same date as the start date
            const startDate = new Date(this.selectionDate);
            const endDate = new Date(startDate);
            //Calculates the end date based on how long the invoice schedule is set to last (refer to the durationMap for the meaning of the values)
            if (this.invoice.how_long === '1') {
                endDate.setDate(endDate.getDate() + 7);
            } else if (this.invoice.how_long === '2') {
                endDate.setMonth(endDate.getMonth() + 1);
            } else if (this.invoice.how_long === '3') {
                endDate.setMonth(endDate.getMonth() + 3);
            } else if (this.invoice.how_long === '4') {
                endDate.setFullYear(endDate.getFullYear() + 1);
            } else if (this.invoice.how_long === '5') {
                endDate.setFullYear(endDate.getFullYear() + 5);
            } else {
                endDate.setDate(endDate.getDate())
            }
            //Difference between end and start dates in milliseconds
            const durationMs = endDate - startDate;
            //The equation divides the milliseconds by the number of milliseconds in one day
            //Math.celi rounds the result up to the nearest whole day.
            //It rounds the result only up to ensure it counts every day.
            const durationDays = Math.ceil(durationMs / (1000 * 60 * 60 * 24));

            
            //This function computes full months difference between two dates
            function monthDiff(d1, d2) {
                //Calculates the difference in years and converts it into months
                let months = (d2.getFullYear() - d1.getFullYear()) * 12;
                //gets the difference in months between two dates and adds them to the months difference variable
                months += d2.getMonth() - d1.getMonth();
                //if the day of second date is before the day of the first date then it subtracts 1 month from the months difference
                if (d2.getDate() < d1.getDate()) months--;
                return months;
                }

            //Frequency days calculation based on invoice_schedule:
            let numberOfInvoices;
            //This checks the invoice_schedule (refer to the scheduleMap) selection and how_long value (refer to the durationMap) for each schedule selection and calculates how many invoices should be made based of different combinations of the two
            if (this.invoice.invoice_schedule === '1') {
                //Because the invoice_schedule value of 1 means daily invoices, it just sets the number of invoices to the difference in days between the end and the start date
                numberOfInvoices = durationDays;
            } else if (this.invoice.invoice_schedule === '2') {
                //The invoice_schedule value of 2 means Weekly invoices
                if (this.invoice.how_long === '2') {
                    //The how_long value of 2 means for 1 month
                    //Therefore this gets the year and the month of the start date
                    const year = startDate.getFullYear()
                    const month = startDate.getMonth();
                    //Calculates makes a new date which is set as the last date of the month of the start date (the 0 at the end sets the date to be the last day of the the month that is before the month indicated in the function)
                    //the getDate extracts this last day of the month to use as a counter of how many days are in the given month
                    const daysInMonth = new Date(year, month + 1, 0).getDate();
                    //Based on the number of days in the given month the invoice was created it calculates the number of invoices needed to be produced for this schedule
                    //Here if the number of says in the month is over 28 then it sets it to 5 invoices and if it is not over 28 then it sets it to 5 invoices.
                    //This is because if an invoice schedule is spread into weekly invoices for one month in any given time period, the end date is on the 5th week after the week of the starting date, but if that given month is 28 days then the end date is on the 4th week after the week of the starting date
                    numberOfInvoices = daysInMonth > 28 ? 5 : 4;
                } else if (this.invoice.how_long === '4') {
                    //The how_long value of 4 means for 1 year
                    //Because the number of weeks in a year is 52 for every year i set the number of invoices to 52
                    numberOfInvoices = 52;
                } else {
                    //If the how long value of 3 or 5 are selected which mean for 1 quarter or for 5 years
                    //It devides the total number of days difference between the end and the start dates by 7 counting computing the difference in weeks instead of weeks and rounds this number up to account for partial weeks as well and just assigns the number of weekly invoice to the invoice count.
                    numberOfInvoices = Math.ceil(durationDays / 7);
                }
            } else if (this.invoice.invoice_schedule === '3') {
                if (this.invoice.how_long === '4') {
                    //Because the invoice_schedule value of 3 means monthly invoices, and the how_long value of 4 means for 1 year, this just sets the number of invoices to 12
                    numberOfInvoices = 12;
                } else {
                    //Because the invoice_schedule value of 3 means monthly invoices, for any other value of how_long this just calculates the number of full months difference between the start date and the end date of the invoice schedule
                    const months = monthDiff(startDate, endDate);
                    //If the number of months difference is 0 then this sets the number of invoices to 1, otherwise it sets the number of invoice to the different in the number of full months between thestart date and the end date
                    numberOfInvoices = months === 0 ? 1 : months;
                }
            } else if (this.invoice.invoice_schedule === '4') {
                if (this.invoice.how_long === '4') {
                    //Because the invoice_schedule value of 4 means quarterly invoices and the how_long value of 4 means for 1 year this sets the number of invoices to be 4 because there are 4 quarters in a year
                    numberOfInvoices = 4;
                } else {
                    //The only other how long option is for 5 years and the cron jobs are programmed to send invoices at the start of every consecutive quarter after sending the invoice for the first quarter it is created in, therefore this sets the number of invoices to 20.
                    numberOfInvoices = 20;
                }
            } else if (this.invoice.invoice_schedule === '5') {
                if (this.invoice.how_long === '4') {
                    //Because the invoice_schedule value of 5 means yearly invoices and the how_long value of 4 means for 1 year, this sends the number of invoices to 1.
                    numberOfInvoices = 1;
                } else {
                    //Because the invoice_schedule value of 5 means yeraly invoices and the only other how_long value can only be 5 in this case which means for 5 years, and the cron jobs are programmed to send yealy invoices each year on the date the invoice schedule was set, it just sets the number of invoices to 5.
                    numberOfInvoices = 5;
                }
            } else {
                //This is in case the invoice_schedule is one invoice
                numberOfInvoices = 1;
            }
            //This is a function which rounds floats to 2 decimal places.
            const round2 = num => Math.round(num * 100) / 100;
            //Creates an array of products or services and their attributes modified to handle errors.
            const productsRaw = this.ProductsOrServices.map(p => ({
                Name: p.Name,
                Price: p.Price || 0,
                VAT: p.VAT || 0,
                Total: p.Total_price || 0,
                Deadline: p.Deadline,
                Employees: p.Employees
            }));
            //rounds the products and services prices to 2 decimal places and accumulates total prices for the invoice
            let priceSum = 0, vatSum = 0, totalSum = 0;
            const productsRounded = productsRaw.map(p => {
                const Price = round2(p.Price);
                const VAT = round2(p.VAT);
                const Total = round2(p.Total);

                priceSum += Price;
                vatSum += VAT;
                totalSum += Total;
                //returns a modified array of products or services with each value of the array as shown below
                return {Name: p.Name, PricePerInvoice: Price, VATPerInvoice: VAT, TotalPerInvoice: Total, Deadline: p.Deadline, Employees: p.Employees};
            });
            const productsToReturn = productsRounded;

            //Totals per invoice
            const totalPricePerInvoice = priceSum;
            const totalVATPerInvoice = vatSum;
            const totalWithVATPerInvoice = totalSum;

            //Returns the invoice_summary structure to handle for the backend
            return {
                number_of_invoices: numberOfInvoices,
                //Assigns the invoice schedule value through indexing the schedule map
                invoice_schedule: scheduleMap[this.invoice.invoice_schedule] || '',
                //Assigns the duration value through indexing the duration map
                duration: durationMap[this.invoice.how_long] || '',
                reminders: {
                    //Converts the number of reminders to integers
                    count: parseInt(this.invoice.no_of_reminders),
                    //Assigns the frequency of reminders value through indexing the schedule map
                    per: reminderFreqMap[this.invoice.frequency_of_reminders] || ''
                },
                //Information for invoices
                products: productsToReturn,
                totalPrice: totalPricePerInvoice,
                totalVAT: totalVATPerInvoice,
                totalWithVAT: totalWithVATPerInvoice,
            };
        },
        Total_number_of_employees(){
            //Initialises a set to store user's ids and ensures only unique values are stored
            const employeesIds = new Set();
            //loops through each empliee assigned to each product or service and adds that employees id to the initialised set.
            //the set won't store the id twice and will just ignore the iteration of the loop if there is a suplicate
            this.ProductsOrServices.forEach(product => {
                product.Employees.forEach(employee => {
                    employeesIds.add(employee.id);
                })
            });
            //Returns the total number of employees assigned for jobs ignoring duplicates
            return employeesIds.size;
        },
        filteredClients() {
            //filters the selected contacts to not include the client the invoice is being created for
            return this.SelectedContacts.filter(client => {
                return !(client.id === this.Client.id && client.ClientType.toLowerCase() === this.Client.ClientType.toLowerCase());
            });
        },
        filteredClientsForTo() {
            //filters the selected contacts so that only clients who have not been added to the CC or BCC options can be added to the To option
            return this.filteredClients.filter(option =>
                !this.SelectedContactsInvoicesCC.includes(option) && !this.SelectedContactsInvoicesBcc.includes(option)
            );
        },
        filteredClientsForCC() {
            //filters the selected contacts so that only clients who have not been added to the To or BCC options can be added to the CC option
            return this.filteredClients.filter(option =>
                !this.SelectedContactsInvoicesTo.includes(option) && !this.SelectedContactsInvoicesBcc.includes(option)
            );
        },
        filteredClientsForBcc() {
            //filters the selected contacts so that only clients who have been added to the To or CC option can be added to the BCC option
            return this.filteredClients.filter(option =>
                !this.SelectedContactsInvoicesTo.includes(option) && !this.SelectedContactsInvoicesCC.includes(option)
            );
        },
        filteredUsersForTo() {
            //filters the users so that only users who have not been added to the CC or BCC option can be added to the To option
            return this.Users.filter(option => 
                !this.SelectedUsersInvoicesCC.includes(option) && !this.SelectedUsersInvoicesBcc.includes(option)
            );
        },
        filteredUsersForCC() {
            //filters the users so that only users who have not been added to the To or BCC option can be added to the CC option
            return this.Users.filter(option => 
                !this.SelectedUsersInvoicesTo.includes(option) && !this.SelectedUsersInvoicesBcc.includes(option)
            );
        },
        filteredUsersForBcc() {
            //filters the users so that only users who have not been added to the To or CC option can be added to the BCC option
            return this.Users.filter(option => 
                !this.SelectedUsersInvoicesTo.includes(option) && !this.SelectedUsersInvoicesCC.includes(option)
            );
        },
    },
    watch: {
        //watches the Calculate_Total computed function
        Calculate_Total: {
            handler(newVal) {
                //When the Calculate_Total return values change, it updates the total component attributes with the the changes return values of the Calculate_Total
                this.Total.Price = newVal.Price;
                this.Total.VAT = newVal.VAT;
                this.Total.Price_with_VAT = newVal.Price_with_VAT;
            },
            immediate: true, //Runs the handler function as soon as the page is mounted
            deep: true, //Watches deep changes in the Calculate_Total function
        },
        //The bottom two watch functions provide an escape for the user for their selected invoice schedule items to select a new schedule
        //watches any changes to the invoice.invoice_schedule component attribute
        'invoice.invoice_schedule'(newVal, oldVal) {
            //If the old value of the component attribute was 0 and invoice.how_long component attribute is currenly 0 and the new selected value of the invoice.invoice_schedule component is set to 0 sets the invoice.invoice_schedule component attribute to empty
            if (oldVal === '0' && this.invoice.how_long === '0' && newVal!= '0') {
                this.invoice.how_long = '';
            }
        },
        //watches any changes to the invoice.how_long component attribute
        'invoice.how_long'(newVal, oldVal) {
            //If the old values of the component attribue was 0 and invoice.invoice_schedule component attribute is currenly 0 and the new selected value of the invoice.how_long component attribute is set to 0 it sets the invoice.how_long component attribute to empty
            if (oldVal === '0' && this.invoice.invoice_schedule === '0' && newVal !== '0') {
                this.invoice.invoice_schedule = '';
            }
        },
        //watches the invoiceScheduleenabled value
        invoiceScheduleEnabled(newVal) {
            //Since the invoiceScheduleenabled value is boolean the below statement executes only if the value is false because in the if statement the !newVal evaluates to true only when newVal is false.
            if (!newVal) {
                this.invoice.invoice_schedule = '0';
                this.invoice.how_long = '0';
                this.invoice.no_of_reminders = '0';
                this.invoice.frequency_of_reminders = '0';
                this.MainContactTo = true;
            }
        },
    },
    methods: {
        Calculate_VAT(item) {
            //if the vat it set to No VAT or 0 sets the vat value to and calculates the totalprice with vat based on this.
            if(item.Selected_VAT_Rate == 'No VAT' || item.Selected_VAT_Rate == '0%') {
                item.VAT = 0;
                item.Total_price = this.roundToTwoDecimalPlaces(item.Price);
            } else {
                //if vat is set to a value other than no vat or 0 converts the selected vat % string to a float value
                const vatRate = Number(item.Selected_VAT_Rate.replace('%', '')) / 100;
                //Calculates the VAT amount based on the item's price and rounds the result to two decimal places
                item.VAT = this.roundToTwoDecimalPlaces(item.Price * vatRate);
                //calculates the total price including vat rounded to two decimal places
                item.Total_price = this.roundToTwoDecimalPlaces(item.Price + item.VAT);
            }
        },
        addProductOrService() {
            this.ProductsOrServices.push({
                Name:'',
                Price: null,
                Selected_VAT_Rate: '',
                Total_price: null,
                VAT: null,
                Deadline: '',
                Employees: [],
            });
        },
        DeleteEntry(index) {
            //Checks if there is more than one product or service
            if (this.ProductsOrServices.length > 1) {
                //If there is removes the specified item using it's index from the array
                this.ProductsOrServices.splice(index, 1);
            } else {
                //prevents the user from deleting the item if there is onlt one item in the array
                console.warn("At least one entry must remain."); //Used for debugging
            }
        },
        onInvoiceScheduleChange() {
            if (!this.invoicesScheduleEnabled) {
                this.invoice.invoice_schedule = '0';
                this.invoice.how_long = '0';
                this.invoice.no_of_reminders = '0';
                this.invoice.frequency_of_reminders = '0';
                this.SelectedContactsInvoicesTo.length = 0;
                this.SelectedContactsInvoicesCC.length = 0;
                this.SelectedContactsInvoicesBcc.length = 0;
                this.SelectedUsersInvoicesTo.length = 0;
                this.SelectedUsersInvoicesCC.length = 0;
                this.SelectedUsersInvoicesBcc.length = 0;
            }
        },
        MainClientEmailInvoice(selected) {
            if(selected === 'to' && this.MainContactTo) {
                this.MainContactCC = false;
                this.MainContactBcc = false;
            } else if (selected === 'cc' && this.MainContactCC) {
                this.MainContactBcc = false;
                this.MainContactTo = false;
            } else if (selected === 'bcc' && this.MainContactBcc) {
                this.MainContactTo = false;
                this.MainContactCC = false;
            } else if (selected === 'all' && !this.invoiceScheduleEnabled) {
                this.MainContactTo = false;
                this.MainContactCC = false;
                this.MainContactBcc = false;
            } else if (selected === 'all' && this.invoiceScheduleEnabled) {
                this.MainContactTo = true;
                this.MainContactCC = false;
                this.MainContactBcc = false;
            }
        },
        async Create() {
            const csrftoken = CookieHandle('csrftoken');
            console.log("Success")
            const response = await fetch(`${baseUrl}/api/invoice/`, {
                method: 'POST',
                headers: {
                    'Url-Header': window.location.href,
                    "Content-Type": "application/json",
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({Invoice_Schedule: this.invoice_Summary, ContactsToBeTod: this.SelectedContactsInvoicesTo, ContactsToBeCCd: this.SelectedContactsInvoicesCC, ContactsToBeBccd: this.SelectedContactsInvoicesBcc, UsersToBeTod: this.SelectedUsersInvoicesTo, UsersToBeCCd: this.SelectedUsersInvoicesCC, UsersToBeBccd: this.SelectedUsersInvoicesBcc, MainClientToBeTod: this.MainContactTo, MainClientToBeCCd: this.MainContactCC, MainClientToBeBccd: this.MainContactBcc}),
                credentials: 'include',
            });
            const data = await response.json();
            console.log("Success")
            
            const combinedInvoices = [];
            const invoiceMap = {};
            //This response from the backend is a very nested json object so I process it like this here
            for (const entry of data.InvoicesToInvoiceItems) {
                const invoiceId = entry.invoice.id;

                if(!(invoiceId in invoiceMap)) {
                    //Makes a deep copy of the invoice component in each entry
                    const invoiceCopy = structuredClone(entry.invoice);
                    //stores this entry's invoice_item in the invoice copy invoice items attribute
                    invoiceCopy.invoice_items = [entry.invoice_item];
                    //Pushes the modified invoice copy into the combined invoices list
                    combinedInvoices.push({invoice: invoiceCopy});
                    //Stores the value of this invoice in the invoice map
                    invoiceMap[invoiceId] = combinedInvoices.length - 1;
                } else {
                    //If the invoice is in the invoiceMap already, pushes the invoice item to it
                    combinedInvoices[invoiceMap[invoiceId]].invoice.invoice_items.push(entry.invoice_item);
                }
            }
            console.log("Success")
            //Pushes the modified invoice to the invoices component list
            for (const entry of combinedInvoices) {
                this.invoices.push(entry);
            }
            console.log("Success")
        },
        async Paid(invoice_id) {
            const csrftoken = CookieHandle('csrftoken');
            //finds the invoice in the list that has the same id as the invoice id passed to the function
            const invoice1 = this.invoices.find(invoice => invoice.invoice.id === invoice_id)
            const invoice = invoice1?.invoice; //If invoice1 has found the invoice with the id, it returns it, if it hasn't returns indefined *used for debugging*
            const response = await fetch(`${baseUrl}/api/invoice/`, {
                method: 'PUT',
                headers: {
                    "Content-Type": "application/json",
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({Invoice: invoice, Paid: true}),
                credentials: 'include'
            })
            const data = await response.json();
            invoice.Paid = data.invoice.Paid;
        },
        async NotPaid(invoice_id){
            const csrftoken = CookieHandle('csrftoken');
            //finds the invoice in the list that has the same id as the invoice id passed to the function
            const invoice1 = this.invoices.find(invoice => invoice.invoice.id === invoice_id)
            const invoice = invoice1?.invoice; //If invoice1 has found the invoice with the id, it returns it, if it hasn't returns indefined *used for debugging*
            const response = await fetch(`${baseUrl}/api/invoice/`, {
                method: 'PUT',
                headers: {
                    "Content-Type": "application/json",
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({Invoice: invoice, Paid: false}),
                credentials: 'include'
            })
            const data = await response.json();
            invoice.Paid = data.invoice.Paid;
        },
        controlDecimalPlaces(item, event) {
            //retrieves the current value from the input field
            let val = event.target.value;
            //Checks if the value contains a decimal point
            if (val.includes('.')) {
                //Extracts the decimal places values
                let decimalPart = val.split('.')[1];
                //Checks if there are are more than two decimal places
                if (decimalPart.length > 2) {
                    //finds the index of the decimal point in the value, changes the index to 3 to get the index of the 3rd decimal place of the value and the splice retuns the value starting from index 1 up to and not including the index of the 3rd decimal place cutting out any decimal places above 2.
                    val = val.slice(0, val.indexOf('.') + 3);
                    //Updates the input field with the modified value
                    event.target.value = val;
                }
            }
            //Converts the modified value to a number and stores it the passed items price attribute
            item.Price = Number(val);
            //Recalculates vat and total price based on the modified value
            this.Calculate_VAT(item);
        },
        roundToTwoDecimalPlaces(num) {
            //Rounds the number to two decimal places
            return Number(num.toFixed(2))
        },
        //Used for debugging
        printUrl(filePath) {
            const fullUrl = `${this.baseURL}${filePath}`;
            console.log(fullUrl);
        },
        //Returns Company name attribue if that attribute is present in the option, otherwise returns the fname and lname attributes
        contactLabel(option) {
            return option.CompanyName ? option.CompanyName : option.Fname + ' ' + option.Lname;
        },
        handleAddInvoiceClick() {
            if (this.FileInvoiceName) {
                const modalId = 'addClientInvoiceModal'
                const modalEl = document.getElementById(modalId)
                const modal = new bootstrap.Modal(modalEl)
                modal.show()
            } else {
                const modalId = 'InvoiceTemplateErrorModal'
                const modalEl = document.getElementById(modalId)
                const modal = new bootstrap.Modal(modalEl)
                modal.show()
            }
        },
        DeleteEntryInvoice(invoice) {
            var ConfirmationModal = new bootstrap.Modal(document.getElementById('DeleteInvoiceConfirmationModal'))
            ConfirmationModal.show();
            const confirmBtn = document.getElementById('confirmbutton');
            //Replaces the confirmation button with a close to remove any event listeners previously used
            //Came up with it after debugging because the buttons were conflicting for some reason
            confirmBtn.replaceWith(confirmBtn.cloneNode(true));
            const newConfirmBtn = document.getElementById('confirmbutton');
            //Adds a new click event listeneder to the confirm button that handles sending the request on button click
            newConfirmBtn.addEventListener('click', async () => {
                const response = await fetch(`${baseUrl}/api/invoice/`, {
                    method: 'DELETE',
                    headers: {'Content-Type': 'application/json'},
                    credentials: 'include',
                    body: JSON.stringify({invoice_id : invoice}),
                });
                const data = await response.json();
                if (data.DELETE == 'Confirm') {
                    //finds the index of the invoice item by comparing it's id with the passed invoice object which stores invoice id
                    const index = this.invoices.findIndex(item => item.invoice.id === invoice);
                    //removes the invoice from the invoices array
                    this.invoices.splice(index, 1);
                }
            });
        },
    },
})
</script>

<style scoped>

</style>