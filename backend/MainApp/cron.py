from MainApp.models import EmailInvoiceWithoutContract_individual, EmailInvoiceFirstWithContract_individual, EmailInvoiceOtherInvoicesWithContract_individual, EmailInvoiceReminder_individual, EmailInvoiceWithoutContract_company, EmailInvoiceFirstWithContract_company, EmailInvoiceOtherInvoicesWithContract_company, EmailInvoiceReminder_company, EmailInvoiceOnlyOneWithContract_company, EmailInvoiceOnlyOneWithContract_individual, Client_Individual, Client_Company, Represents, UploadedInvoiceWordDocumentCompany, UploadedInvoiceWordDocumentIndividual, Contract, Invoice_Summary, InvoiceItem, Invoice, InvoicesToInvoiceItems, ContractItem, ContactsCompaniesToBeTodThrough, ContactsIndividualsToBeTodThrough, ContactsCompaniesToBeCCdThrough, ContactsIndividualsToBeCCdThrough, ContactsCompaniesToBeBccdThrough, ContactsIndividualsToBeBccdThrough, UsersToBeTodThrough, UsersToBeCCdThrough, UsersToBeBccdThrough
from AuthenticationApp.models import CustomUser
from django.core.mail import EmailMessage
from django.db.utils import ProgrammingError, OperationalError
from django.utils import timezone
from datetime import datetime, date, timedelta
import calendar
from MainApp.views import replace_placeholders_invoice, replace_key, ReplacePlaceholdersEmailCompany
from django.contrib.contenttypes.models import ContentType

#Here I created these algorithms triggered by cron jobs to detect invoices that need to be sent on the date these algorithms are triggered by cron jobs which is every day at 9am
#This is the simplest way I could think of doing this
#This file uses standard coding techniques and methods used acess the whole project so if anything gets confusing refer mainly to the MainApp.views file because the code there is commented a lot.

