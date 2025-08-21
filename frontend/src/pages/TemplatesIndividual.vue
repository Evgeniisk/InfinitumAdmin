<template>
    <form>
        <div class="row mb-3">
            <div class="col-12">
                <h5 for="formFileContract" class="form-label w-100">Please select a template to use for your contracts:</h5>
            </div>
            <div class="col-11">
                <div class="input-group">
                    <input class="form-control" type="file" id="formFileContract" @change="handleFileContract" accept=".docx"/>
                </div>
            </div>
            <div class="col-1">
                <span class="d-inline-block" tabindex="0" data-bs-toggle="popover" data-bs-trigger="hover focus" data-bs-title="This input field recognises only .docx file formats." data-bs-content="This input field recognises the following placeholders inside the .docx document that are inside the { } brackets: {Client_First_Name}, {Client_Last_Name}, {Client_Address}, {Directors_Signature}, {Date_Signed_Director}, {Client_Signature}, {Date_Signed_Client}, {Total_price}, {Total_Price_with_VAT}, {Payments_Breakdown} and recognises the following placeholders inside the table of the .docx document that are inside the { } brackets: {Service_or_Product_Name}, {Price}, {VAT}, {Price_with_VAT}, {Total_price}, {Total_VAT}, {Total_Price_with_VAT}.">
                    <img src="/src/assets/info-circle.svg">
                </span>
            </div>
            <div class="col-12">
                <template v-if="loading">
                    <p class="placeholder-glow">
                        <span class="placeholder col-3"></span>
                    </p>
                    <p class="placeholder-wave">
                        <span class="placeholder col-12"></span>
                    </p>
                </template>
                <template v-else>
                    <div v-if="FileName" class="mb-2">
                        <strong>Current file:</strong>
                        <p>{{ FileName }}</p>
                    </div>
                    <div v-else>
                        <p>No file found in the database, please upload a file.</p>
                    </div>
                </template>
            </div>
        </div>
        <div class="row mb-3">
            <div class="col-12">
                <h5 for="formFileInvoice" class="form-label w-100">Please select a template to use for your invoices:</h5>
            </div>
            <div class="col-11">
                <div class="input-group">
                    <input class="form-control" type="file" id="formFileInvoice" @change="handleFileInvoice" accept=".docx"/>
                </div>
            </div>
            <div class="col-1">
                <span class="d-inline-block" tabindex="0" data-bs-toggle="popover" data-bs-trigger="hover focus" data-bs-title="This input field recognises only .docx file formats." data-bs-content="This input field recognises the following placeholders inside the .docx document that are inside the { } brackets: {Client_First_Name}, {Client_Last_Name}, {Client_Address}, {Date}, {Invoice_Number}, {Due_date} and recognises the following placeholders inside the table of the .docx document that are inside the { } brackets: {Service_or_Product_Name}, {Price}, {VAT}, {Price_with_VAT}, {Total_price}, {Total_VAT}, {Total_Price_with_VAT}.">
                    <img src="/src/assets/info-circle.svg">
                </span>
            </div>
            <div class="col-12">
                <template v-if="loading">
                    <p class="placeholder-glow">
                        <span class="placeholder col-3"></span>
                    </p>
                    <p class="placeholder-wave">
                        <span class="placeholder col-12"></span>
                    </p>
                </template>
                <template v-else>
                    <div v-if="FileInvoiceName" class="mt-2">
                        <strong>Current file:</strong>
                        <p>{{ FileInvoiceName }}</p>
                    </div>
                    <div v-else>
                        <p>No file found in the database, please upload a file.</p>
                    </div>
                </template>
            </div>
        </div>
        <hr class="w-100 my-3">
        <h5>Please fill in the email subject template you want to use for sending contracts through DocuSign:</h5>
        <div class="row mb-3">
            <label for="EmailSubjectforDocuSign" class="form-label">Subject</label>
            <div class="col-11"> 
                <input type="text" class="form-control" id="EmailSubjectforDocuSign" placeholder="DocuSign Example" v-model="EmailSubjectforDocuSign">
            </div>
            <div class="col-1">
                <span class="d-inline-block" tabindex="0" data-bs-toggle="popover" data-bs-trigger="hover focus" data-bs-content="This field acceps the following placeholders inside the { } brackets: {Client_First_Name}, {Client_Last_Name}, {Related_Contact_First_Name}, {Related_Contact_Last_Name}, {Related_Contact_Company_Name}. In order for the related contacts placeholders to be replaced, you have to choose them to be used for templates on the client information page. An example of using this is: {Client_First_Name} {Client_Last_Name}, you received a contract from Example Ltd. Where {Client_First_Name} and {Client_Last_Name} will be replaced with your client's first and last names">
                    <img src="/src/assets/info-circle.svg">
                </span>
            </div>
        </div>
        <hr class="w-100 my-3">
        <h5>Please fill in the email template you want to use for sending one off invoices without a contract:</h5>
        <div class="row mb-3">
            <label for="EmailSubjectInputInvoice1" class="form-label">Subject</label>
            <div class="col-11">
                <input type="text" class="form-control" id="EmailSubjectInputInvoice1" placeholder="Invoice Example" v-model="EmailInvoiceWithoutContract.Subject">
            </div>
            <div class="col-1">
                <span class="d-inline-block" tabindex="0" data-bs-toggle="popover" data-bs-trigger="hover focus" data-bs-content="This field acceps the following placeholders inside the { } brackets: {Client_First_Name}, {Client_Last_Name}, {Period}, {Related_Contact_First_Name}, {Related_Contact_Last_Name}, {Related_Contact_Company_Name}. In order for the related contacts placeholders to be replaced, you have to choose them to be used for templates on the client information page. An example of using this is: Dear {Client_First_Name}, you received an invoice from Example Ltd for the period of {Period}. Where {Client_First_Name} will be replaced with your client's first name and {Period} will be replaced with 'month starting on dd-mm-yyyy' or 'week starting on dd-mm-yyyy' depending on the chosen schedule period of invoices.">
                    <img src="/src/assets/info-circle.svg">
                </span>
            </div>
        </div>
        <div class="row mb-3">
            <label for="EmailBodyInputInvoice1" class="form-label">Body</label>
            <div class="col-11">
                <textarea class="form-control" id="EmailBodyInvoice1" rows="5" v-model="EmailInvoiceWithoutContract.Body"></textarea>
            </div>
            <div class="col-1">
                <span class="d-inline-block" tabindex="0" data-bs-toggle="popover" data-bs-trigger="hover focus" data-bs-content="This field acceps the following placeholders inside the { } brackets: {Client_First_Name}, {Client_Last_Name}, {Period}, {Related_Contact_First_Name}, {Related_Contact_Last_Name}, {Related_Contact_Company_Name}. In order for the related contacts placeholders to be replaced, you have to choose them to be used for templates on the client information page. An example of using this is: Dear {Related_Contact_First_Name}, {Client_First_Name} {Client_Last_Name} received an invoice from Example Ltd for the period of {Period}. Where {Related_Contact_First_Name} will be replaced with the chosen related contact individual's first name related to the client and {Period} will be replaced with 'month starting on dd-mm-yyyy' or 'week starting on dd-mm-yyyy' depending on the chosen schedule period of invoices.">
                    <img src="/src/assets/info-circle.svg">
                </span>
            </div>
        </div>
        <hr class="w-100 my-3">
        <h5>Please fill in the email template you want to use for sending an invoice after contract if the invoice isn't broken into multiple invoices:</h5>
        <div class="row mb-3">
            <label for="EmailSubjectInputInvoice1" class="form-label">Subject</label>
            <div class="col-11">
                <input type="text" class="form-control" id="EmailSubjectInputInvoice1" placeholder="Invoice Example" v-model="EmailInvoiceOnlyOneWithContract.Subject">
            </div>
            <div class="col-1">
                <span class="d-inline-block" tabindex="0" data-bs-toggle="popover" data-bs-trigger="hover focus" data-bs-content="This field acceps the following placeholders inside the { } brackets: {Client_First_Name}, {Client_Last_Name}, {Period}, {Related_Contact_First_Name}, {Related_Contact_Last_Name}, {Related_Contact_Company_Name}. In order for the related contacts placeholders to be replaced, you have to choose them to be used for templates on the client information page. An example of using this is: Dear {Related_Contact_First_Name}, {Client_First_Name} {Client_Last_Name} received an invoice from Example Ltd for the period of {Period}. Where {Related_Contact_First_Name} will be replaced with the chosen related contact individual's first name related to the client, and {Period} will be replaced with 'month starting on dd-mm-yyyy' or 'week starting on dd-mm-yyyy' depending on the chosen schedule period of invoices.">
                    <img src="/src/assets/info-circle.svg">
                </span>
            </div>
        </div>
        <div class="row mb-3">
            <label for="EmailBodyInputInvoice1" class="form-label">Body</label>
            <div class="col-11">
                <textarea class="form-control" id="EmailBodyInvoice1" rows="5" v-model="EmailInvoiceOnlyOneWithContract.Body"></textarea>
            </div>
            <div class="col-1">
                <span class="d-inline-block" tabindex="0" data-bs-toggle="popover" data-bs-trigger="hover focus" data-bs-content="This field acceps the following placeholders inside the { } brackets: {Client_First_Name}, {Client_Last_Name}, {Period}, {Related_Contact_First_Name}, {Related_Contact_Last_Name}, {Related_Contact_Company_Name}. In order for the related contacts placeholders to be replaced, you have to choose them to be used for templates on the client information page. An example of using this is: Dear {Related_Contact_First_Name}, {Client_First_Name} {Client_Last_Name} received an invoice from Example Ltd for the period of {Period}. Where {Related_Contact_First_Name} will be replaced with the chosen related contact individual's first name related to the client, and {Period} will be replaced with 'month starting on dd-mm-yyyy' or 'week starting on dd-mm-yyyy' depending on the chosen schedule period of invoices.">
                    <img src="/src/assets/info-circle.svg">
                </span>
            </div>
        </div>
        <hr class="w-100 my-3">
        <h5>Please fill in the email template you want to use for sending first invoice after contract if it's broken into multiple invoices:</h5>
        <div class="row mb-3">
            <label for="EmailSubjectInputInvoice2" class="form-label">Subject</label>
            <div class="col-11">
                <input type="text" class="form-control" id="EmailSubjectInputInvoice2" placeholder="Invoice Reminder Example" v-model="EmailInvoiceFirstWithContract.Subject">
            </div>
            <div class="col-1">
                <span class="d-inline-block" tabindex="0" data-bs-toggle="popover" data-bs-trigger="hover focus" data-bs-content="This field acceps the following placeholders inside the { } brackets: {Client_First_Name}, {Client_Last_Name}, {Period}, {Related_Contact_First_Name}, {Related_Contact_Last_Name}, {Related_Contact_Company_Name}. In order for the related contacts placeholders to be replaced, you have to choose them to be used for templates on the client information page. An example of using this is: Dear {Related_Contact_First_Name}, {Client_First_Name} {Client_Last_Name} received an invoice from Example Ltd for the period of {Period}. Where {Related_Contact_First_Name} will be replaced with the chosen related contact individual's first name related to the client, and {Period} will be replaced with 'month starting on dd-mm-yyyy' or 'week starting on dd-mm-yyyy' depending on the chosen schedule period of invoices.">
                    <img src="/src/assets/info-circle.svg">
                </span>
            </div>
        </div>
        <div class="row mb-3">
            <label for="EmailBodyInputInvoice2" class="form-label">Body</label>
            <div class="col-11">
                <textarea class="form-control" id="EmailBodyInvoice2" rows="5" v-model="EmailInvoiceFirstWithContract.Body"></textarea>
            </div>
            <div class="col-1">
                <span class="d-inline-block" tabindex="0" data-bs-toggle="popover" data-bs-trigger="hover focus" data-bs-content="This field acceps the following placeholders inside the { } brackets: {Client_First_Name}, {Client_Last_Name}, {Period}, {Related_Contact_First_Name}, {Related_Contact_Last_Name}, {Related_Contact_Company_Name}. In order for the related contacts placeholders to be replaced, you have to choose them to be used for templates on the client information page. An example of using this is: Dear {Related_Contact_First_Name}, {Client_First_Name} {Client_Last_Name} received an invoice from Example Ltd for the period of {Period}. Where {Related_Contact_First_Name} will be replaced with the chosen related contact individual's first name related to the client, and {Period} will be replaced with 'month starting on dd-mm-yyyy' or 'week starting on dd-mm-yyyy' depending on the chosen schedule period of invoices.">
                    <img src="/src/assets/info-circle.svg">
                </span>
            </div>
        </div>
        <h5>Please fill in the email template you want to use for sending invoices relating to a contract after the first invoice:</h5>
        <div class="row mb-3">
            <label for="EmailSubjectInputInvoice2" class="form-label">Subject</label>
            <div class="col-11">
                <input type="text" class="form-control" id="EmailSubjectInputInvoice2" placeholder="Invoice Reminder Example" v-model="EmailInvoiceOtherInvoicesWithContract.Subject">
            </div>
            <div class="col-1">
                <span class="d-inline-block" tabindex="0" data-bs-toggle="popover" data-bs-trigger="hover focus" data-bs-content="This field acceps the following placeholders inside the { } brackets: {Client_First_Name}, {Client_Last_Name}, {Period}, {Related_Contact_First_Name}, {Related_Contact_Last_Name}, {Related_Contact_Company_Name}. In order for the related contacts placeholders to be replaced, you have to choose them to be used for templates on the client information page. An example of using this is: Dear {Related_Contact_First_Name}, {Client_First_Name} {Client_Last_Name} received an invoice from Example Ltd for the period of {Period}. Where {Related_Contact_First_Name} will be replaced with the chosen related contact individual's first name related to the client, and {Period} will be replaced with 'month starting on dd-mm-yyyy' or 'week starting on dd-mm-yyyy' depending on the chosen schedule period of invoices.">
                    <img src="/src/assets/info-circle.svg">
                </span>
            </div>
        </div>
        <div class="row mb-3">
            <label for="EmailBodyInputInvoice2" class="form-label">Body</label>
            <div class="col-11">
                <textarea class="form-control" id="EmailBodyInvoice2" rows="5" v-model="EmailInvoiceOtherInvoicesWithContract.Body"></textarea>
            </div>
            <div class="col-1">
                <span class="d-inline-block" tabindex="0" data-bs-toggle="popover" data-bs-trigger="hover focus" data-bs-content="This field acceps the following placeholders inside the { } brackets: {Client_First_Name}, {Client_Last_Name}, {Period}, {Related_Contact_First_Name}, {Related_Contact_Last_Name}, {Related_Contact_Company_Name}. In order for the related contacts placeholders to be replaced, you have to choose them to be used for templates on the client information page. An example of using this is: Dear {Related_Contact_First_Name}, {Client_First_Name} {Client_Last_Name} received an invoice from Example Ltd for the period of {Period}. Where {Related_Contact_First_Name} will be replaced with the chosen related contact individual's first name related to the client, and {Period} will be replaced with 'month starting on dd-mm-yyyy' or 'week starting on dd-mm-yyyy' depending on the chosen schedule period of invoices.">
                    <img src="/src/assets/info-circle.svg">
                </span>
            </div>
        </div>
        <hr class="w-100 my-3">
        <h5>Please fill in the email template you want to use for sending automated invoice reminders:</h5>
        <div class="row mb-3">
            <label for="EmailSubjectInputInvoice2" class="form-label">Subject</label>
            <div class="col-11">
                <input type="text" class="form-control" id="EmailSubjectInputInvoice2" placeholder="Invoice Reminder Example" v-model="EmailInvoiceReminder.Subject">
            </div>
            <div class="col-1">
                <span class="d-inline-block" tabindex="0" data-bs-toggle="popover" data-bs-trigger="hover focus" data-bs-content="This field acceps the following placeholders inside the { } brackets: {Client_First_Name}, {Client_Last_Name}, {Period}, {Related_Contact_First_Name}, {Related_Contact_Last_Name}, {Related_Contact_Company_Name}. In order for the related contacts placeholders to be replaced, you have to choose them to be used for templates on the client information page. An example of using this is: Dear {Related_Contact_First_Name}, {Client_First_Name} {Client_Last_Name} received an invoice from Example Ltd for the period of {Period}. Where {Related_Contact_First_Name} will be replaced with the chosen related contact individual's first name related to the client, and {Period} will be replaced with 'month starting on dd-mm-yyyy' or 'week starting on dd-mm-yyyy' depending on the chosen schedule period of invoices.">
                    <img src="/src/assets/info-circle.svg">
                </span>
            </div>
        </div>
        <div class="row mb-3">
            <label for="EmailBodyInputInvoice2" class="form-label">Body</label>
            <div class="col-11">
                <textarea class="form-control" id="EmailBodyInvoice2" rows="5" v-model="EmailInvoiceReminder.Body"></textarea>
            </div>
            <div class="col-1">
                <span class="d-inline-block" tabindex="0" data-bs-toggle="popover" data-bs-trigger="hover focus" data-bs-content="This field acceps the following placeholders inside the { } brackets: {Client_First_Name}, {Client_Last_Name}, {Period}, {Related_Contact_First_Name}, {Related_Contact_Last_Name}, {Related_Contact_Company_Name}. In order for the related contacts placeholders to be replaced, you have to choose them to be used for templates on the client information page. An example of using this is: Dear {Related_Contact_First_Name}, {Client_First_Name} {Client_Last_Name} received an invoice from Example Ltd for the period of {Period}. Where {Related_Contact_First_Name} will be replaced with the chosen related contact individual's first name related to the client, and {Period} will be replaced with 'month starting on dd-mm-yyyy' or 'week starting on dd-mm-yyyy' depending on the chosen schedule period of invoices.">
                    <img src="/src/assets/info-circle.svg">
                </span>
            </div>
        </div>
        <div class="d-grid gap-2">
            <button type="button" class="btn btn-success" @click="save()" :disabled="!form_chage()">Save</button>
        </div>
    </form>

    <!-- Modal for the placeholders and successful file upload confirmation -->
    <div class="modal fade" ref='placeholdersconfirmationmodal'id="staticBackdrop" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 v-if="FileName && placeholders" class="modal-title fs-5" id="staticBackdroplabel">File upload successful!</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="closeModal"></button>
                </div>
                <div class="modal-body">
                    <div v-if="FileName && placeholders">
                        <h5>The following placeholders were detected in the contract template:</h5>
                        <p>{{ placeholders }}</p>
                    </div>
                    <div v-if="FileInvoiceName && placeholdersInvoice">
                        <h5>The following placeholders were detected in the invoice template:</h5>
                        <p>{{ placeholdersInvoice }}</p>
                    </div>
                    <div v-if="PlaceholdersEmailSubjectforDocuSign">
                        <h5>The following placeholders were detected in the email subject template that will be used for sending contracts through DocuSign:</h5>
                        <p>{{ PlaceholdersEmailSubjectforDocuSign }}</p>
                    </div>
                    <div v-if="PlaceholdersEmailInvoiceWithoutContract.Subject">
                        <h5>The following placeholders were detected in the subject of the email template that will be used for sending one off invoices without a contract:</h5>
                        <p>{{ PlaceholdersEmailInvoiceWithoutContract.Subject }}</p>
                    </div>
                    <div v-if="PlaceholdersEmailInvoiceWithoutContract.Body">
                        <h5>The following placeholders were detected in the body of the email template that will be used for sending one off invoices without a contract:</h5>
                        <p>{{ PlaceholdersEmailInvoiceWithoutContract.Body }}</p>
                    </div>
                    <div v-if="PlaceholdersEmailInvoiceOnlyOneWithContract.Subject">
                        <h5>The following placeholders were detected in the subject of the email template that will be used for sending first invoice after contract if the invoice isn't broken into multiple invoices:</h5>
                        <p>{{ PlaceholdersEmailInvoiceOnlyOneWithContract.Subject }}</p>
                    </div>
                    <div v-if="PlaceholdersEmailInvoiceOnlyOneWithContract.Body">
                        <h5>The following placeholders were detected in the body of the email template that will be used for sending first invoice after contract if the invoice isn't broken into multiple invoices:</h5>
                        <p>{{ PlaceholdersEmailInvoiceOnlyOneWithContract.Body }}</p>
                    </div>
                    <div v-if="PlaceholdersEmailInvoiceFirstWithContract.Subject">
                        <h5>The following placeholders were detcted in the subject of the email template that will be used for sending first invoice after contract if it's broken into multiple invoices:</h5>
                        <p>{{ PlaceholdersEmailInvoiceFirstWithContract.Subject }}</p>
                    </div>
                    <div v-if="PlaceholdersEmailInvoiceFirstWithContract.Body">
                        <h5>The following placeholders were detected in the body of the email template that will be used for sending first invoice after contract if it's broken into multiple invoices:</h5>
                        <p>{{ PlaceholdersEmailInvoiceFirstWithContract.Body }}</p>
                    </div>
                    <div v-if="PlaceholdersEmailInvoiceOtherInvoicesWithContract.Subject">
                        <h5>The following placeholders were detected in the subject of the email template that will be used for sending invoices relating to a contract after the first invoice:</h5>
                        <p>{{ PlaceholdersEmailInvoiceOtherInvoicesWithContract.Subject }}</p>
                    </div>
                    <div v-if="PlaceholdersEmailInvoiceOtherInvoicesWithContract.Body">
                        <h5>The following placeholders were detected in the body of the email template that will be used for sending invoices relating to a contract after the first invoice:</h5>
                        <p>{{ PlaceholdersEmailInvoiceOtherInvoicesWithContract.Body }}</p>
                    </div>
                    <div v-if="PlaceholdersEmailInvoiceReminder.Subject">
                        <h5>The following placeholders were detcted in the subject of the email template that will be used for sending automated invoice reminders:</h5>
                        <p>{{ PlaceholdersEmailInvoiceReminder.Subject }}</p>
                    </div>
                    <div v-if="PlaceholdersEmailInvoiceReminder.Body">
                        <h5>The following placeholders were detcted in the body of the email template that will be used for sending automated invoice reminders:</h5>
                        <p>{{ PlaceholdersEmailInvoiceReminder.Body }}</p>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="closeModal">Close</button>
                    <button type="button" class="btn btn-primary" @click="closeModal">Understood</button>
                </div>
            </div>
        </div>
    </div>

