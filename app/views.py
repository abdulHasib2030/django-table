from django.shortcuts import render, redirect

# Create your views here.
from .models import Person
from django.http import FileResponse
from reportlab.pdfgen import canvas

def personListView(request):
    table = Person.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        status = request.POST['status']
      
        Person.objects.create(name = name, email = email, status= status)
        return redirect('person_add')
        
    return render(request, "people.html", {
        "table": table
    })

### PDF Download View
def generate_pdf(request, pk):
    response = FileResponse(generate_pdf_file(pk), 
                            as_attachment=True, 
                            filename='user_information.pdf')
    return response
  

def generate_pdf_file(pk):
    from io import BytesIO
 
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
 
    # Create a PDF document
    user = Person.objects.get(id = pk)
    p.drawString(100, 750, f"{user.name} Information")
 
    y = 700
    p.drawString(100, y, f"Name : {user.name}")
    p.drawString(100, y - 20, f"Email : {user.email}")
    p.drawString(100, y - 40, f"Status : {user.status}")
    y -= 60
 
    p.showPage()
    p.save()
 
    buffer.seek(0)
    return buffer