def InvoicesAutomationsTiedtoContract():

    invoice_summary = Invoice_Summary.objects.filter(contract__isnull=False)
    
    for summary in invoice_summary:
        if summary.number_of_invoices != 0:
            current_date = timezone.now().date()
            if summary.schedule == "Monthly":
                if summary.created_at == current_date:
                    continue
                else:
                    if current_date.day != 1:
                        continue
                    else:
                        pass
            elif summary.schedule == "Daily":
                if summary.created_at == current_date:
                    continue
                else:
                    pass
            elif summary.schedule == "Weekly":
                created_week = summary.created_at.isocalendar()[1]
                current_week = current_date.isocalendar()[1]
                created_month = summary.created_at.month
                current_month = current_date.month
                created_year = summary.created_at.year
                current_year = current_date.year
                if created_week == current_week and created_month == current_month and created_year == current_year:
                    continue
                else:
                    if current_date.weekday() == 0:
                        pass
                    else:
                        continue
            elif summary.schedule == "Quarterly":
                created_quarter = (summary.created_at.month -1) // 3 + 1
                current_quarter = (current_date.month - 1) // 3 + 1
                created_year = summary.created_at.year
                current_year = current_date.year
                if created_quarter == current_quarter and created_year == current_year:
                    continue
                else:
                    first_month_of_current_quarter = 3* (current_quarter - 1) + 1
                    if current_date.month == first_month_of_current_quarter and current_date.day == 1:
                        pass
                    else:
                        continue
            elif summary.schedule == "Yearly":
                if summary.created_at.year == current_date.year:
                    continue
                else:
                    if summary.created_at.month == current_date.month and summary.created_at.day == current_date.day or (summary.created_at.month == 2 and summary.created_at.day == 29 and current_date.month == 2 and current_date.day in [28, 29]):
                        pass
                    else:
                        continue
            to = []
            cc = []
            bcc = []
            try:
                contactscompaniestobetod = ContactsCompaniesToBeTodThrough.objects.filter(invoice_summary = summary, workplace = summary.workplace)
            except (ProgrammingError, OperationalError):
                contactscompaniestobetod = []
            try:
                contactscompaniestobeCCd = ContactsCompaniesToBeCCdThrough.objects.filter(invoice_summary = summary, workplace = summary.workplace)
            except (ProgrammingError, OperationalError):
                contactscompaniestobeCCd = []
            try:
                contactscompaniestobeBccd = ContactsCompaniesToBeBccdThrough.objects.filter(invoice_summary = summary, workplace=summary.workplace)
            except (ProgrammingError, OperationalError):
                contactscompaniestobeBccd = []
            try:
                contactsindividualstobetod = ContactsIndividualsToBeTodThrough.objects.filter(invoice_summary = summary, workplace=summary.workplace)
            except (ProgrammingError, OperationalError):
                contactsindividualstobetod = []
            try:
                contactsindividualstobeCCd = ContactsIndividualsToBeCCdThrough.objects.filter(invoice_summary = summary, workplace=summary.workplace)
            except (ProgrammingError, OperationalError):
                contactsindividualstobeCCd = []
            try:
                contactsindividualstobeBccd = ContactsIndividualsToBeBccdThrough.objects.filter(invoice_summary = summary, workplace=summary.workplace)
            except (ProgrammingError, OperationalError):
                contactsindividualstobeBccd = []
            try:
                userstobetod = UsersToBeTodThrough.objects.filter(invoice_summary = summary, workplace = summary.workplace)
            except (ProgrammingError, OperationalError):
                userstobetod = []
            try:
                userstobeCCd = UsersToBeCCdThrough.objects.filter(invoice_summary = summary, workplace = summary.workplace)
            except (ProgrammingError, OperationalError):
                userstobeCCd = []
            try:
                userstobeBccd = UsersToBeBccdThrough.objects.filter(invoice_summary = summary, workplace = summary.workplace)
            except (ProgrammingError, OperationalError):
                userstobeBccd = []

            if contactscompaniestobetod:
                for contact in contactscompaniestobetod:
                    email = contact.client_company.email
                    to.append(email)
            if contactscompaniestobeCCd:
                for contact in contactscompaniestobeCCd:
                    email = contact.client_company.email
                    cc.append(email)
            if contactscompaniestobeBccd:
                for contact in contactscompaniestobeBccd:
                    email = contact.client_company.email
                    bcc.append(email)
            if contactsindividualstobetod:
                for contact in contactsindividualstobetod:
                    email = contact.client_individual.email
                    to.append(email)
            if contactsindividualstobeCCd:
                for contact in contactsindividualstobeCCd:
                    email = contact.client_individual.email
                    cc.append(email)
            if contactsindividualstobeBccd:
                for contact in contactsindividualstobeBccd:
                    email = contact.client_individual.email
                    bcc.append(email)
            if userstobetod:
                for user in userstobetod:
                    email = user.user.email
                    to.append(email)
            if userstobeCCd:
                for user in userstobeCCd:
                    email = user.user.email
                    cc.append(email)
            if userstobeBccd:
                for user in userstobeBccd:
                    email = user.user.email
                    bcc.append(email)

            if summary.MainClientToBeTod:
                if summary.billed_to_company:
                    email = summary.billed_to_company.email
                else:
                    email = summary.billed_to_individual.email
                to.append(email)
            elif summary.MainClientToBeCCd:
                if summary.billed_to_company:
                    email = summary.billed_to_company.email
                else:
                    email = summary.billed_to_individual.email
                cc.append(email)
            elif summary.MainClientToBeBccd:
                if summary.billed_to_company:
                    email = summary.billed_to_company.email
                else:
                    email = summary.billed_to_company.email
                bcc.append(email)
                
            if summary.number_of_invoices != 1 and summary.number_of_invoices > 0:
                if summary.billed_to_company:
                    invoice_summary = summary
                    Total_price = invoice_summary.Total_price
                    Total_VAT = invoice_summary.Total_VAT
                    Total_with_VAT = invoice_summary.Total_with_VAT
                    total_table_entries = {'Price': Total_price, 'VAT': Total_VAT, 'Price_with_VAT': Total_with_VAT}
                    Current_date_time = timezone.now().strftime('%d%m%Y%H%M%S')
                    Date = datetime.today().strftime('%d-%m-%Y')
                    Due_date = datetime.today().strftime('%d-%m-%Y')
                    identifier = summary.billed_to_company.name + Current_date_time
                    if invoice_summary.contract:
                        invoice = Invoice.objects.create(InvoiceSummary=invoice_summary, workplace = invoice_summary.workplace, client_company=summary.billed_to_company, identifier=identifier, contract = invoice_summary.contract)
                    else:
                        invoice = Invoice.objects.create(InvoiceSummary=invoice_summary, workplace = invoice_summary.workplace, client_company=summary.billed_to_company, identifier=identifier)
                    invoice_items = InvoiceItem.objects.filter(invoice_summary=invoice_summary, last=False, workplace=invoice_summary.workplace)
                    for invoice_item in invoice_items:
                        invoices_to_invoice_items = InvoicesToInvoiceItems.objects.create(invoice_item = invoice_item, invoice=invoice, workplace=invoice_summary.workplace)
                    table_entries = []
                    for item in invoice_items:
                        entry = {'Name': item.Name, 'Price': item.Price, 'VAT': item.VAT, 'Total_price': item.Total_price}
                        table_entries.append(entry)
                    replacements = {
                    "{Company_Name}": summary.billed_to_company.name,
                    "{Company_Address}": summary.billed_to_company.address,
                    "{Date}": Date,
                    "{Invoice_Number}": identifier,
                    "{Due_date}": Due_date
                    }
                    input_file = UploadedInvoiceWordDocumentCompany.objects.get(workplace=summary.workplace)
                    replace_placeholders_invoice(input_file, replacements, table_entries, invoice, total_table_entries)
                    if to or cc or bcc:
                        Email_template = EmailInvoiceOtherInvoicesWithContract_company.objects.get(workplace=summary.workplace)
                        content_type = ContentType.objects.get_for_model(summary.billed_to_company)
                        Related_Contact_First_Name = None
                        Related_Contact_Last_Name = None
                        Related_Contact_Company_Name = None
                        represents_list = Represents.objects.filter(from_content_type=content_type, from_object_id = summary.billed_to_company.id, workplace=summary.workplace, selected=True)
                        for rep in represents_list:
                            if isinstance(rep.to_entity, Client_Individual):
                                Related_Contact_First_Name = rep.to_entity.Fname
                                Related_Contact_Last_Name = rep.to_entity.Lname
                            elif isinstance(rep.to_entity, Client_Company):
                                Related_Contact_Company_Name = rep.to_entity.name
                        company_name = summary.billed_to_company.name
                        Signer_First_Name = summary.billed_to_company.Signer.Fname
                        Signer_Last_Name = summary.billed_to_company.Signer.Lname
                        invoice_schedule = summary.schedule
                        replacements = {
                            "{Company_Name}": company_name,
                            "{Signer_First_Name}": Signer_First_Name,
                            "{Signer_Last_Name}": Signer_Last_Name,
                            "{Period}": invoice_schedule,
                            "{Related_Contact_First_Name}": Related_Contact_First_Name,
                            "{Related_Contact_Last_Name}": Related_Contact_Last_Name,
                            "{Related_Contact_Company_Name}": Related_Contact_Company_Name,
                        }
                        email_subject = ReplacePlaceholdersEmailCompany(Email_template.subject, replacements)
                        email_body = ReplacePlaceholdersEmailCompany(Email_template.body, replacements)
                        Subject = email_subject
                        Body = email_body
                        if to and cc and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, cc=cc, bcc=bcc)
                        elif to and cc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, cc=cc)
                        elif to and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, bcc=bcc)
                        elif cc and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, cc = cc, bcc=bcc)
                        elif to:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to)
                        elif cc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, cc = cc)
                        elif bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, bcc = bcc)
                        email.attach_file(invoice.invoice_file.path)
                        email.send()
                    else:
                        pass
                    summary.number_of_invoices -= 1
                elif summary.billed_to_individual:
                    invoice_summary = summary
                    Total_price = invoice_summary.Total_price
                    Total_VAT = invoice_summary.Total_VAT
                    Total_with_VAT = invoice_summary.Total_with_VAT
                    total_table_entries = {'Price': Total_price, 'VAT': Total_VAT, 'Price_with_VAT': Total_with_VAT}
                    Current_date_time = timezone.now().strftime('%d%m%Y%H%M%S')
                    Date = datetime.today().strftime('%d-%m-%Y')
                    Due_date = datetime.today().strftime('%d-%m-%Y')
                    identifier = summary.billed_to_individual.Fname + summary.billed_to_individual.Lname + Current_date_time
                    if invoice_summary.contract:
                        invoice = Invoice.objects.create(InvoiceSummary=invoice_summary, workplace = invoice_summary.workplace, client_company=summary.billed_to_company, identifier=identifier, contract = invoice_summary.contract)
                    else:
                        invoice = Invoice.objects.create(InvoiceSummary=invoice_summary, workplace = invoice_summary.workplace, client_company=summary.billed_to_company, identifier=identifier)
                    invoice_items = InvoiceItem.objects.filter(invoice_summary=invoice_summary, last=False, workplace=invoice_summary.workplace)
                    for invoice_item in invoice_items:
                        invoices_to_invoice_items = InvoicesToInvoiceItems.objects.create(invoice_item = invoice_item, invoice=invoice, workplace=invoice_summary.workplace)
                    table_entries = []
                    for item in invoice_items:
                        entry = {'Name': item.Name, 'Price': item.Price, 'VAT': item.VAT, 'Total_price': item.Total_price}
                        table_entries.append(entry)
                    replacements = {
                    "{Individual_Name}": f"{summary.billed_to_individual.Fname} {summary.billed_to_individual.Lname}",
                    "{Company_Address}": summary.billed_to_individual.address,
                    "{Date}": Date,
                    "{Invoice_Number}": identifier,
                    "{Due_date}": Due_date
                    }
                    input_file = UploadedInvoiceWordDocumentIndividual.objects.get(workplace=summary.workplace)
                    replace_placeholders_invoice(input_file, replacements, table_entries, invoice, total_table_entries)
                    if to or cc or bcc:
                        Email_template = EmailInvoiceOtherInvoicesWithContract_individual.objects.get(workplace=summary.workplace)
                        content_type = ContentType.objects.get_for_model(summary.billed_to_individual)
                        Related_Contact_First_Name = None
                        Related_Contact_Last_Name = None
                        Related_Contact_Company_Name = None
                        represents_list = Represents.objects.filter(from_content_type=content_type, from_object_id = summary.billed_to_individual.id, workplace=summary.workplace, selected=True)
                        for rep in represents_list:
                            if isinstance(rep.to_entity, Client_Individual):
                                Related_Contact_First_Name = rep.to_entity.Fname
                                Related_Contact_Last_Name = rep.to_entity.Lname
                            elif isinstance(rep.to_entity, Client_Company):
                                Related_Contact_Company_Name = rep.to_entity.name
                        Individual_Fname = summary.billed_to_individual.Fname
                        Individual_Lname = summary.billed_to_individual.Lname
                        invoice_schedule = summary.schedule
                        replacements = {
                            "{Client_First_Name}": Individual_Fname,
                            "{Client_Last_Name}": Individual_Lname,
                            "{Period}": invoice_schedule,
                            "{Related_Contact_First_Name}": Related_Contact_First_Name,
                            "{Related_Contact_Last_Name}": Related_Contact_Last_Name,
                            "{Related_Contact_Company_Name}": Related_Contact_Company_Name,
                        }
                        email_subject = ReplacePlaceholdersEmailCompany(Email_template.subject, replacements)
                        email_body = ReplacePlaceholdersEmailCompany(Email_template.body, replacements)
                        Subject = email_subject
                        Body = email_body
                        Subject = Email_template.subject
                        Body = Email_template.body
                        if to and cc and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, cc=cc, bcc=bcc)
                        elif to and cc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, cc=cc)
                        elif to and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, bcc=bcc)
                        elif cc and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, cc = cc, bcc=bcc)
                        elif to:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to)
                        elif cc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, cc = cc)
                        elif bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, bcc = bcc)
                        email.attach_file(invoice.invoice_file.path)
                        email.send()
                    else:
                        pass
                    summary.number_of_invoices -= 1
            elif summary.number_of_invoices == 1:
                if summary.billed_to_company:
                    invoice_summary = summary
                    Total_price = invoice_summary.last_invoice_total_price
                    Total_VAT = invoice_summary.last_invoice_Total_VAT
                    Total_with_VAT = invoice_summary.last_invoice_Total_with_VAT
                    total_table_entries = {'Price': Total_price, 'VAT': Total_VAT, 'Price_with_VAT': Total_with_VAT}
                    Current_date_time = timezone.now().strftime('%d%m%Y%H%M%S')
                    Date = datetime.today().strftime('%d-%m-%Y')
                    Due_date = datetime.today().strftime('%d-%m-%Y')
                    identifier = summary.billed_to_company.name + Current_date_time
                    if invoice_summary.contract:
                        invoice = Invoice.objects.create(InvoiceSummary=invoice_summary, workplace = invoice_summary.workplace, client_company=summary.billed_to_company, identifier=identifier, contract = invoice_summary.contract)
                    else:
                        invoice = Invoice.objects.create(InvoiceSummary=invoice_summary, workplace = invoice_summary.workplace, client_company=summary.billed_to_company, identifier=identifier)
                    invoice_items = InvoiceItem.objects.filter(invoice_summary=invoice_summary, last=True, workplace=invoice_summary.workplace)
                    for invoice_item in invoice_items:
                        invoices_to_invoice_items = InvoicesToInvoiceItems.objects.create(invoice_item = invoice_item, invoice=invoice, workplace=invoice_summary.workplace)
                    table_entries = []
                    for item in invoice_items:
                        entry = {'Name': item.Name, 'Price': item.Price, 'VAT': item.VAT, 'Total_price': item.Total_price}
                        table_entries.append(entry)
                    replacements = {
                    "{Company_Name}": summary.billed_to_company.name,
                    "{Company_Address}": summary.billed_to_company.address,
                    "{Date}": Date,
                    "{Invoice_Number}": identifier,
                    "{Due_date}": Due_date
                    }
                    input_file = UploadedInvoiceWordDocumentCompany.objects.get(workplace=summary.workplace)
                    replace_placeholders_invoice(input_file, replacements, table_entries, invoice, total_table_entries)
                    if to or cc or bcc:
                        Email_template = EmailInvoiceOtherInvoicesWithContract_company.objects.get(workplace=summary.workplace)
                        content_type = ContentType.objects.get_for_model(summary.billed_to_company)
                        Related_Contact_First_Name = None
                        Related_Contact_Last_Name = None
                        Related_Contact_Company_Name = None
                        represents_list = Represents.objects.filter(from_content_type=content_type, from_object_id = summary.billed_to_company.id, workplace=summary.workplace, selected=True)
                        for rep in represents_list:
                            if isinstance(rep.to_entity, Client_Individual):
                                Related_Contact_First_Name = rep.to_entity.Fname
                                Related_Contact_Last_Name = rep.to_entity.Lname
                            elif isinstance(rep.to_entity, Client_Company):
                                Related_Contact_Company_Name = rep.to_entity.name
                        company_name = summary.billed_to_company.name
                        Signer_First_Name = summary.billed_to_company.Signer.Fname
                        Signer_Last_Name = summary.billed_to_company.Signer.Lname
                        invoice_schedule = summary.schedule
                        replacements = {
                            "{Company_Name}": company_name,
                            "{Signer_First_Name}": Signer_First_Name,
                            "{Signer_Last_Name}": Signer_Last_Name,
                            "{Period}": invoice_schedule,
                            "{Related_Contact_First_Name}": Related_Contact_First_Name,
                            "{Related_Contact_Last_Name}": Related_Contact_Last_Name,
                            "{Related_Contact_Company_Name}": Related_Contact_Company_Name,
                        }
                        email_subject = ReplacePlaceholdersEmailCompany(Email_template.subject, replacements)
                        email_body = ReplacePlaceholdersEmailCompany(Email_template.body, replacements)
                        Subject = email_subject
                        Body = email_body
                        if to and cc and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, cc=cc, bcc=bcc)
                        elif to and cc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, cc=cc)
                        elif to and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, bcc=bcc)
                        elif cc and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, cc = cc, bcc=bcc)
                        elif to:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to)
                        elif cc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, cc = cc)
                        elif bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, bcc = bcc)
                        email.attach_file(invoice.invoice_file.path)
                        email.send()
                    else:
                        pass
                    summary.number_of_invoices -= 1
                elif summary.billed_to_individual:
                    invoice_summary = summary
                    Total_price = invoice_summary.last_invoice_total_price
                    Total_VAT = invoice_summary.last_invoice_Total_VAT
                    Total_with_VAT = invoice_summary.last_invoice_Total_with_VAT
                    total_table_entries = {'Price': Total_price, 'VAT': Total_VAT, 'Price_with_VAT': Total_with_VAT}
                    Current_date_time = timezone.now().strftime('%d%m%Y%H%M%S')
                    Date = datetime.today().strftime('%d-%m-%Y')
                    Due_date = datetime.today().strftime('%d-%m-%Y')
                    identifier = summary.billed_to_individual.Fname + summary.billed_to_individual.Lname + Current_date_time
                    if invoice_summary.contract:
                        invoice = Invoice.objects.create(InvoiceSummary=invoice_summary, workplace = invoice_summary.workplace, client_company=summary.billed_to_company, identifier=identifier, contract = invoice_summary.contract)
                    else:
                        invoice = Invoice.objects.create(InvoiceSummary=invoice_summary, workplace = invoice_summary.workplace, client_company=summary.billed_to_company, identifier=identifier)
                    invoice_items = InvoiceItem.objects.filter(invoice_summary=invoice_summary, last=True, workplace=invoice_summary.workplace)
                    for invoice_item in invoice_items:
                        invoices_to_invoice_items = InvoicesToInvoiceItems.objects.create(invoice_item = invoice_item, invoice=invoice, workplace=invoice_summary.workplace)
                    table_entries = []
                    for item in invoice_items:
                        entry = {'Name': item.Name, 'Price': item.Price, 'VAT': item.VAT, 'Total_price': item.Total_price}
                        table_entries.append(entry)
                    replacements = {
                    "{Individual_Name}": f"{summary.billed_to_individual.Fname} {summary.billed_to_individual.Lname}",
                    "{Company_Address}": summary.billed_to_individual.address,
                    "{Date}": Date,
                    "{Invoice_Number}": identifier,
                    "{Due_date}": Due_date
                    }
                    input_file = UploadedInvoiceWordDocumentIndividual.objects.get(workplace=summary.workplace)
                    replace_placeholders_invoice(input_file, replacements, table_entries, invoice, total_table_entries)
                    if to or cc or bcc:
                        Email_template = EmailInvoiceOtherInvoicesWithContract_individual.objects.get(workplace=summary.workplace)
                        content_type = ContentType.objects.get_for_model(summary.billed_to_individual)
                        Related_Contact_First_Name = None
                        Related_Contact_Last_Name = None
                        Related_Contact_Company_Name = None
                        represents_list = Represents.objects.filter(from_content_type=content_type, from_object_id = summary.billed_to_individual.id, workplace=summary.workplace, selected=True)
                        for rep in represents_list:
                            if isinstance(rep.to_entity, Client_Individual):
                                Related_Contact_First_Name = rep.to_entity.Fname
                                Related_Contact_Last_Name = rep.to_entity.Lname
                            elif isinstance(rep.to_entity, Client_Company):
                                Related_Contact_Company_Name = rep.to_entity.name
                        Individual_Fname = summary.billed_to_individual.Fname
                        Individual_Lname = summary.billed_to_individual.Lname
                        invoice_schedule = summary.schedule
                        replacements = {
                            "{Client_First_Name}": Individual_Fname,
                            "{Client_Last_Name}": Individual_Lname,
                            "{Period}": invoice_schedule,
                            "{Related_Contact_First_Name}": Related_Contact_First_Name,
                            "{Related_Contact_Last_Name}": Related_Contact_Last_Name,
                            "{Related_Contact_Company_Name}": Related_Contact_Company_Name,
                        }
                        email_subject = ReplacePlaceholdersEmailCompany(Email_template.subject, replacements)
                        email_body = ReplacePlaceholdersEmailCompany(Email_template.body, replacements)
                        Subject = email_subject
                        Body = email_body
                        Subject = Email_template.subject
                        Body = Email_template.body
                        if to and cc and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, cc=cc, bcc=bcc)
                        elif to and cc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, cc=cc)
                        elif to and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, bcc=bcc)
                        elif cc and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, cc = cc, bcc=bcc)
                        elif to:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to)
                        elif cc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, cc = cc)
                        elif bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, bcc = bcc)
                        email.attach_file(invoice.invoice_file.path)
                        email.send()
                    else:
                        pass
                    summary.number_of_invoices -= 1
            else:
                continue




