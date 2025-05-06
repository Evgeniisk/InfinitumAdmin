from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
#The login_required decorator does the following:
#If the user isn't logged in, it redirects the user to settings.LOGIN_URL, passing the path specified by setting.Login_URL in the browser.
#If the user is logged in, it executes the view normally. The view code is then free to assume the user is logged in because the decorator does all the checking and security.
from django.contrib.auth.decorators import login_required
from .models import Email_Template_first, Email_Template_second, Client_Individual, Client_Company, Represents, Contract, Recurring_Invoice, Invoice, ContractItem, Job
# Create your views here.

@login_required
def api_email_template_first(request):
    #With request.user django automatically loads the full user from the database (CustomUser model)
    #With request.user.workplace django accesses the company FK for the logged-in user.
    #Thereby with the objects.filter() function accessing only the email template for that company.
    if request.method == 'GET':
        email_template_first = Email_Template_first.objects.get(workplace = request.user.workplace)
        return JsonResponse(email_template_first.as_dict())
    
    elif request.method =='POST':
        data = json.loads(request.body)
        subject = data.get('subject')
        body = data.get('body')
        #This accesses the user's workplace to store it associated with the right company in the database (isolation and data management)
        workplace = request.user.workplace
        email_template_first_post = Email_Template_first.objects.create(subject=subject, body=body, workplace=workplace)
        return JsonResponse(email_template_first_post.as_dict())
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        subject = data.get('subject')
        body = data.get('body')
        
        email_template_first_put = Email_Template_first.objects.get(workplace = request.user.workplace)
        email_template_first_put.subject = subject
        email_template_first_put.body = body
        email_template_first_put.save()
        return JsonResponse(email_template_first_put.as_dict())
    
    else:
        return HttpResponse(status=405)



@login_required
def api_email_template_second(request):
    if request.method == 'GET':
        email_template_second = Email_Template_second.objects.get(workplace = request.user.workplace)
        return JsonResponse(email_template_second.as_dict())
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        subject = data.get('subject')
        body = data.get('body')
        workplace = request.user.workplace
        email_template_second_post = Email_Template_second.objects.create(subject=subject, body=body, workplace=workplace)
        return JsonResponse(email_template_second_post.as_dict())
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        subject = data.get('subject')
        body = data.get('body')
        email_template_second_put = Email_Template_second.objects.get(workplace = request.user.workplace)
        email_template_second_put.subject = subject
        email_template_second_put.body = body
        email_template_second_put.save()
        return JsonResponse(email_template_second_put.as_dict())
    
    else:
        return HttpResponse(status=405)



@login_required
def api_client_individual(request):
    if request.method == 'GET':
        return JsonResponse({
            'clients_individuals': [
                client_individual.as_dict() for client_individual in Client_Individual.objects.filter(workplace = request.user.workplace)
            ]
        })
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        Fname = data.get('Fname')
        Lname = data.get('Lname')
        phone = data.get('phone')
        email = data.get('email')
        address = data.get('address')
        workplace = request.user.workplace
        client_individual_post = Client_Individual.objects.create(Fname=Fname, Lname=Lname, phone=phone, address=address, email=email, workplace=workplace)
        return JsonResponse(client_individual_post.as_dict())
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        id = data.get('id')
        Fname = data.get('Fname')
        Lname = data.get('Lname')
        phone = data.get('phone')
        email = data.get('email')
        address = data.get('address')
        client_individual_put = Client_Individual.objects.get(workplace = request.user.workplace, id=id)
        client_individual_put.Fname = Fname
        client_individual_put.Lname = Lname
        client_individual_put.phone = phone
        client_individual_put.email = email
        client_individual_put.address = address
        client_individual_put.save()
        return JsonResponse(client_individual_put.as_dict())
    
    elif request.method == 'DELETE':
        data = json.loads(request.body)
        id = data.get('id')
        client_individual_delete = Client_Individual.objects.get(workplace = request.user.workplace, id=id)
        client_individual_delete.delete()
        return JsonResponse({'message':'Client deleted'})
    
    else:
        return HttpResponse(status=405)
    


