from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from .form import SignupForm, AddRecordForm
from .models import Record

# Create your views here.

class Home(View):
    template_name = 'home.html'

    def get(self, request):

        records = Record.objects.all()

        return render(request, self.template_name, {'records': records})
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have Been Logged In!")
            return redirect('crm_main_app:home')
        else:
            messages.success(request, "There was an error logging you in")
            return redirect('crm_main_app:home')

class Logout_user(View):

    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out...")
        return redirect('crm_main_app:home')
    
class Signup(View):
    
    template_name = 'signup.html'

    def get(self, request):
        form = SignupForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have succesfully reistered!")
            return redirect('crm_main_app:home')
        else:   
            return render(request, self.template_name, {'form': form})

class Customer_record(View):
    
    template_name = 'record.html'

    def get(self, request, pk):
        if request.user.is_authenticated:
            Customer_record = Record.objects.get(id=pk)
            return render(request, self.template_name, {'customer_record': Customer_record})
        else:
            messages.success(request, "You must be logged in to view the page...")
            return redirect('crm_main_app:home')

class Delete_record(View):

    def get(self, request, pk):
        if request.user.is_authenticated:
            delete_it = Record.objects.get(id=pk)
            delete_it.delete()
            messages.success(request, "Record Deleted!")
            return redirect('crm_main_app:home')
        else:
            messages.success(request, "You must be logged in to do that...!")
            return redirect('crm_main_app:home')
        
# class Add_record(View):

#     template_name = 'add_record.html'

#     def get(self, request):

#         return render(request, self.template_name)
        
#     def post(self, request):

#         form = AddRecordForm(request.POST or None)

#         if request.user.is_authenticated:
#             if form.is_valid():
#                 add_record = form.save()
#                 messages.success(request, "Record Added...")
#                 return redirect('crm_main_app:home')
#             # 
      
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect('crm_main_app:home')        
        return render(request, 'add_record.html', {"form": form})
    else:
        messages.success(request, "You must be logged in...")
        return redirect('crm_main_app:home')
    
class Update_record(View):

    template_name = 'update_record.html'

    def get(self, request, pk):
        if request.user.is_authenticated:
            current_record = Record.objects.get(id=pk)
            form = AddRecordForm(request.POST or None, instance=current_record)
            if form.is_valid():
                form.save()
                messages.success(request, "Record has been updated")
                return redirect('crm_main_app:home')
            return render(request, self.template_name, {'form': form})
        else:
            messages.success(request, "You Must Be Logged In...")
            return redirect('crm_main_app:home')
            