def InvoicesAutomationsNotTiedtoContract():

    invoice_summary = Invoice_Summary.objects.filter(contract__isnull=True)
    
    for summary in invoice_summary:
        if summary.number_of_invoices != 0:
            current_date = timezone.now().date()
            if summary.schedule == "Monthly":
                if summary.created_at == current_date:
                    continue
                else:
                    if current_date.day != 1:
                        continue
                    else:
                        pass
            elif summary.schedule == "Daily":
                if summary.created_at == current_date:
                    continue
                else:
                    pass
            elif summary.schedule == "Weekly":
                created_week = summary.created_at.isocalendar()[1]
                current_week = current_date.isocalendar()[1]
                created_month = summary.created_at.month
                current_month = current_date.month
                created_year = summary.created_at.year
                current_year = current_date.year
                if created_week == current_week and created_month == current_month and created_year == current_year:
                    continue
                else:
                    if current_date.weekday() == 0:
                        pass
                    else:
                        continue
            elif summary.schedule == "Quarterly":
                created_quarter = (summary.created_at.month -1) // 3 + 1
                current_quarter = (current_date.month - 1) // 3 + 1
                created_year = summary.created_at.year
                current_year = current_date.year
                if created_quarter == current_quarter and created_year == current_year:
                    continue
                else:
                    first_month_of_current_quarter = 3* (current_quarter - 1) + 1
                    if current_date.month == first_month_of_current_quarter and current_date.day == 1:
                        pass
                    else:
                        continue
            elif summary.schedule == "Yearly":
                if summary.created_at.year == current_date.year:
                    continue
                else:
                    if summary.created_at.month == current_date.month and summary.created_at.day == current_date.day or (summary.created_at.month == 2 and summary.created_at.day == 29 and current_date.month == 2 and current_date.day in [28, 29]):
                        pass
                    else:
                        continue
            to = []
            cc = []
            bcc = []
            try:
                contactscompaniestobetod = ContactsCompaniesToBeTodThrough.objects.filter(invoice_summary = summary, workplace = summary.workplace)
            except (ProgrammingError, OperationalError):
                contactscompaniestobetod = []
            try:
                contactscompaniestobeCCd = ContactsCompaniesToBeCCdThrough.objects.filter(invoice_summary = summary, workplace = summary.workplace)
            except (ProgrammingError, OperationalError):
                contactscompaniestobeCCd = []
            try:
                contactscompaniestobeBccd = ContactsCompaniesToBeBccdThrough.objects.filter(invoice_summary = summary, workplace=summary.workplace)
            except (ProgrammingError, OperationalError):
                contactscompaniestobeBccd = []
            try:
                contactsindividualstobetod = ContactsIndividualsToBeTodThrough.objects.filter(invoice_summary = summary, workplace=summary.workplace)
            except (ProgrammingError, OperationalError):
                contactsindividualstobetod = []
            try:
                contactsindividualstobeCCd = ContactsIndividualsToBeCCdThrough.objects.filter(invoice_summary = summary, workplace=summary.workplace)
            except (ProgrammingError, OperationalError):
                contactsindividualstobeCCd = []
            try:
                contactsindividualstobeBccd = ContactsIndividualsToBeBccdThrough.objects.filter(invoice_summary = summary, workplace=summary.workplace)
            except (ProgrammingError, OperationalError):
                contactsindividualstobeBccd = []
            try:
                userstobetod = UsersToBeTodThrough.objects.filter(invoice_summary = summary, workplace = summary.workplace)
            except (ProgrammingError, OperationalError):
                userstobetod = []
            try:
                userstobeCCd = UsersToBeCCdThrough.objects.filter(invoice_summary = summary, workplace = summary.workplace)
            except (ProgrammingError, OperationalError):
                userstobeCCd = []
            try:
                userstobeBccd = UsersToBeBccdThrough.objects.filter(invoice_summary = summary, workplace = summary.workplace)
            except (ProgrammingError, OperationalError):
                userstobeBccd = []

            if contactscompaniestobetod:
                for contact in contactscompaniestobetod:
                    email = contact.client_company.email
                    to.append(email)
            if contactscompaniestobeCCd:
                for contact in contactscompaniestobeCCd:
                    email = contact.client_company.email
                    cc.append(email)
            if contactscompaniestobeBccd:
                for contact in contactscompaniestobeBccd:
                    email = contact.client_company.email
                    bcc.append(email)
            if contactsindividualstobetod:
                for contact in contactsindividualstobetod:
                    email = contact.client_individual.email
                    to.append(email)
            if contactsindividualstobeCCd:
                for contact in contactsindividualstobeCCd:
                    email = contact.client_individual.email
                    cc.append(email)
            if contactsindividualstobeBccd:
                for contact in contactsindividualstobeBccd:
                    email = contact.client_individual.email
                    bcc.append(email)
            if userstobetod:
                for user in userstobetod:
                    email = user.user.email
                    to.append(email)
            if userstobeCCd:
                for user in userstobeCCd:
                    email = user.user.email
                    cc.append(email)
            if userstobeBccd:
                for user in userstobeBccd:
                    email = user.user.email
                    bcc.append(email)
            
            if summary.MainClientToBeTod:
                if summary.billed_to_company:
                    email = summary.billed_to_company.email
                else:
                    email = summary.billed_to_individual.email
                to.append(email)
            elif summary.MainClientToBeCCd:
                if summary.billed_to_company:
                    email = summary.billed_to_company.email
                else:
                    email = summary.billed_to_individual.email
                cc.append(email)
            elif summary.MainClientToBeBccd:
                if summary.billed_to_company:
                    email = summary.billed_to_company.email
                else:
                    email = summary.billed_to_company.email
                bcc.append(email)
            else:
                pass

            if summary.number_of_invoices != 1 and summary.number_of_invoices > 0:
                if summary.billed_to_company:
                    invoice_summary = summary
                    Total_price = invoice_summary.Total_price
                    Total_VAT = invoice_summary.Total_VAT
                    Total_with_VAT = invoice_summary.Total_with_VAT
                    total_table_entries = {'Price': Total_price, 'VAT': Total_VAT, 'Price_with_VAT': Total_with_VAT}
                    Current_date_time = timezone.now().strftime('%d%m%Y%H%M%S')
                    Date = datetime.today().strftime('%d-%m-%Y')
                    Due_date = datetime.today().strftime('%d-%m-%Y')
                    identifier = summary.billed_to_company.name + Current_date_time
                    invoice = Invoice.objects.create(InvoiceSummary=invoice_summary, workplace = invoice_summary.workplace, client_company=summary.billed_to_company, identifier=identifier)
                    invoice_items = InvoiceItem.objects.filter(invoice_summary=invoice_summary, last=False, workplace=invoice_summary.workplace)
                    for invoice_item in invoice_items:
                        invoices_to_invoice_items = InvoicesToInvoiceItems.objects.create(invoice_item = invoice_item, invoice=invoice, workplace=invoice_summary.workplace)
                    table_entries = []
                    for item in invoice_items:
                        entry = {'Name': item.Name, 'Price': item.Price, 'VAT': item.VAT, 'Total_price': item.Total_price}
                        table_entries.append(entry)
                    replacements = {
                    "{Company_Name}": summary.billed_to_company.name,
                    "{Company_Address}": summary.billed_to_company.address,
                    "{Date}": Date,
                    "{Invoice_Number}": identifier,
                    "{Due_date}": Due_date
                    }
                    input_file = UploadedInvoiceWordDocumentCompany.objects.get(workplace=summary.workplace)
                    replace_placeholders_invoice(input_file, replacements, table_entries, invoice, total_table_entries)
                    if to or cc or bcc:
                        Email_template = EmailInvoiceWithoutContract_company.objects.get(workplace=summary.workplace)
                        content_type = ContentType.objects.get_for_model(summary.billed_to_company)
                        Related_Contact_First_Name = None
                        Related_Contact_Last_Name = None
                        Related_Contact_Company_Name = None
                        represents_list = Represents.objects.filter(from_content_type=content_type, from_object_id = summary.billed_to_company.id, workplace=summary.workplace, selected=True)
                        for rep in represents_list:
                            if isinstance(rep.to_entity, Client_Individual):
                                Related_Contact_First_Name = rep.to_entity.Fname
                                Related_Contact_Last_Name = rep.to_entity.Lname
                            elif isinstance(rep.to_entity, Client_Company):
                                Related_Contact_Company_Name = rep.to_entity.name
                        company_name = summary.billed_to_company.name
                        Signer_First_Name = summary.billed_to_company.Signer.Fname
                        Signer_Last_Name = summary.billed_to_company.Signer.Lname
                        invoice_schedule = summary.schedule
                        replacements = {
                            "{Company_Name}": company_name,
                            "{Signer_First_Name}": Signer_First_Name,
                            "{Signer_Last_Name}": Signer_Last_Name,
                            "{Period}": invoice_schedule,
                            "{Related_Contact_First_Name}": Related_Contact_First_Name,
                            "{Related_Contact_Last_Name}": Related_Contact_Last_Name,
                            "{Related_Contact_Company_Name}": Related_Contact_Company_Name,
                        }
                        email_subject = ReplacePlaceholdersEmailCompany(Email_template.subject, replacements)
                        email_body = ReplacePlaceholdersEmailCompany(Email_template.body, replacements)
                        Subject = email_subject
                        Body = email_body
                        if to and cc and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, cc=cc, bcc=bcc)
                        elif to and cc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, cc=cc)
                        elif to and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, bcc=bcc)
                        elif cc and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, cc = cc, bcc=bcc)
                        elif to:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to)
                        elif cc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, cc = cc)
                        elif bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, bcc = bcc)
                        email.attach_file(invoice.invoice_file.path)
                        email.send()
                    else:
                        pass
                    summary.number_of_invoices -= 1
                elif summary.billed_to_individual:
                    invoice_summary = summary
                    Total_price = invoice_summary.Total_price
                    Total_VAT = invoice_summary.Total_VAT
                    Total_with_VAT = invoice_summary.Total_with_VAT
                    total_table_entries = {'Price': Total_price, 'VAT': Total_VAT, 'Price_with_VAT': Total_with_VAT}
                    Current_date_time = timezone.now().strftime('%d%m%Y%H%M%S')
                    Date = datetime.today().strftime('%d-%m-%Y')
                    Due_date = datetime.today().strftime('%d-%m-%Y')
                    identifier = summary.billed_to_individual.Fname + summary.billed_to_individual.Lname + Current_date_time
                    invoice = Invoice.objects.create(InvoiceSummary=invoice_summary, workplace = invoice_summary.workplace, client_company=summary.billed_to_company, identifier=identifier)
                    invoice_items = InvoiceItem.objects.filter(invoice_summary=invoice_summary, last=False, workplace=invoice_summary.workplace)
                    for invoice_item in invoice_items:
                        invoices_to_invoice_items = InvoicesToInvoiceItems.objects.create(invoice_item = invoice_item, invoice=invoice, workplace=invoice_summary.workplace)
                    table_entries = []
                    for item in invoice_items:
                        entry = {'Name': item.Name, 'Price': item.Price, 'VAT': item.VAT, 'Total_price': item.Total_price}
                        table_entries.append(entry)
                    replacements = {
                    "{Individual_Name}": f"{summary.billed_to_individual.Fname} {summary.billed_to_individual.Lname}",
                    "{Company_Address}": summary.billed_to_individual.address,
                    "{Date}": Date,
                    "{Invoice_Number}": identifier,
                    "{Due_date}": Due_date
                    }
                    input_file = UploadedInvoiceWordDocumentIndividual.objects.get(workplace=summary.workplace)
                    replace_placeholders_invoice(input_file, replacements, table_entries, invoice, total_table_entries)
                    if to or cc or bcc:
                        Email_template = EmailInvoiceWithoutContract_individual.objects.get(workplace=summary.workplace)
                        content_type = ContentType.objects.get_for_model(summary.billed_to_individual)
                        Related_Contact_First_Name = None
                        Related_Contact_Last_Name = None
                        Related_Contact_Company_Name = None
                        represents_list = Represents.objects.filter(from_content_type=content_type, from_object_id = summary.billed_to_individual.id, workplace=summary.workplace, selected=True)
                        for rep in represents_list:
                            if isinstance(rep.to_entity, Client_Individual):
                                Related_Contact_First_Name = rep.to_entity.Fname
                                Related_Contact_Last_Name = rep.to_entity.Lname
                            elif isinstance(rep.to_entity, Client_Company):
                                Related_Contact_Company_Name = rep.to_entity.name
                        Individual_Fname = summary.billed_to_individual.Fname
                        Individual_Lname = summary.billed_to_individual.Lname
                        invoice_schedule = summary.schedule
                        replacements = {
                            "{Client_First_Name}": Individual_Fname,
                            "{Client_Last_Name}": Individual_Lname,
                            "{Period}": invoice_schedule,
                            "{Related_Contact_First_Name}": Related_Contact_First_Name,
                            "{Related_Contact_Last_Name}": Related_Contact_Last_Name,
                            "{Related_Contact_Company_Name}": Related_Contact_Company_Name,
                        }
                        email_subject = ReplacePlaceholdersEmailCompany(Email_template.subject, replacements)
                        email_body = ReplacePlaceholdersEmailCompany(Email_template.body, replacements)
                        Subject = email_subject
                        Body = email_body
                        if to and cc and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, cc=cc, bcc=bcc)
                        elif to and cc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, cc=cc)
                        elif to and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, bcc=bcc)
                        elif cc and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, cc = cc, bcc=bcc)
                        elif to:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to)
                        elif cc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, cc = cc)
                        elif bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, bcc = bcc)
                        email.attach_file(invoice.invoice_file.path)
                        email.send()
                    else:
                        pass
                    summary.number_of_invoices -= 1
            elif summary.number_of_invoices == 1:
                if summary.billed_to_company:
                    invoice_summary = summary
                    Total_price = invoice_summary.last_invoice_total_price
                    Total_VAT = invoice_summary.last_invoice_Total_VAT
                    Total_with_VAT = invoice_summary.last_invoice_Total_with_VAT
                    total_table_entries = {'Price': Total_price, 'VAT': Total_VAT, 'Price_with_VAT': Total_with_VAT}
                    Current_date_time = timezone.now().strftime('%d%m%Y%H%M%S')
                    Date = datetime.today().strftime('%d-%m-%Y')
                    Due_date = datetime.today().strftime('%d-%m-%Y')
                    identifier = summary.billed_to_company.name + Current_date_time
                    invoice = Invoice.objects.create(InvoiceSummary=invoice_summary, workplace = invoice_summary.workplace, client_company=summary.billed_to_company, identifier=identifier)
                    invoice_items = InvoiceItem.objects.filter(invoice_summary=invoice_summary, last=True, workplace=invoice_summary.workplace)
                    for invoice_item in invoice_items:
                        invoices_to_invoice_items = InvoicesToInvoiceItems.objects.create(invoice_item = invoice_item, invoice=invoice, workplace=invoice_summary.workplace)
                    table_entries = []
                    for item in invoice_items:
                        entry = {'Name': item.Name, 'Price': item.Price, 'VAT': item.VAT, 'Total_price': item.Total_price}
                        table_entries.append(entry)
                    replacements = {
                    "{Company_Name}": summary.billed_to_company.name,
                    "{Company_Address}": summary.billed_to_company.address,
                    "{Date}": Date,
                    "{Invoice_Number}": identifier,
                    "{Due_date}": Due_date
                    }
                    input_file = UploadedInvoiceWordDocumentCompany.objects.get(workplace=summary.workplace)
                    replace_placeholders_invoice(input_file, replacements, table_entries, invoice, total_table_entries)
                    if to or cc or bcc:
                        Email_template = EmailInvoiceWithoutContract_company.objects.get(workplace=summary.workplace)
                        content_type = ContentType.objects.get_for_model(summary.billed_to_company)
                        Related_Contact_First_Name = None
                        Related_Contact_Last_Name = None
                        Related_Contact_Company_Name = None
                        represents_list = Represents.objects.filter(from_content_type=content_type, from_object_id = summary.billed_to_company.id, workplace=summary.workplace, selected=True)
                        for rep in represents_list:
                            if isinstance(rep.to_entity, Client_Individual):
                                Related_Contact_First_Name = rep.to_entity.Fname
                                Related_Contact_Last_Name = rep.to_entity.Lname
                            elif isinstance(rep.to_entity, Client_Company):
                                Related_Contact_Company_Name = rep.to_entity.name
                        company_name = summary.billed_to_company.name
                        Signer_First_Name = summary.billed_to_company.Signer.Fname
                        Signer_Last_Name = summary.billed_to_company.Signer.Lname
                        invoice_schedule = summary.schedule
                        replacements = {
                            "{Company_Name}": company_name,
                            "{Signer_First_Name}": Signer_First_Name,
                            "{Signer_Last_Name}": Signer_Last_Name,
                            "{Period}": invoice_schedule,
                            "{Related_Contact_First_Name}": Related_Contact_First_Name,
                            "{Related_Contact_Last_Name}": Related_Contact_Last_Name,
                            "{Related_Contact_Company_Name}": Related_Contact_Company_Name,
                        }
                        email_subject = ReplacePlaceholdersEmailCompany(Email_template.subject, replacements)
                        email_body = ReplacePlaceholdersEmailCompany(Email_template.body, replacements)
                        Subject = email_subject
                        Body = email_body
                        if to and cc and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, cc=cc, bcc=bcc)
                        elif to and cc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, cc=cc)
                        elif to and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, bcc=bcc)
                        elif cc and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, cc = cc, bcc=bcc)
                        elif to:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to)
                        elif cc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, cc = cc)
                        elif bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, bcc = bcc)
                        email.attach_file(invoice.invoice_file.path)
                        email.send()
                    else:
                        pass
                    summary.number_of_invoices -= 1
                elif summary.billed_to_individual:
                    invoice_summary = summary
                    Total_price = invoice_summary.last_invoice_total_price
                    Total_VAT = invoice_summary.last_invoice_Total_VAT
                    Total_with_VAT = invoice_summary.last_invoice_Total_with_VAT
                    total_table_entries = {'Price': Total_price, 'VAT': Total_VAT, 'Price_with_VAT': Total_with_VAT}
                    Current_date_time = timezone.now().strftime('%d%m%Y%H%M%S')
                    Date = datetime.today().strftime('%d-%m-%Y')
                    Due_date = datetime.today().strftime('%d-%m-%Y')
                    identifier = summary.billed_to_individual.Fname + summary.billed_to_individual.Lname + Current_date_time
                    invoice = Invoice.objects.create(InvoiceSummary=invoice_summary, workplace = invoice_summary.workplace, client_company=summary.billed_to_company, identifier=identifier)
                    invoice_items = InvoiceItem.objects.filter(invoice_summary=invoice_summary, last=True, workplace=invoice_summary.workplace)
                    for invoice_item in invoice_items:
                        invoices_to_invoice_items = InvoicesToInvoiceItems.objects.create(invoice_item = invoice_item, invoice=invoice, workplace=invoice_summary.workplace)
                    table_entries = []
                    for item in invoice_items:
                        entry = {'Name': item.Name, 'Price': item.Price, 'VAT': item.VAT, 'Total_price': item.Total_price}
                        table_entries.append(entry)
                    replacements = {
                    "{Individual_Name}": f"{summary.billed_to_individual.Fname} {summary.billed_to_individual.Lname}",
                    "{Company_Address}": summary.billed_to_individual.address,
                    "{Date}": Date,
                    "{Invoice_Number}": identifier,
                    "{Due_date}": Due_date
                    }
                    input_file = UploadedInvoiceWordDocumentIndividual.objects.get(workplace=summary.workplace)
                    replace_placeholders_invoice(input_file, replacements, table_entries, invoice, total_table_entries)
                    if to or cc or bcc:
                        Email_template = EmailInvoiceWithoutContract_individual.objects.get(workplace=summary.workplace)
                        content_type = ContentType.objects.get_for_model(summary.billed_to_individual)
                        Related_Contact_First_Name = None
                        Related_Contact_Last_Name = None
                        Related_Contact_Company_Name = None
                        represents_list = Represents.objects.filter(from_content_type=content_type, from_object_id = summary.billed_to_individual.id, workplace=summary.workplace, selected=True)
                        for rep in represents_list:
                            if isinstance(rep.to_entity, Client_Individual):
                                Related_Contact_First_Name = rep.to_entity.Fname
                                Related_Contact_Last_Name = rep.to_entity.Lname
                            elif isinstance(rep.to_entity, Client_Company):
                                Related_Contact_Company_Name = rep.to_entity.name
                        Individual_Fname = summary.billed_to_individual.Fname
                        Individual_Lname = summary.billed_to_individual.Lname
                        invoice_schedule = summary.schedule
                        replacements = {
                            "{Client_First_Name}": Individual_Fname,
                            "{Client_Last_Name}": Individual_Lname,
                            "{Period}": invoice_schedule,
                            "{Related_Contact_First_Name}": Related_Contact_First_Name,
                            "{Related_Contact_Last_Name}": Related_Contact_Last_Name,
                            "{Related_Contact_Company_Name}": Related_Contact_Company_Name,
                        }
                        email_subject = ReplacePlaceholdersEmailCompany(Email_template.subject, replacements)
                        email_body = ReplacePlaceholdersEmailCompany(Email_template.body, replacements)
                        Subject = email_subject
                        Body = email_body
                        if to and cc and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, cc=cc, bcc=bcc)
                        elif to and cc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, cc=cc)
                        elif to and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, bcc=bcc)
                        elif cc and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, cc = cc, bcc=bcc)
                        elif to:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to)
                        elif cc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, cc = cc)
                        elif bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, bcc = bcc)
                        email.attach_file(invoice.invoice_file.path)
                        email.send()
                    else:
                        pass
                    summary.number_of_invoices -= 1
            else:
                continue
    