</template>
    
<script lang="ts">
import { defineComponent } from "vue";
import { nextTick } from 'vue';
import { Modal } from 'bootstrap';
import { Popover } from 'bootstrap';
import { RouterView } from "vue-router";
import {CookieHandle} from '@/utils.js';
const baseUrl = `${import.meta.env.VITE_API_URL}/main`;


export default defineComponent({
    data() {
        return {
            EmailSubjectforDocuSign: '',
            OriginalSubjectforDocuSign: '',
            EmailInvoiceWithoutContract: {
                Subject: '',
                Body: '',
            },
            OriginalEmailInvoiceWithoutContract: {
                Subject: '',
                Body: '',
            },
            EmailInvoiceOnlyOneWithContract: {
                Subject: '',
                Body: '',
            },
            OriginalEmailInvoiceOnlyOneWithContract: {
                Subject: '',
                Body: '',
            },
            EmailInvoiceFirstWithContract: {
                Subject: '',
                Body: '',
            },
            OriginalEmailInvoiceFirstWithContract: {
                Subject: '',
                Body: '',
            },
            EmailInvoiceOtherInvoicesWithContract: {
                Subject: '',
                Body: '',
            },
            OriginalEmailInvoiceOtherInvoicesWithContract: {
                Subject: '',
                Body: '',
            },
            EmailInvoiceReminder: {
                Subject: '',
                Body: '',
            },
            OriginalEmailInvoiceReminder: {
                Subject: '',
                Body: '',
            },
            file: null,
            FileName: null,
            fileInvoice: null,
            FileInvoiceName: null,
            placeholders: [],
            placeholdersInvoice: [],
            bootstrapModal: null,
            handleATagLinkBound: null,
            currentPopoverTrigger: null,
            loading: true,
            PlaceholdersEmailInvoiceWithoutContract: {
                Subject: [],
                Body: [],
            },
            PlaceholdersEmailInvoiceFirstWithContract: {
                Subject: [],
                Body: [],
            },
            PlaceholdersEmailInvoiceOtherInvoicesWithContract: {
                Subject: [],
                Body: [],
            },
            PlaceholdersEmailInvoiceReminder: {
                Subject: [],
                Body: [],
            },
            PlaceholdersEmailInvoiceOnlyOneWithContract: {
                Subject: [],
                Body: [],
            },
            PlaceholdersEmailSubjectforDocuSign: [],
        };
    },
    async mounted() {
        const csrftoken = CookieHandle('csrftoken');
        //initialises bootstrap popovers
        const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
        const popoverList = [...popoverTriggerList].map((popoverTriggerEl) => new Popover(popoverTriggerEl))

        const response1 = await fetch(`${baseUrl}/api/EmailInvoiceWithoutContract/`,{
            method: 'GET',
            headers: {
                'Url-Header': window.location.href,
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            credentials: 'include',
        })
        if (response1.status === 200) {
            const data1 = await response1.json();
            this.EmailInvoiceWithoutContract = data1;
            this.OriginalEmailInvoiceWithoutContract = JSON.parse(JSON.stringify(data1));
        } else {
            this.EmailInvoiceWithoutContract = {
                Subject: '',
                Body: '',
            };
            this.OriginalEmailInvoiceWithoutContract = {
                Subject: '',
                Body: '',
            }
        }

        const response2 = await fetch(`${baseUrl}/api/EmailInvoiceFirstWithContract/`,{
            method: 'GET',
            headers: {
                'Url-Header': window.location.href,
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            credentials: 'include',
        })
        if (response2.status === 200) {
            const data2 = await response2.json();
            this.EmailInvoiceFirstWithContract = data2;
            this.OriginalEmailInvoiceFirstWithContract = JSON.parse(JSON.stringify(data2));
        } else {
            this.EmailInvoiceFirstWithContract = {
                Subject: '',
                Body: '',
            };
            this.OriginalEmailInvoiceFirstWithContract = {
                Subject: '',
                Body: '',
            }
        }

        const response3 = await fetch(`${baseUrl}/api/EmailInvoiceOtherInvoicesWithContract/`,{
            method: 'GET',
            headers: {
                'Url-Header': window.location.href,
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            credentials: 'include',
        })
        if (response3.status === 200) {
            const data3 = await response3.json();
            this.EmailInvoiceOtherInvoicesWithContract = data3;
            this.OriginalEmailInvoiceOtherInvoicesWithContract = JSON.parse(JSON.stringify(data3));
        } else {
            this.EmailInvoiceOtherInvoicesWithContract = {
                Subject: '',
                Body: '',
            };
            this.OriginalEmailInvoiceOtherInvoicesWithContract = {
                Subject: '',
                Body: '',
            }
        }

        const response4 = await fetch(`${baseUrl}/api/EmailInvoiceReminder/`,{
            method: 'GET',
            headers: {
                'Url-Header': window.location.href,
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            credentials: 'include',
        })
        if (response4.status === 200) {
            const data4 = await response4.json();
            this.EmailInvoiceReminder = data4;
            this.OriginalEmailInvoiceReminder = JSON.parse(JSON.stringify(data4));
        } else {
            this.EmailInvoiceReminder = {
                Subject: '',
                Body: '',
            };
            this.OriginalEmailInvoiceReminder = {
                Subject: '',
                Body: '',
            }
        }

        const response5 = await fetch(`${baseUrl}/api/EmailInvoiceOnlyOneWithContract/`,{
            method: 'GET',
            headers: {
                'Url-Header': window.location.href,
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            credentials: 'include',
        })
        if (response5.status === 200) {
            const data5 = await response5.json();
            this.EmailInvoiceOnlyOneWithContract = data5;
            this.OriginalEmailInvoiceOnlyOneWithContract = JSON.parse(JSON.stringify(data5));
        } else {
            this.EmailInvoiceOnlyOneWithContract = {
                Subject: '',
                Body: '',
            };
            this.OriginalEmailInvoiceOnlyOneWithContract = {
                Subject: '',
                Body: '',
            }
        }

        const response8 = await fetch(`${baseUrl}/api/EmailSubjectforDocuSign/`, {
            method: 'GET',
            headers: {
                'Url-Header': window.location.href,
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            credentials: 'include',
        })
        if (response8.status === 200) {
            const data8 = await response8.json();
            this.EmailSubjectforDocuSign = data8.Subject;
            this.OriginalSubjectforDocuSign = JSON.parse(JSON.stringify(data8.Subject));
        } else {
            this.EmailSubjectforDocuSign = '';
            this.OriginalSubjectforDocuSign = '';
        }

        const response6 = await fetch(`${baseUrl}/api/contract-upload/`, {
            method: "GET",
            headers: {
                'Url-Header': window.location.href,
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            credentials: 'include'
        });
        if (response6.status === 200) {
            const data6 = await response6.json();
            this.FileName = data6.FileName;
        }
        this.bootstrapModal = new Modal(this.$refs.placeholdersconfirmationmodal);

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
        this.bootstrapModal = new Modal(this.$refs.placeholdersconfirmationmodal);
        this.loading = false;
    },
    methods: {
        //This function gets the selected file from the input type="file" and assigns it to the file component
        handleFileContract(event) {
            //Gets the selected file from the input type="file"
            //target.files returns of list of selected files through the event passed automatically from input type="file" so I need to get the first element of that array as its just one file and thats the one I need
            this.file = event.target.files[0];
        },
        //This function gets the selected file from the input type="file" and assigns it to the fileInvoice component
        handleFileInvoice(event) {
            //Gets the selected file from the input type="file"
            //target.files returns of list of selected files through the event passed automatically from input type="file" so I need to get the first element of that array as its just one file and thats the one I need
            this.fileInvoice = event.target.files[0];
        },
        openModal() {
            if (!this.bootstrapModal) {
                this.bootstrapModal = new Modal(this.$refs.placeholdersconfirmationmodal);
            }
            this.bootstrapModal.show();
        },
        closeModal() {
            if (this.bootstrapModal) {
                this.bootstrapModal.hide();
            }
        },
        async save(){
            const csrftoken = CookieHandle('csrftoken');
            if (JSON.stringify(this.EmailInvoiceWithoutContract) !== JSON.stringify(this.OriginalEmailInvoiceWithoutContract)){
                if ((this.EmailInvoiceWithoutContract.Subject === '' && this.EmailInvoiceWithoutContract.Body === '') && (this.OriginalEmailInvoiceWithoutContract.Subject !== '' || this.OriginalEmailInvoiceWithoutContract.Body !== '')){
                    await fetch(`${baseUrl}/api/EmailInvoiceWithoutContract/`, {
                        method: 'DELETE',
                        headers: {
                            'Url-Header': window.location.href,
                            "Content-Type": "application/json",
                            'X-CSRFToken': csrftoken
                        },
                        credentials: 'include',
                    });
                    this.OriginalEmailInvoiceWithoutContract.Subject = JSON.parse(JSON.stringify(this.EmailInvoiceWithoutContract.Subject));
                    this.OriginalEmailInvoiceWithoutContract.Body = JSON.parse(JSON.stringify(this.EmailInvoiceWithoutContract.Body));
                } else if ((this.EmailInvoiceWithoutContract.Subject !== '' || this.EmailInvoiceWithoutContract.Body !== '') && (this.OriginalEmailInvoiceWithoutContract.Subject !== '' || this.OriginalEmailInvoiceWithoutContract.Body !== '')) {
                    const response = await fetch(`${baseUrl}/api/EmailInvoiceWithoutContract/`, {
                        method: 'PUT',
                        headers: {
                            'Url-Header': window.location.href,
                            "Content-Type": "application/json",
                            'X-CSRFToken': csrftoken
                        
                        },
                        body: JSON.stringify(this.EmailInvoiceWithoutContract),
                        credentials: 'include',
                    });
                    const data = await response.json();
                    this.PlaceholdersEmailInvoiceWithoutContract.Subject = data.Confirmation_Placeholders_in_Subject;
                    this.PlaceholdersEmailInvoiceWithoutContract.Body = data.Confirmation_Placeholders_in_Body;
                    this.EmailInvoiceWithoutContract.Subject = data.email_template.Subject;
                    this.EmailInvoiceWithoutContract.Body = data.email_template.Body;
                    this.OriginalEmailInvoiceWithoutContract.Subject = JSON.parse(JSON.stringify(this.EmailInvoiceWithoutContract.Subject));
                    this.OriginalEmailInvoiceWithoutContract.Body = JSON.parse(JSON.stringify(this.EmailInvoiceWithoutContract.Body));
                    this.bootstrapModal.show();
                } else if ((this.EmailInvoiceWithoutContract.Subject !=='' || this.EmailInvoiceWithoutContract.Body !== '') && (this.OriginalEmailInvoiceWithoutContract.Subject === '' && this.OriginalEmailInvoiceWithoutContract.Body === '')){
                    const response = await fetch(`${baseUrl}/api/EmailInvoiceWithoutContract/`, {
                        method: 'POST',
                        headers: {
                            'Url-Header': window.location.href,
                            "Content-Type": "application/json",
                            'X-CSRFToken': csrftoken
                        },
                        body: JSON.stringify(this.EmailInvoiceWithoutContract),
                        credentials: 'include',
                    });
                    const data = await response.json();
                    this.PlaceholdersEmailInvoiceWithoutContract.Subject = data.Confirmation_Placeholders_in_Subject;
                    this.PlaceholdersEmailInvoiceWithoutContract.Body = data.Confirmation_Placeholders_in_Body;
                    this.EmailInvoiceWithoutContract.Subject = data.email_template.Subject;
                    this.EmailInvoiceWithoutContract.Body = data.email_template.Body;
                    this.OriginalEmailInvoiceWithoutContract.Subject = JSON.parse(JSON.stringify(this.EmailInvoiceWithoutContract.Subject));
                    this.OriginalEmailInvoiceWithoutContract.Body = JSON.parse(JSON.stringify(this.EmailInvoiceWithoutContract.Body));
                    this.bootstrapModal.show();
                }
            }
            if (JSON.stringify(this.EmailInvoiceFirstWithContract) !== JSON.stringify(this.OriginalEmailInvoiceFirstWithContract)){
                if ((this.EmailInvoiceFirstWithContract.Subject === '' && this.EmailInvoiceFirstWithContract.Body === '') && (this.OriginalEmailInvoiceFirstWithContract.Subject !== '' || this.OriginalEmailInvoiceFirstWithContract.Body !== '')){
                    await fetch(`${baseUrl}/api/EmailInvoiceFirstWithContract/`, {
                        method: 'DELETE',
                        headers: {
                            'Url-Header': window.location.href,
                            "Content-Type": "application/json",
                            'X-CSRFToken': csrftoken
                        },
                        credentials: 'include',
                    });
                    this.OriginalEmailInvoiceFirstWithContract.Subject = JSON.parse(JSON.stringify(this.EmailInvoiceFirstWithContract.Subject));
                    this.OriginalEmailInvoiceFirstWithContract.Body = JSON.parse(JSON.stringify(this.EmailInvoiceFirstWithContract.Body));
                } else if ((this.EmailInvoiceFirstWithContract.Subject !== '' || this.EmailInvoiceFirstWithContract.Body !== '') && (this.OriginalEmailInvoiceFirstWithContract.Subject !== '' || this.OriginalEmailInvoiceFirstWithContract.Body !== '')) {
                    const response = await fetch(`${baseUrl}/api/EmailInvoiceFirstWithContract/`, {
                        method: 'PUT',
                        headers: {
                            'Url-Header': window.location.href,
                            "Content-Type": "application/json",
                            'X-CSRFToken': csrftoken
                        },
                        body: JSON.stringify(this.EmailInvoiceFirstWithContract),
                        credentials: 'include',
                    });
                    const data = await response.json();
                    this.PlaceholdersEmailInvoiceFirstWithContract.Subject = data.Confirmation_Placeholders_in_Subject;
                    this.PlaceholdersEmailInvoiceFirstWithContract.Body = data.Confirmation_Placeholders_in_Body;
                    this.EmailInvoiceFirstWithContract.Subject = data.email_template.Subject;
                    this.EmailInvoiceFirstWithContract.Body = data.email_template.Body;
                    this.OriginalEmailInvoiceFirstWithContract.Subject = JSON.parse(JSON.stringify(this.EmailInvoiceFirstWithContract.Subject));
                    this.OriginalEmailInvoiceFirstWithContract.Body = JSON.parse(JSON.stringify(this.EmailInvoiceFirstWithContract.Body));
                    this.bootstrapModal.show();
                } else if ((this.EmailInvoiceFirstWithContract.Subject !=='' || this.EmailInvoiceFirstWithContract.Body !== '') && (this.OriginalEmailInvoiceFirstWithContract.Subject === '' && this.OriginalEmailInvoiceFirstWithContract.Body === '')){
                    const response = await fetch(`${baseUrl}/api/EmailInvoiceFirstWithContract/`, {
                        method: 'POST',
                        headers: {
                            'Url-Header': window.location.href,
                            "Content-Type": "application/json",
                            'X-CSRFToken': csrftoken
                        },
                        body: JSON.stringify(this.EmailInvoiceFirstWithContract),
                        credentials: 'include',
                    });
                    const data = await response.json();
                    this.PlaceholdersEmailInvoiceFirstWithContract.Subject = data.Confirmation_Placeholders_in_Subject;
                    this.PlaceholdersEmailInvoiceFirstWithContract.Body = data.Confirmation_Placeholders_in_Body;
                    this.EmailInvoiceFirstWithContract.Subject = data.email_template.Subject;
                    this.EmailInvoiceFirstWithContract.Body = data.email_template.Body;
                    this.OriginalEmailInvoiceFirstWithContract.Subject = JSON.parse(JSON.stringify(this.EmailInvoiceFirstWithContract.Subject));
                    this.OriginalEmailInvoiceFirstWithContract.Body = JSON.parse(JSON.stringify(this.EmailInvoiceFirstWithContract.Body));
                    this.bootstrapModal.show();
                }
            }
            if (JSON.stringify(this.EmailInvoiceOtherInvoicesWithContract) !== JSON.stringify(this.OriginalEmailInvoiceOtherInvoicesWithContract)){
                if ((this.EmailInvoiceOtherInvoicesWithContract.Subject === '' && this.EmailInvoiceOtherInvoicesWithContract.Body === '') && (this.OriginalEmailInvoiceOtherInvoicesWithContract.Subject !== '' || this.OriginalEmailInvoiceOtherInvoicesWithContract.Body !== '')){
                    await fetch(`${baseUrl}/api/EmailInvoiceOtherInvoicesWithContract/`, {
                        method: 'DELETE',
                        headers: {
                            'Url-Header': window.location.href,
                            "Content-Type": "application/json",
                            'X-CSRFToken': csrftoken
                        },
                        credentials: 'include',
                    });
                    this.OriginalEmailInvoiceOtherInvoicesWithContract.Subject = JSON.parse(JSON.stringify(this.EmailInvoiceOtherInvoicesWithContract.Subject));
                    this.OriginalEmailInvoiceOtherInvoicesWithContract.Body = JSON.parse(JSON.stringify(this.EmailInvoiceOtherInvoicesWithContract.Body));
                } else if ((this.EmailInvoiceOtherInvoicesWithContract.Subject !== '' || this.EmailInvoiceOtherInvoicesWithContract.Body !== '') && (this.OriginalEmailInvoiceOtherInvoicesWithContract.Subject !== '' || this.OriginalEmailInvoiceOtherInvoicesWithContract.Body !== '')) {
                    const response = await fetch(`${baseUrl}/api/EmailInvoiceOtherInvoicesWithContract/`, {
                        method: 'PUT',
                        headers: {
                            'Url-Header': window.location.href,
                            "Content-Type": "application/json",
                            'X-CSRFToken': csrftoken
                        },
                        body: JSON.stringify(this.EmailInvoiceOtherInvoicesWithContract),
                        credentials: 'include',
                    });
                    const data = await response.json();
                    this.PlaceholdersEmailInvoiceOtherInvoicesWithContract.Subject = data.Confirmation_Placeholders_in_Subject;
                    this.PlaceholdersEmailInvoiceOtherInvoicesWithContract.Body = data.Confirmation_Placeholders_in_Body;
                    this.EmailInvoiceOtherInvoicesWithContract.Subject = data.email_template.Subject;
                    this.EmailInvoiceOtherInvoicesWithContract.Body = data.email_template.Body;
                    this.OriginalEmailInvoiceOtherInvoicesWithContract.Subject = JSON.parse(JSON.stringify(this.EmailInvoiceOtherInvoicesWithContract.Subject));
                    this.OriginalEmailInvoiceOtherInvoicesWithContract.Body = JSON.parse(JSON.stringify(this.EmailInvoiceOtherInvoicesWithContract.Body));
                    this.bootstrapModal.show();
                } else if ((this.EmailInvoiceOtherInvoicesWithContract.Subject !=='' || this.EmailInvoiceOtherInvoicesWithContract.Body !== '') && (this.OriginalEmailInvoiceOtherInvoicesWithContract.Subject === '' && this.OriginalEmailInvoiceOtherInvoicesWithContract.Body === '')){
                    const response = await fetch(`${baseUrl}/api/EmailInvoiceOtherInvoicesWithContract/`, {
                        method: 'POST',
                        headers: {
                            'Url-Header': window.location.href,
                            "Content-Type": "application/json",
                            'X-CSRFToken': csrftoken
                        },
                        body: JSON.stringify(this.EmailInvoiceOtherInvoicesWithContract),
                        credentials: 'include',
                    });
                    const data = await response.json();
                    this.PlaceholdersEmailInvoiceOtherInvoicesWithContract.Subject = data.Confirmation_Placeholders_in_Subject;
                    this.PlaceholdersEmailInvoiceOtherInvoicesWithContract.Body = data.Confirmation_Placeholders_in_Body;
                    this.EmailInvoiceOtherInvoicesWithContract.Subject = data.email_template.Subject;
                    this.EmailInvoiceOtherInvoicesWithContract.Body = data.email_template.Body;
                    this.OriginalEmailInvoiceOtherInvoicesWithContract.Subject = JSON.parse(JSON.stringify(this.EmailInvoiceOtherInvoicesWithContract.Subject));
                    this.OriginalEmailInvoiceOtherInvoicesWithContract.Body = JSON.parse(JSON.stringify(this.EmailInvoiceOtherInvoicesWithContract.Body));
                    this.bootstrapModal.show();
                }
            }
            if (JSON.stringify(this.EmailInvoiceReminder) !== JSON.stringify(this.OriginalEmailInvoiceReminder)){
                if ((this.EmailInvoiceReminder.Subject === '' && this.EmailInvoiceReminder.Body === '') && (this.OriginalEmailInvoiceReminder.Subject !== '' || this.OriginalEmailInvoiceReminder.Body !== '')){
                    await fetch(`${baseUrl}/api/EmailInvoiceReminder/`, {
                        method: 'DELETE',
                        headers: {
                            'Url-Header': window.location.href,
                            "Content-Type": "application/json",
                            'X-CSRFToken': csrftoken
                        },
                        credentials: 'include',
                    });
                    this.OriginalEmailInvoiceReminder.Subject = JSON.parse(JSON.stringify(this.EmailInvoiceReminder.Subject));
                    this.OriginalEmailInvoiceReminder.Body = JSON.parse(JSON.stringify(this.EmailInvoiceReminder.Body));
                } else if ((this.EmailInvoiceReminder.Subject !== '' || this.EmailInvoiceReminder.Body !== '') && (this.OriginalEmailInvoiceReminder.Subject !== '' || this.OriginalEmailInvoiceReminder.Body !== '')) {
                    const response = await fetch(`${baseUrl}/api/EmailInvoiceReminder/`, {
                        method: 'PUT',
                        headers: {
                            'Url-Header': window.location.href,
                            "Content-Type": "application/json",
                            'X-CSRFToken': csrftoken
                        },
                        body: JSON.stringify(this.EmailInvoiceReminder),
                        credentials: 'include',
                    });
                    const data = await response.json();
                    this.PlaceholdersEmailInvoiceReminder.Subject = data.Confirmation_Placeholders_in_Subject;
                    this.PlaceholdersEmailInvoiceReminder.Body = data.Confirmation_Placeholders_in_Body;
                    this.EmailInvoiceReminder.Subject = data.email_template.Subject;
                    this.EmailInvoiceReminder.Body = data.email_template.Body;
                    this.OriginalEmailInvoiceReminder.Subject = JSON.parse(JSON.stringify(this.EmailInvoiceReminder.Subject));
                    this.OriginalEmailInvoiceReminder.Body = JSON.parse(JSON.stringify(this.EmailInvoiceReminder.Body));
                    this.bootstrapModal.show();
                } else if ((this.EmailInvoiceReminder.Subject !=='' || this.EmailInvoiceReminder.Body !== '') && (this.OriginalEmailInvoiceReminder.Subject === '' && this.OriginalEmailInvoiceReminder.Body === '')){
                    const response = await fetch(`${baseUrl}/api/EmailInvoiceReminder/`, {
                        method: 'POST',
                        headers: {
                            'Url-Header': window.location.href,
                            "Content-Type": "application/json",
                            'X-CSRFToken': csrftoken
                        },
                        body: JSON.stringify(this.EmailInvoiceReminder),
                        credentials: 'include',
                    });
                    const data = await response.json();
                    this.PlaceholdersEmailInvoiceReminder.Subject = data.Confirmation_Placeholders_in_Subject;
                    this.PlaceholdersEmailInvoiceReminder.Body = data.Confirmation_Placeholders_in_Body;
                    this.EmailInvoiceReminder.Subject = data.email_template.Subject;
                    this.EmailInvoiceReminder.Body = data.email_template.Body;
                    this.OriginalEmailInvoiceReminder.Subject = JSON.parse(JSON.stringify(this.EmailInvoiceReminder.Subject));
                    this.OriginalEmailInvoiceReminder.Body = JSON.parse(JSON.stringify(this.EmailInvoiceReminder.Body));
                    this.bootstrapModal.show();
                }
            }
            if (JSON.stringify(this.EmailInvoiceOnlyOneWithContract) !== JSON.stringify(this.OriginalEmailInvoiceOnlyOneWithContract)){
                if ((this.EmailInvoiceOnlyOneWithContract.Subject === '' && this.EmailInvoiceOnlyOneWithContract.Body === '') && (this.OriginalEmailInvoiceOnlyOneWithContract.Subject !== '' || this.OriginalEmailInvoiceOnlyOneWithContract.Body !== '')){
                    await fetch(`${baseUrl}/api/EmailInvoiceOnlyOneWithContract/`, {
                        method: 'DELETE',
                        headers: {
                            'Url-Header': window.location.href,
                            "Content-Type": "application/json",
                            'X-CSRFToken': csrftoken
                        },
                        credentials: 'include',
                    });
                    this.OriginalEmailInvoiceOnlyOneWithContract.Subject = JSON.parse(JSON.stringify(this.EmailInvoiceOnlyOneWithContract.Subject));
                    this.OriginalEmailInvoiceOnlyOneWithContract.Body = JSON.parse(JSON.stringify(this.EmailInvoiceOnlyOneWithContract.Body));
                } else if ((this.EmailInvoiceOnlyOneWithContract.Subject !== '' || this.EmailInvoiceOnlyOneWithContract.Body !== '') && (this.OriginalEmailInvoiceOnlyOneWithContract.Subject !== '' || this.OriginalEmailInvoiceOnlyOneWithContract.Body !== '')) {
                    const response = await fetch(`${baseUrl}/api/EmailInvoiceOnlyOneWithContract/`, {
                        method: 'PUT',
                        headers: {
                            'Url-Header': window.location.href,
                            "Content-Type": "application/json",
                            'X-CSRFToken': csrftoken
                        },
                        body: JSON.stringify(this.EmailInvoiceOnlyOneWithContract),
                        credentials: 'include',
                    });
                    const data = await response.json();
                    this.PlaceholdersEmailInvoiceOnlyOneWithContract.Subject = data.Confirmation_Placeholders_in_Subject;
                    this.PlaceholdersEmailInvoiceOnlyOneWithContract.Body = data.Confirmation_Placeholders_in_Body;
                    this.EmailInvoiceOnlyOneWithContract.Subject = data.email_template.Subject;
                    this.EmailInvoiceOnlyOneWithContract.Body = data.email_template.Body;
                    this.OriginalEmailInvoiceOnlyOneWithContract.Subject = JSON.parse(JSON.stringify(this.EmailInvoiceOnlyOneWithContract.Subject));
                    this.OriginalEmailInvoiceOnlyOneWithContract.Body = JSON.parse(JSON.stringify(this.EmailInvoiceOnlyOneWithContract.Body));
                    this.bootstrapModal.show();
                } else if ((this.EmailInvoiceOnlyOneWithContract.Subject !=='' || this.EmailInvoiceOnlyOneWithContract.Body !== '') && (this.OriginalEmailInvoiceOnlyOneWithContract.Subject === '' && this.OriginalEmailInvoiceOnlyOneWithContract.Body === '')){
                    const response = await fetch(`${baseUrl}/api/EmailInvoiceOnlyOneWithContract/`, {
                        method: 'POST',
                        headers: {
                            'Url-Header': window.location.href,
                            "Content-Type": "application/json",
                            'X-CSRFToken': csrftoken
                        },
                        body: JSON.stringify(this.EmailInvoiceOnlyOneWithContract),
                        credentials: 'include',
                    });
                    const data = await response.json();
                    this.PlaceholdersEmailInvoiceOnlyOneWithContract.Subject = data.Confirmation_Placeholders_in_Subject;
                    this.PlaceholdersEmailInvoiceOnlyOneWithContract.Body = data.Confirmation_Placeholders_in_Body;
                    this.EmailInvoiceOnlyOneWithContract.Subject = data.email_template.Subject;
                    this.EmailInvoiceOnlyOneWithContract.Body = data.email_template.Body;
                    this.OriginalEmailInvoiceOnlyOneWithContract.Subject = JSON.parse(JSON.stringify(this.EmailInvoiceOnlyOneWithContract.Subject));
                    this.OriginalEmailInvoiceOnlyOneWithContract.Body = JSON.parse(JSON.stringify(this.EmailInvoiceOnlyOneWithContract.Body));
                    this.bootstrapModal.show();
                }
            }
            if (JSON.stringify(this.EmailSubjectforDocuSign) !== JSON.stringify(this.OriginalSubjectforDocuSign)){
                if ((this.EmailSubjectforDocuSign === '' && this.OriginalSubjectforDocuSign !== '')){
                    await fetch(`${baseUrl}/api/EmailSubjectforDocuSign/`, {
                        method: 'DELETE',
                        headers: {
                            'Url-Header': window.location.href,
                            "Content-Type": "application/json",
                            'X-CSRFToken': csrftoken
                        },
                        body: JSON.stringify(this.EmailSubjectforDocuSign),
                        credentials: 'include',
                    });
                    this.OriginalSubjectforDocuSign = JSON.parse(JSON.stringify(this.EmailSubjectforDocuSign));
                } else if ((this.EmailSubjectforDocuSign !== '' && this.OriginalSubjectforDocuSign !== '')) {
                    const response = await fetch(`${baseUrl}/api/EmailSubjectforDocuSign/`, {
                        method: 'PUT',
                        headers: {
                            'Url-Header': window.location.href,
                            "Content-Type": "application/json",
                            'X-CSRFToken': csrftoken
                        },
                        body: JSON.stringify(this.EmailSubjectforDocuSign),
                        credentials: 'include',
                    });
                    const data = await response.json();
                    this.PlaceholdersEmailSubjectforDocuSign = data.Confirmation_Placeholders_in_Subject;
                    this.EmailSubjectforDocuSign = data.email_template.Subject;
                    this.OriginalSubjectforDocuSign = JSON.parse(JSON.stringify(this.EmailSubjectforDocuSign));
                    this.bootstrapModal.show();
                } else if ((this.EmailSubjectforDocuSign !== '' && this.OriginalSubjectforDocuSign === '')) {
                    const response = await fetch(`${baseUrl}/api/EmailSubjectforDocuSign/`, {
                        method: 'POST',
                        headers: {
                            'Url-Header': window.location.href,
                            "Content-Type": "application/json",
                            'X-CSRFToken': csrftoken
                        },
                        body: JSON.stringify(this.EmailSubjectforDocuSign),
                        credentials: 'include',
                    });
                    const data = await response.json();
                    this.PlaceholdersEmailSubjectforDocuSign = data.Confirmation_Placeholders_in_Subject;
                    this.EmailSubjectforDocuSign = data.email_template.Subject;
                    this.OriginalSubjectforDocuSign = JSON.parse(JSON.stringify(this.EmailSubjectforDocuSign));
                    this.bootstrapModal.show();
                }
            }
            if (this.file !== null){
                //This FromData() JavaScript function is used to create key value pairs and can handle files as values of keys
                const formData = new FormData();
                //This adds a key "file" and value (the uploaded file to the FormData functio)
                formData.append("file", this.file);
                const response4 = await fetch(`${baseUrl}/api/contract-upload/`, {
                    method: 'POST',
                    headers: {
                        'Url-Header': window.location.href,
                        'X-CSRFToken': csrftoken
                    },
                    //When the FromData is sent in the body of the request, the browser automatically sets a header of this request indicating it to be multipart/form-data which encodes the fiels in the form data (including the file) in the http request
                    //This allows Django to automatically determine what can be done with the request because of the header content type, and hence I can easily retrieve the file from the form-data using the file key (refer to MainApp.views)
                    body: formData,
                    credentials: 'include'
                });
                const data4 = await response4.json();
                this.FileName = data4.FileName;
                this.placeholders = data4.Placeholders;
                this.bootstrapModal.show();
                this.file = null;
            }
            if (this.fileInvoice !== null){
                //This FromData() JavaScript function is used to create key value pairs and can handle files as values of keys
                const formData1 = new FormData();
                //This adds a key "file" and value (the uploaded file to the FormData functio)
                formData1.append("file", this.fileInvoice);
                const response5 = await fetch(`${baseUrl}/api/invoice-upload/`, {
                    method: 'POST',
                    headers: {
                        'Url-Header': window.location.href,
                        'X-CSRFToken': csrftoken
                    },
                    //When the FromData is sent in the body of the request, the browser automatically sets a header of this request indicating it to be multipart/form-data which encodes the fiels in the form data (including the file) in the http request
                    body: formData1,
                    credentials: 'include'
                });
                const data5 = await response5.json();
                this.FileInvoiceName = data5.FileName;
                this.placeholdersInvoice = data5.Placeholders;
                this.bootstrapModal.show();
                this.fileInvoice = null;
            }
        },
        //Function which detects changes made to the form and dynamically enable or disable the save button
        form_chage() {
            if(JSON.stringify(this.EmailInvoiceWithoutContract) !== JSON.stringify(this.OriginalEmailInvoiceWithoutContract) || JSON.stringify(this.EmailInvoiceFirstWithContract) !== JSON.stringify(this.OriginalEmailInvoiceFirstWithContract) || JSON.stringify(this.EmailInvoiceOtherInvoicesWithContract) !== JSON.stringify(this.OriginalEmailInvoiceOtherInvoicesWithContract) || JSON.stringify(this.EmailInvoiceReminder) !== JSON.stringify(this.OriginalEmailInvoiceReminder) || JSON.stringify(this.EmailInvoiceOnlyOneWithContract) !== JSON.stringify(this.OriginalEmailInvoiceOnlyOneWithContract) || JSON.stringify(this.EmailSubjectforDocuSign) !== JSON.stringify(this.OriginalSubjectforDocuSign) || this.file !== null || this.fileInvoice !== null){
                return true
            } else {
                return false
            }
        },
    },
});
</script>
    
<style scoped>
    
</style>