@login_required
def api_client_company(request):
    if request.method == 'GET':
        return JsonResponse({
            'clients_companies': [
                client_company.as_dict() for client_company in Client_Company.objects.filter(workplace = request.user.workplace)
            ]
        })
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        address = data.get('address')
        client_individuals_ids = data.get('individual_ids', [])

        client_company_post = Client_Company.objects.create(name=name, address=address, workplace=request.user.workplace)

        for client_individual_id in client_individuals_ids:
            individual = Client_Individual.objects.get(id=client_individual_id, workplace=request.user.workplace)
            Represents.objects.create(client_individual=individual, client_company=client_company_post, workplace=request.user.workplace, primary_contact=True)
        
        return JsonResponse(client_company_post.as_dict())
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        id = data.get('id')
        name = data.get('name')
        address = data.get('address')
        client_individuals_ids = data.get('individual_ids', [])

        client_company_put = Client_Company.objects.get(id=id, workplace=request.user.workplace)
        client_company_put.name = name
        client_company_put.address = address
        client_company_put.save()

        for client_individual_id in client_individuals_ids:
            individual = Client_Individual.objects.get(id=client_individual_id, workplace=request.user.workplace)
            if not Represents.objects.filter(client_individual=individual, workplace=request.user.workplace).exists():
                Represents.objects.create(client_individual=individual, client_company=client_company_put, workplace=request.user.workplace, primary_contact=True)
        
        return JsonResponse(client_company_put.as_dict())
    
    elif request.method == 'DELETE':
        data = json.loads(request.body)
        id = data.get('id')
        client_company_delete = Client_Company.objects.get(id=id, workplace=request.user.workplace)
        represents_company_delete = Represents.objects.get(client_company=client_company_delete, workplace=request.user.workplace)
        represents_company_delete.delete()
        client_company_delete.delete()
        return JsonResponse({'client_company': 'Deleted', 'Related Represents table entry': 'Deleted'})
    
    else:
        return HttpResponse(status=405)
    


@login_required
def api_contract(request):
    if request.method == 'GET':
        return JsonResponse({
            'contracts': [
                contract.as_dict() for contract in Contract.objects.filter(workplace=request.user.workplace)
            ]
        })
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        total_amount = data.get('total_amount')
        if 'client_individual_id' in data:
            client_individual_id = data.get('client_individual_id')
            client_individual = Client_Individual.objects.get(id=client_individual_id, workplace = request.user.workplace)
            contract_post = Contract.objects.create(total_amount=total_amount, workplace = request.user.workplace, client_individual=client_individual)
        elif 'client_company_id' in data:
            client_company_id = data.get('client_company_id')
            client_company = Client_Company.objects.get(id=client_company_id, workplace=request.user.workplace)
            contract_post = Contract.objects.create(total_amount=total_amount, workplace = request.user.workplace, client_company=client_company)
        return JsonResponse(contract_post.as_dict())
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        id = data.get('id')
        total_amount = data.get('total_amount')
        status = data.get('status')
        if 'client_individual_id' in data:
            client_individual_id = data.get('client_individual_id')
            client_individual = Client_Individual.objects.get(id=client_individual_id, workplace = request.user.workplace)
            contract_PUT = Contract.objects.get(id=id, workplace=request.user.workplace)
            contract_PUT.total_amount = total_amount
            contract_PUT.status = status
            contract_PUT.client_individual = client_individual
        elif 'client_company_id' in data:
            client_company_id = data.get('client_company_id')
            client_company = Client_Company.objects.get(id=client_company_id, workplace = request.user.workplace)
            contract_PUT = Contract.objects.get(id=id, workplace=request.user.workplace)
            contract_PUT.total_amount = total_amount
            contract_PUT.status = status
            contract_PUT.client_company = client_company
        contract_PUT.save()
        return JsonResponse(contract_PUT.as_dict())
    
    elif request.method == 'DELETE':
        data = json.loads(request.body)
        id = data.get('id')
        if 'client_individual_id' in data:
            client_individual_id = data.get('client_individual_id')
            client_individual = Client_Individual.objects.get(id=client_individual_id, workplace = request.user.workplace)
            contract_DELETE = Contract.objects.get(id=id, workplace = request.user.workplace, client_individual = client_individual)
        elif 'client_company_id' in data:
            client_company_id = data.get('client_company_id')
            client_company = Client_Company.objects.get(id=client_company_id, workplace = request.user.workplace)
            contract_DELETE = Contract.objects.get(id=id, workplace = request.user.workplace, client_company = client_company)
        contract_DELETE.delete()
        return JsonResponse({'Delete': 'Successful'})
    
    else:
        return HttpResponse(status=405)
    