def calculate_reminder_days(reminders_count, reminders_per, invoice_summary):
    current_date = timezone.now().date()
    created_at_date = invoice_summary.created_at

    def calculate_weekdays_between(start_date, end_date):
        days = []
        while start_date <= end_date:
            if start_date.weekday() < 5:
                days.append(start_date)
            start_date += timedelta(days=1)
        return days
    
    if reminders_per == 'Per Day':
        return [current_date]
    
    elif reminders_per == 'Per Week':
        start_date = current_date - timedelta(days=current_date.weekday())
        end_date = start_date + timedelta(days=6)
        if start_date <= created_at_date <=end_date:
            start_date = created_at_date
        weekdays = calculate_weekdays_between(start_date, end_date)
    
    elif reminders_per == 'Per Month':
        year = current_date.year
        month = current_date.month
        days_in_month = calendar.monthrange(year, month)[1]
        start_date = date(year, month, 1)
        end_date = date(year, month, days_in_month)
        if start_date <= created_at_date <= end_date:
            start_date = created_at_date
        weekdays = calculate_weekdays_between(start_date, end_date)
    
    elif reminders_per == 'Per Quarter':
        year = current_date.year
        current_quarter = (current_date.month - 1) // 3 + 1
        first_month = 3* (current_quarter - 1) + 1
        last_month = first_month + 2
        start_date = date(year, first_month, 1)
        last_month_days = calendar.monthrange(year, last_month)[1]
        end_date = date(year, last_month, last_month_days)
        if start_date <= created_at_date <= end_date:
            start_date = created_at_date
        weekdays = calculate_weekdays_between(start_date, end_date)

    elif reminders_per == 'Per Year':
        year = current_date.year
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
        if start_date <= created_at_date <= end_date:
            start_date = created_at_date
        weekdays = calculate_weekdays_between(start_date, end_date)
    
    else:
        return []
    
    total_weekdays = len(weekdays)
    if reminders_count >= total_weekdays:
        return weekdays
    step = total_weekdays // reminders_count

    reminder_days = []
    for i in range(reminders_count):
        day_index = i * step
        if day_index < total_weekdays:
            reminder_days.append(weekdays[day_index])

    return reminder_days




