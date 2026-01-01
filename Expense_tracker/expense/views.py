from django.shortcuts import render,redirect,get_object_or_404
from .models import expense,income,User
from django.db.models import Sum
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
# Create your views here.
def home(request):
 if request.user.is_authenticated:
    selected_month=request.GET.get('month')
    selected_category=request.GET.get('category')
    filtered_expense=0
    expenses=expense.objects.filter(owner=request.user).order_by('-date','-id')
    if selected_category:
      if selected_month:
       expenses=expenses.filter(date__month=selected_month,category=selected_category).order_by('-date','-id')
      else:
          expenses=expenses.filter(category=selected_category).order_by('-date','-id')
      filtered_expense=expenses.aggregate(total=Sum('amount')) ['total'] or 0
      print(filtered_expense)  
    if selected_month:
       if selected_category:
        expenses=expenses.filter(date__month=selected_month,category=selected_category).order_by('-date','-id')
       else:
          expenses=expenses.filter(date__month=selected_month).order_by('-date','-id')
       filtered_expense=expenses.aggregate(total=Sum('amount')) ['total'] or 0
    total_expense=expense.objects.filter(owner=request.user).aggregate(total=Sum('amount')) ['total'] or 0
    incomes=income.objects.filter(owner=request.user).first()
    total_income=incomes.amount if incomes else 0
    total_balance=total_income-total_expense
 else:
    expenses=[]
    total_balance=0
    total_expense=0
    total_income=0
    selected_month=''
    selected_category=''
    filtered_expense=0
 return render(request, 'expense/home.html',{'expenses':expenses, 'total_expense':total_expense,'total_income':total_income,'total_balance':total_balance,'selected_month':selected_month,'filtered_expense':filtered_expense,'selected_category':selected_category})

@login_required
def add_expense(request):
     if request.method=='POST':
         expense_id=request.POST.get('expense_id')
         category=request.POST.get('category')
         date=request.POST.get('date')
         description=request.POST.get('description')
         amount=Decimal(request.POST.get('amount'))

         if expense_id:
          expense_card=get_object_or_404(expense,id=expense_id,owner=request.user)
          expense_card.amount=amount
          expense_card.category=category
          expense_card.description=description
          expense_card.date=date
          expense_card.save()
         else:
             expense.objects.create(
                 owner=request.user,
                 amount=amount,
                 category=category,
                 date=date,
                 description=description
             )
     return redirect('home')
@login_required
def delete_expense(request,id):
     obj=get_object_or_404(expense,id=id,owner=request.user)
     obj.delete()
     return redirect('home')
@login_required
def set_income(request):
    if request.method=='POST':
        amount=request.POST.get('income')
        income.objects.update_or_create(owner=request.user,defaults={'amount':amount})
    return redirect('home')
def login_user(request):
  if request.method=='POST':
     username=request.POST.get('username')
     password=request.POST.get('password')
     user=authenticate(request,username=username , password=password )
     if user is not None:
        login(request,user)
        messages.success(request,'Logged in Successfully!')
     else:
        messages.error(request,'Invalid Credential!')
        return redirect('home')
  return redirect('home')

@login_required    
def logout_user(request):
   logout(request)
   messages.error(request,'Logged out Successfully! ')
   return redirect('home')
def register_user(request):
  if request.method=='POST':
     username=request.POST.get('username')
     password=request.POST.get('password1')
     confirm_password=request.POST.get('password2')

     if username and password and confirm_password is None:
        messages.error(request,'Some fields are empty')
        return redirect('home')
     else:
        if User.objects.filter(username=username).exists():
           messages.error(request,'username already exist!')
           return redirect('home')
        else:
           if password!=confirm_password:
              messages.error(request,'passwords must be same!')
              return redirect('home')
           else:
              user=User.objects.create_user(username=username,password=password)
              login(request,user)
              messages.success(request,'Account Created Successfully!')
              return redirect('home')
  return redirect('home')


     