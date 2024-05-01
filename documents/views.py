from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Role, UserDetails, Documents, UsersDocuments

# Create your views here.

@login_required(login_url="/")
def upoadDocument(request):
    user = request.user
    user_detail = UserDetails.objects.filter(user=user).first()
    role_deatils = Role.objects.filter(name=user_detail.role).first()
    documents = role_deatils.documents.all()
    greeting = {}
    greeting['documents'] = documents
    if request.method == "POST":
        for document in documents:
            file = request.FILES.get(str(document.id))
            UsersDocuments.objects.create(user=user,files=file,document=document)
        greeting['message'] = "Upload Succesfully"
        return render(request,'documents/message.html',greeting)

    return render(request,'documents/documentform.html',greeting)


@login_required(login_url='/')
def getOneDoucment(request, document_id):
    # Retrieve the document and user objects using the IDs
    document_from_db = get_object_or_404(Documents, id=document_id)
    default_document = [document_from_db]
    print(default_document)

    if request.method == 'POST':
        for document in default_document:
            uploaded_file = request.FILES[str(document.id)]
            documentRef = Documents.objects.get(pk=document.id)

            UserDocumentInstance = UsersDocuments.objects.filter(user=request.user,document=documentRef).first()
            if UserDocumentInstance == None:
                document_file = UsersDocuments.objects.create(
                    document=documentRef,
                    user=request.user,
                    files=uploaded_file
                )
                document_file.save()
            else:
                UserDocumentInstance.files = uploaded_file
                UserDocumentInstance.save()

    
        return render(request,'documents/message.html',{"message":'Document Submit successfully!'})
    
    return render(request, 'documents/documentform.html',{"documents":default_document})