def InvoicesRemindersAutomations():
    invoice_summary = Invoice_Summary.objects.all()
    for summary in invoice_summary:
        current_date = timezone.now().date()
        reminder_list = []
        if summary.schedule == "Monthly":
            if summary.created_at == current_date:
                continue
            else:
                if current_date.day != 1:
                    invoices = Invoice.objects.filter(InvoiceSummary=summary, workplace=summary.workplace, Paid=False)
                    if invoices:
                        for invoice in invoices:
                            if invoice.Paid:
                                continue
                            reminders_count = invoice.InvoiceSummary.reminders_count
                            reminders_per = invoice.InvoiceSummary.reminders_per
                            invoice_summary = invoice.InvoiceSummary
                            reminder_days = calculate_reminder_days(reminders_count, reminders_per, invoice_summary)
                            for day in reminder_days:
                                 if day == current_date:
                                    reminder_invoice = invoice
                                    reminder_day = day
                                    reminder_list.append(reminder_invoice)
                                    break
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
        elif summary.schedule == "Daily":
            if summary.created_at == current_date:
                continue
            else:
                    invoices = Invoice.objects.filter(InvoiceSummary = summary, workplace=summary.workplace, Paid=False)
                    if invoices:
                        for invoice in invoices:
                            if invoice.Paid:
                                continue
                            reminders_count = invoice.InvoiceSummary.reminders_count
                            reminders_per = invoice.InvoiceSummary.reminders_per
                            invoice_summary = invoice.InvoiceSummary
                            reminder_days = calculate_reminder_days(reminders_count, reminders_per, invoice_summary)
                            for day in reminder_days:
                                 if day == current_date:
                                    reminder_invoice = invoice
                                    reminder_day = day
                                    reminder_list.append(reminder_invoice)
                                    break
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
                
        elif summary.schedule == "Weekly":
            created_day = summary.created_at.isocalendar()[0]
            current_day = current_date.isocalendar()[0]
            created_week = summary.created_at.isocalendar()[1]
            current_week = current_date.isocalendar()[1]
            created_month = summary.created_at.month
            current_month = current_date.month
            created_year = summary.created_at.year
            current_year = current_date.year
            if created_day == current_day and created_week == current_week and created_month == current_month and created_year == current_year:
                continue
            else:
                if current_date.weekday() != 0:
                    invoices = Invoice.objects.filter(InvoiceSummary = summary, workplace=summary.workplace, Paid=False)
                    if invoices:
                        for invoice in invoices:
                            if invoice.Paid:
                                continue
                            reminders_count = invoice.InvoiceSummary.reminders_count
                            reminders_per = invoice.InvoiceSummary.reminders_per
                            invoice_summary = invoice.InvoiceSummary
                            reminder_days = calculate_reminder_days(reminders_count, reminders_per, invoice_summary)
                            for day in reminder_days:
                                 if day == current_date:
                                    reminder_invoice = invoice
                                    reminder_day = day
                                    reminder_list.append(reminder_invoice)
                                    break
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
        elif summary.schedule == "Quarterly":
            created_quarter = (summary.created_at.month -1) // 3 + 1
            current_quarter = (current_date.month - 1) // 3 + 1
            created_year = summary.created_at.year
            current_year = current_date.year
            if created_quarter == current_quarter and created_year == current_year:
                if current_date != summary.created_at:
                    invoices = Invoice.objects.filter(InvoiceSummary = summary, workplace=summary.workplace, Paid=False)
                    if invoices:
                        for invoice in invoices:
                            if invoice.Paid:
                                continue
                            reminders_count = invoice.InvoiceSummary.reminders_count
                            reminders_per = invoice.InvoiceSummary.reminders_per
                            invoice_summary = invoice.InvoiceSummary
                            reminder_days = calculate_reminder_days(reminders_count, reminders_per, invoice_summary)
                            for day in reminder_days:
                                 if day == current_date:
                                    reminder_invoice = invoice
                                    reminder_day = day
                                    reminder_list.append(reminder_invoice)
                                    break
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
            else:
                invoices = Invoice.objects.filter(InvoiceSummary = summary, workplace=summary.workplace, Paid=False)
                if invoices:
                    for invoice in invoices:
                        if invoice.Paid:
                                continue
                        reminders_count = invoice.InvoiceSummary.reminders_count
                        reminders_per = invoice.InvoiceSummary.reminders_per
                        invoice_summary = invoice.InvoiceSummary
                        reminder_days = calculate_reminder_days(reminders_count, reminders_per, invoice_summary)
                        for day in reminder_days:
                             if day == current_date:
                                reminder_invoice = invoice
                                reminder_day = day
                                reminder_list.append(reminder_invoice)
                                break
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
        elif summary.schedule == "Yearly":
            if summary.created_at.year == current_date.year:
                if current_date != summary.created_at:
                    invoices = Invoice.objects.filter(InvoiceSummary = summary, workplace=summary.workplace, Paid=False)
                    if invoices:
                        for invoice in invoices:
                            if invoice.Paid:
                                continue
                            reminders_count = invoice.InvoiceSummary.reminders_count
                            reminders_per = invoice.InvoiceSummary.reminders_per
                            invoice_summary = invoice.InvoiceSummary
                            reminder_days = calculate_reminder_days(reminders_count, reminders_per, invoice_summary)
                            for day in reminder_days:
                                 if day == current_date:
                                    reminder_invoice = invoice
                                    reminder_day = day
                                    reminder_list.append(reminder_invoice)
                                    break
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
            else:
                invoices = Invoice.objects.filter(InvoiceSummary = summary, workplace=summary.workplace, Paid=False)
                if invoices:
                    for invoice in invoices:
                        if invoice.Paid:
                                continue
                        reminders_count = invoice.InvoiceSummary.reminders_count
                        reminders_per = invoice.InvoiceSummary.reminders_per
                        invoice_summary = invoice.InvoiceSummary
                        reminder_days = calculate_reminder_days(reminders_count, reminders_per, invoice_summary)
                        for day in reminder_days:
                             if day == current_date:
                                reminder_invoice = invoice
                                reminder_day = day
                                reminder_list.append(reminder_invoice)
                                break
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
        else:
            continue
        to = []
        cc = []
        bcc = []
        try:
            contactscompaniestobetod = ContactsCompaniesToBeTodThrough.objects.filter(invoice_summary = summary, workplace = summary.workplace)
        except (ProgrammingError, OperationalError):
            contactscompaniestobetod = []
        try:
            contactscompaniestobeCCd = ContactsCompaniesToBeCCdThrough.objects.filter(invoice_summary = summary, workplace = summary.workplace)
        except (ProgrammingError, OperationalError):
            contactscompaniestobeCCd = []
        try:
            contactscompaniestobeBccd = ContactsCompaniesToBeBccdThrough.objects.filter(invoice_summary = summary, workplace=summary.workplace)
        except (ProgrammingError, OperationalError):
            contactscompaniestobeBccd = []
        try:
            contactsindividualstobetod = ContactsIndividualsToBeTodThrough.objects.filter(invoice_summary = summary, workplace=summary.workplace)
        except (ProgrammingError, OperationalError):
            contactsindividualstobetod = []
        try:
            contactsindividualstobeCCd = ContactsIndividualsToBeCCdThrough.objects.filter(invoice_summary = summary, workplace=summary.workplace)
        except (ProgrammingError, OperationalError):
            contactsindividualstobeCCd = []
        try:
            contactsindividualstobeBccd = ContactsIndividualsToBeBccdThrough.objects.filter(invoice_summary = summary, workplace=summary.workplace)
        except (ProgrammingError, OperationalError):
            contactsindividualstobeBccd = []
        try:
            userstobetod = UsersToBeTodThrough.objects.filter(invoice_summary = summary, workplace = summary.workplace)
        except (ProgrammingError, OperationalError):
            userstobetod = []
        try:
            userstobeCCd = UsersToBeCCdThrough.objects.filter(invoice_summary = summary, workplace = summary.workplace)
        except (ProgrammingError, OperationalError):
            userstobeCCd = []
        try:
            userstobeBccd = UsersToBeBccdThrough.objects.filter(invoice_summary = summary, workplace = summary.workplace)
        except (ProgrammingError, OperationalError):
            userstobeBccd = []

        if contactscompaniestobetod:
            for contact in contactscompaniestobetod:
                email = contact.client_company.email
                to.append(email)
        if contactscompaniestobeCCd:
            for contact in contactscompaniestobeCCd:
                email = contact.client_company.email
                cc.append(email)
        if contactscompaniestobeBccd:
            for contact in contactscompaniestobeBccd:
                email = contact.client_company.email
                bcc.append(email)
        if contactsindividualstobetod:
            for contact in contactsindividualstobetod:
                email = contact.client_individual.email
                to.append(email)
        if contactsindividualstobeCCd:
            for contact in contactsindividualstobeCCd:
                email = contact.client_individual.email
                cc.append(email)
        if contactsindividualstobeBccd:
            for contact in contactsindividualstobeBccd:
                email = contact.client_individual.email
                bcc.append(email)
        if userstobetod:
            for user in userstobetod:
                email = user.user.email
                to.append(email)
        if userstobeCCd:
            for user in userstobeCCd:
                email = user.user.email
                cc.append(email)
        if userstobeBccd:
            for user in userstobeBccd:
                email = user.user.email
                bcc.append(email)
        
        if summary.MainClientToBeTod:
            if summary.billed_to_company:
                email = summary.billed_to_company.email
            else:
                email = summary.billed_to_individual.email
            to.append(email)
        elif summary.MainClientToBeCCd:
            if summary.billed_to_company:
                email = summary.billed_to_company.email
            else:
                email = summary.billed_to_individual.email
            cc.append(email)
        elif summary.MainClientToBeBccd:
            if summary.billed_to_company:
                email = summary.billed_to_company.email
            else:
                email = summary.billed_to_individual.email
            bcc.append(email)
        else:
            pass

        if reminder_list:
            for item in reminder_list:
                if summary.billed_to_company:
                    if to or cc or bcc:
                        Email_template = EmailInvoiceReminder_company.objects.get(workplace=summary.workplace)
                        content_type = ContentType.objects.get_for_model(summary.billed_to_company)
                        Related_Contact_First_Name = None
                        Related_Contact_Last_Name = None
                        Related_Contact_Company_Name = None
                        represents_list = Represents.objects.filter(from_content_type=content_type, from_object_id = summary.billed_to_company.id, workplace=summary.workplace, selected=True)
                        for rep in represents_list:
                            if isinstance(rep.to_entity, Client_Individual):
                                Related_Contact_First_Name = rep.to_entity.Fname
                                Related_Contact_Last_Name = rep.to_entity.Lname
                            elif isinstance(rep.to_entity, Client_Company):
                                Related_Contact_Company_Name = rep.to_entity.name
                        company_name = summary.billed_to_company.name
                        Signer_First_Name = summary.billed_to_company.Signer.Fname
                        Signer_Last_Name = summary.billed_to_company.Signer.Lname
                        invoice_schedule = summary.schedule
                        replacements = {
                            "{Company_Name}": company_name,
                            "{Signer_First_Name}": Signer_First_Name,
                            "{Signer_Last_Name}": Signer_Last_Name,
                            "{Period}": invoice_schedule,
                            "{Related_Contact_First_Name}": Related_Contact_First_Name,
                            "{Related_Contact_Last_Name}": Related_Contact_Last_Name,
                            "{Related_Contact_Company_Name}": Related_Contact_Company_Name,
                        }
                        email_subject = ReplacePlaceholdersEmailCompany(Email_template.subject, replacements)
                        email_body = ReplacePlaceholdersEmailCompany(Email_template.body, replacements)
                        Subject = email_subject
                        Body = email_body
                        if to and cc and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, cc=cc, bcc=bcc)
                        elif to and cc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, cc=cc)
                        elif to and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, bcc=bcc)
                        elif cc and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, cc = cc, bcc=bcc)
                        elif to:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to)
                        elif cc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, cc = cc)
                        elif bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, bcc = bcc)
                        email.attach_file(item.invoice_file.path)
                        email.send()
                    else:
                        pass
                elif summary.billed_to_individual:
                    if to or cc or bcc:
                        Email_template = EmailInvoiceReminder_individual.objects.get(workplace=summary.workplace)
                        content_type = ContentType.objects.get_for_model(summary.billed_to_individual)
                        Related_Contact_First_Name = None
                        Related_Contact_Last_Name = None
                        Related_Contact_Company_Name = None
                        represents_list = Represents.objects.filter(from_content_type=content_type, from_object_id = summary.billed_to_individual.id, workplace=summary.workplace, selected=True)
                        for rep in represents_list:
                            if isinstance(rep.to_entity, Client_Individual):
                                Related_Contact_First_Name = rep.to_entity.Fname
                                Related_Contact_Last_Name = rep.to_entity.Lname
                            elif isinstance(rep.to_entity, Client_Company):
                                Related_Contact_Company_Name = rep.to_entity.name
                        Individual_Fname = summary.billed_to_individual.Fname
                        Individual_Lname = summary.billed_to_individual.Lname
                        invoice_schedule = summary.schedule
                        replacements = {
                            "{Client_First_Name}": Individual_Fname,
                            "{Client_Last_Name}": Individual_Lname,
                            "{Period}": invoice_schedule,
                            "{Related_Contact_First_Name}": Related_Contact_First_Name,
                            "{Related_Contact_Last_Name}": Related_Contact_Last_Name,
                            "{Related_Contact_Company_Name}": Related_Contact_Company_Name,
                        }
                        email_subject = ReplacePlaceholdersEmailCompany(Email_template.subject, replacements)
                        email_body = ReplacePlaceholdersEmailCompany(Email_template.body, replacements)
                        Subject = email_subject
                        Body = email_body
                        if to and cc and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, cc=cc, bcc=bcc)
                        elif to and cc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, cc=cc)
                        elif to and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to, bcc=bcc)
                        elif cc and bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, cc = cc, bcc=bcc)
                        elif to:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, to = to)
                        elif cc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, cc = cc)
                        elif bcc:
                            email = EmailMessage(subject = Subject, body = Body, from_email=None, bcc = bcc)
                        email.attach_file(item.invoice_file.path)
                        email.send()
                    else:
                        pass
            