#Rewrite the GET method to process query in the URL instead of loading the request body.
@login_required
def api_Recurring_Invoice(request):
    if request.method == 'GET':
        data = json.loads(request.body)
        id = data.get('id')
        assigned_to = data.get('assigned_to')
        contract_assigned_to = Contract.objects.get(id=assigned_to, workplace=request.user.workplace)
        recurring_invoice = Recurring_Invoice.objects.get(id=id, assigned_to=assigned_to)
        return JsonResponse({contract_assigned_to.as_dict(): recurring_invoice.as_dict()})
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        duration = data.get('duration')
        frequency = data.get('frequency')
        assigned_to = Contract.objects.get(id=data.get('assigned_to'), workplace=request.user.workplace)
        recurring_invoice_post = Recurring_Invoice.objects.create(duration=duration, frequency=frequency, assigned_to=assigned_to)
        return JsonResponse(recurring_invoice_post.as_dict())
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        id = data.get('id')
        duration = data.get('duration')
        frequency = data.get('frequency')
        assigned_to = Contract.objects.get(id=data.get('assigned_to'), workplace=request.user.workplace)
        recurring_invoice_put = Recurring_Invoice.objects.get(id=id, assigned_to=assigned_to)
        recurring_invoice_put.duration = duration
        recurring_invoice_put.frequency = frequency
        recurring_invoice_put.save()
        return JsonResponse(recurring_invoice_put.as_dict())
    
    elif request.method == 'DELETE':
        data = json.loads(request.body)
        id = data.get('id')
        assigned_to = Contract.objects.get(id=data.get('assigned_to'), workplace=request.user.workplace)
        recurring_invoice_delete = Recurring_Invoice.objects.get(id=id, assigned_to=assigned_to)
        recurring_invoice_delete.delete()
        return JsonResponse({'Contract': assigned_to.as_dict(), 'recurring_Invoice': 'Deleted'})
    
    else:
        return HttpResponse(status=405)



@login_required
def api_Invoice(request):
    if request.method == 'GET':
        return JsonResponse({
            'invoices': [invoice.as_dict() for invoice in Invoice.objects.filter(workplace = request.user.workplace)]
        })
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        total_amount = data.get('total_amount')
        if 'recurrence' in data:
            recurrence = Recurring_Invoice.objects.get(id=data.get('recurrence'))
            if 'billed_to_company' in data:
                billed_to_company = Client_Company.objects.get(id=data.get('billed_to_company'))
                invoice_post = Invoice.objects.create(total_amount=total_amount, recurrence=recurrence, billed_to_company=billed_to_company, workplace=request.user.workplace)
            elif 'billed_to_individual' in data:
                billed_to_individual = Client_Individual.objects.get(id=data.get('billed_to_individual'))
                invoice_post = Invoice.objects.create(total_amount=total_amount, recurrence=recurrence, billed_to_individual=billed_to_individual, workplace=request.user.workplace)
        elif 'recurrence' not in data:
            if 'billed_to_company' in data:
                billed_to_company = Client_Company.objects.get(id=data.get('billed_to_company'))
                invoice_post = Invoice.objects.create(total_amount=total_amount, billed_to_company=billed_to_company, workplace=request.user.workplace)
            elif 'billed_to_individual' in data:
                billed_to_individual = Client_Individual.objects.get(id=data.get('billed_to_individual'))
                invoice_post = Invoice.objects.create(total_amount=total_amount, billed_to_individual=billed_to_individual, workplace=request.user.workplace)
        return JsonResponse(invoice_post.as_dict())
    
    elif request.method == 'DELETE':
        data = json.loads(request.body)
        id = data.get('id')
        if 'billed_to_company' in data:
            billed_to_company = Client_Company.objects.get(id=data.get('billed_to_company'))
            invoice_delete = Invoice.objects.get(id=id, billed_to_company=billed_to_company, workplace=request.user.workplace)
        elif 'billed_to_individual' in data:
            billed_to_individual = Client_Individual.objects.get(id=data.get('billed_to_individual'))
            invoice_delete = Invoice.objects.get(id=id, billed_to_individual=billed_to_individual, workplace=request.user.workplace)
        invoice_delete.delete()
        return JsonResponse({'message': 'Invoice deleted successfully'})
    
    else:
        return HttpResponse(status=405)
    

