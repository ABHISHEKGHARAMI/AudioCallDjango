from django.shortcuts import render ,redirect
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages

from .forms import SignUpForm

# Create your views here.

# login view
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect(reverse('videocall:index'))
            else:
                messages.error(request, 'Invalid username or password')
            
        else:
            messages.error(request,'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request,'accounts/login.html',{'form' : form})


    
# function based view for the user for creation of the user
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request,'your profile has been successfully created')
        
    
    
    
