from django.shortcuts import render, HttpResponse, get_object_or_404
from documents.models import Documents,Role, UsersDocuments
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def admin_dashboard(request):
    return render(request,'admin/dashboard.html')

def add_docuemnt(request):
    if request.method == 'POST':
        name = request.POST.get('name')  # Get the name from the POST data
        description = request.POST.get('description')  # Get the description from the POST data
        files = request.FILES.get('files')  # Get the file from the FILES data
        is_have_form = False  # Set is_have_form to True since a file is uploaded
        if files:
            is_have_form = True

        # Save the document to the database
        your_model_instance = Documents(name=name, description=description, files=files, is_have_form=is_have_form)
        your_model_instance.save()
        return HttpResponse("add successfully")
    return render(request,'admin/adddocuments.html')


def add_role(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        document_ids = request.POST.getlist('default')  # Get list of selected document IDs
        role = Role.objects.create(name=name)

        # Associate selected documents with the role
        for document_id in document_ids:
            document = Documents.objects.get(id=document_id)
            role.documents.add(document)

        return HttpResponse("Role added successfully")
    
    documents = Documents.objects.all()
    return render(request,'admin/addrole.html',{"documents":documents})



def all_users(request):
    users = User.objects.filter(is_superuser=False)
    greeting = {}
    greeting['users'] = users
    return render(request,'admin/user.html',greeting)


def is_submit(all_document,document):
    for i in all_document:
        if i.document.id == document.id:
            return True
    return False

def user_details(request,id):
    user = User.objects.get(pk=id)
    print(user)
    documents = UsersDocuments.objects.filter(user=user)
    all_documents = Documents.objects.all()
    temp = []
    for i in all_documents:
        if not is_submit(documents,i):
            temp.append(i)

    print(temp)
    greeting = {}
    greeting['documents'] = documents
    greeting['lefted_documents'] = temp
    greeting['id'] = id
   
    return render(request,'admin/userdocuments.html',greeting)





def editDocument(request,id):
   
    document = UsersDocuments.objects.get(pk=id)
    greeting = {}
    greeting['document'] = document

    if request.method == "POST":
        status = bool(int(request.POST.get('status')))
        usermessage = request.POST.get('message')

        print(status)
        document.approved = status
        document.save()
        user = document.user
        value = "Approved" if status else "Disapproved"
        subject = f"Your {document.document.name} has been {value}"
        message = ""
        if status:
            message = "Your Documnet has been approved"
        else:
            message = usermessage

        from_email = settings.EMAIL_HOST_USER  # Sender's email address
        recipient_list = [user.email]  # List of recipient email addresses

        send_mail(subject, message, from_email, recipient_list)

        return render(request,'documents/message.html',{"message":'Document Update Successfully'})

   
    return render(request,'admin/editdocument.html',greeting)




def sendmail(request, document_id,user_id):
    if not request.user.is_superuser:
        return HttpResponse('Only admin can send email')
    
    # Retrieve the document and user objects using the IDs
    document = get_object_or_404(Documents, id=document_id)
    user = get_object_or_404(User, id=user_id)

    original_url = request.build_absolute_uri('/')[:-1]
    url = f"{original_url}/upoload-document/{document_id}"
    
    subject = f"Please Submit your {document.name}."
    message = f"click on this link {url} to submit your document"
    from_email = settings.EMAIL_HOST_USER  # Sender's email address
    recipient_list = [user.email]  # List of recipient email addresses

    send_mail(subject, message, from_email, recipient_list)

    return render(request,'documents/message.html',{"message":'Email sent successfully!'})