#Rewrite the GET method to process query in the URL instead of loading the request body.
@login_required
def api_ContractItem(request):
    if request.method == 'GET':
        data = json.loads(request.body)
        id = data.get('id')
        contract = data.get('contract')
        is_in = data.get('invoice')
        contract_item_get = ContractItem.objects.get(id=id, contract=Contract.objects.get(id=contract), is_in=Invoice.objects.get(id=is_in), workplace=request.user.workplace)
        return JsonResponse(contract_item_get.as_dict())
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        ItemName = data.get('ItemName')
        description = data.get('description')
        amount = data.get('amount')
        contract = data.get('contract')
        is_in = data.get('invoice')
        contract_item_post = ContractItem.objects.create(ItemName = ItemName, description=description, amount=amount, contract=contract, is_in=is_in, workplace=request.user.workplace)
        return JsonResponse(contract_item_post.as_dict())
    
    elif request.method == 'PUT':
        data=json.loads(request.body)
        id = data.get('id')
        ItemName = data.get('ItemName')
        description = data.get('description')
        amount = data.get('amount')
        contract = data.get('contract')
        is_in = data.get('invoice')
        contract_item_put = ContractItem.objects.get(id=id, contract=contract, is_in=is_in, workplace=request.user.workplace)
        contract_item_put.ItemName = ItemName
        contract_item_put.description = description
        contract_item_put.amount = amount
        contract_item_put.save()
        return JsonResponse(contract_item_put.as_dict())
    
    elif request.method == 'DELETE':
        data = json.loads(request.body)
        id = data.get('id')
        contract = data.get('contract')
        is_in = data.get('invoice')
        contract_item_delete = ContractItem.objects.get(id=id, contract=contract, is_in=is_in, workplace = request.user.workplace)
        contract_item_delete.delete()
        return JsonResponse({'Contract Item': 'Deleted'})
    
    else:
        return HttpResponse(status=405)
    
@login_required
def api_Job(request):
    if request.method == 'GET':
        return JsonResponse({
            'Jobs': [
                job.as_dict() for job in Job.objects.filter(user = request.user, workplace = request.user.workplace)
            ]
        })
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        ItemName = data.get('ItemName')
        status = data.get('status')
        completed_at = data.get('completed_at')
        correspons_to = data.get('ContractItem')
        if 'description' in data:
            description = data.get('description')
        if 'started_at' in data:
            started_at = data.get('started_at')
        if description == True:
            job_item_post = Job.objects.create(ItemName=ItemName, description=description, status=status, completed_at=completed_at, corresponds_to=correspons_to, user=request.user, workplace=request.user.workplace)
        elif started_at == True:
            job_item_post = Job.objects.create(ItemName=ItemName, started_at=started_at, status=status, completed_at=completed_at, corresponds_to=correspons_to, user=request.user, workplace=request.user.workplace)
        elif description == True and started_at == True:
            job_item_post = Job.objects.create(ItemName=ItemName, description=description, started_at=started_at, status=status, completed_at=completed_at, corresponds_to=correspons_to, user=request.user, workplace=request.user.workplace)
        return JsonResponse(job_item_post.as_dict())
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        id = data.get('id')
        ItemName = data.get('ItemName')
        description = data.get('description')
        started_at = data.get('started_at')
        status = data.get('status')
        completed_at = data.get('completed_at')
        correspons_to = data.get('ContractItem')
        job_item_put = Job.objects.get(id=id, ItemName=ItemName, description=description, corresponds_to=correspons_to, user=request.user, workplace=request.user.workplace)
        job_item_put.started_at = started_at
        job_item_put.status = status
        job_item_put.completed_at = completed_at
        job_item_put.save()
        return JsonResponse(job_item_put.as_dict())
    
    elif request.method == 'DELETE':
        data = json.loads(request.body)
        id = data.get('id')
        corresponds_to = data.get('ContractItem')
        job_item_delete = Job.objects.get(id=id, corresponds_to=corresponds_to, user = request.user, workplace=request.user.workplace)
        job_item_delete.delete()
        return JsonResponse({'Job item': 'deleted'})
    
    else:
        return HttpResponse(status=405)