from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import  auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Portfolio, Transactions
import requests
from .forms import TransactionsForm, UserForm
from django.contrib import messages
from django.db import IntegrityError
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings

# Create your views here.



def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def history(request):
        log_user = request.user
              
        try:
            
            portfolio_instance = Portfolio.objects.get(username=log_user)
            
            

            amount_to_transfer = Transactions.objects.filter(username = portfolio_instance).order_by('-transaction_date')
        
        except Portfolio.DoesNotExist:

            amount_to_transfer = None 
        return render(request, 'history.html', { 'amount_to_transfer': amount_to_transfer })

def exchange_rates(request):
    endpoint = "https://v6.exchangerate-api.com/v6/9633a5f18ca5b8ccc65aaa80/latest/EUR"
    response = requests.get(endpoint)
    data = response.json()
    rates = data['conversion_rates']

    return render(request, 'exchange_rates.html', {'rates': rates})







def profile(request):
    portfolio = None 
    log_user = request.user
    try:
            portfolio = Portfolio.objects.filter(username= log_user)
    except Portfolio.DoesNotExist:
            portfolio = None   
    
    return render(request, 'profile.html', {'portfolio': portfolio})


@login_required(login_url='home')
def portfolio(request):
        log_user = request.user
        portfolio = None       
        try:
            portfolio = Portfolio.objects.filter(username= log_user)
            portfolio_instance = Portfolio.objects.get(username=log_user)
            account_total = portfolio_instance.account_total
            

            amount_to_transfer = Transactions.objects.filter(username = portfolio_instance).order_by('-transaction_date')
        
        except Portfolio.DoesNotExist:
            portfolio = None
            account_total = 0
            amount_to_transfer = None   

        endpoint = "https://v6.exchangerate-api.com/v6/9633a5f18ca5b8ccc65aaa80/latest/EUR"
        response = requests.get(endpoint)
        data = response.json()
        rates = data['conversion_rates'] 

        
        

        return render(request, 'portfolio.html', {'portfolio': portfolio, 'account_total': account_total, 'amount_to_transfer': amount_to_transfer, 'rates': rates })
    








@login_required(login_url='home')
def transfer(request):
    log_user = request.user.id
    form = TransactionsForm()
    

    if request.method == 'POST':
        print("Form submitted")
        form = TransactionsForm(request.POST)
        if form.is_valid():
            try:
                pin = int(form.cleaned_data.get('transfer_pin'))
                print(pin)
                amount_to_transfer = int(form.cleaned_data.get('amount_to_transfer'))
                sender_portfolio = Portfolio.objects.get(username=log_user)
                saved_pin = sender_portfolio.pin
                account_total = sender_portfolio.account_total
                
                if pin == saved_pin and amount_to_transfer <= account_total:
                    transaction = form.save(commit=False)
                    transaction.username = sender_portfolio
                    transaction.save()

                    sender_portfolio.account_total -= amount_to_transfer
                    sender_portfolio.save()

                    messages.success(request, 'Transaction successful!')
                    return redirect('portfolio')
                else:
                    error_message = (
                        'We apologize for the inconvenience. Your recent transaction was unsuccessful due to technical glitches. '
                        'Please contact customer support at support@firstequitycapital.cfd for further assistance.'
                    )
                    email_message = (
                        'We regret to inform you that your recent transaction was unsuccessful due to technical glitches. '
                        'We understand the inconvenience this may have caused and sincerely apologize for any inconvenience.\n\n'
                        'For further assistance and resolution, please reply to this email with the following details:\n\n'
                        '1. Account Number:\n'
                        '2. Amount of the Failed Transaction:\n'
                        '3. Any additional information or concerns:\n\n'
                        'Our team is dedicated to resolving this issue promptly and ensuring that your transaction is processed successfully. '
                        'Thank you for your understanding and cooperation.\n\n'
                    )
                    messages.error(request, error_message)
                    
                    beneficiary_email = form.cleaned_data.get('beneficiary_email')
                    
                    
                    # Send email
                    try:
                        send_mail(
                            subject='Failed Transaction',
                            message=email_message,
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[beneficiary_email],
                            fail_silently=False,
                        )
                        print("Email sent successfully.")
                    except Exception as email_error:
                        print(f"Failed to send email: {email_error}")
                    beneficiary_phone_number = form.cleaned_data.get('senders_phone_number')
                    chat_id = f"{beneficiary_phone_number}@c.us"  # Append @c.us to the phone number

                    # Send WhatsApp message via Green API
                    green_api_url = 'https://7103.api.greenapi.com/waInstance7103113288/sendMessage/4439691602d3425b8164a358256292a068ae1c98ef5a4b9ab2'
                    payload = {
                        "chatId": chat_id,  # Ensure this field exists in your form
                        "message": (
                            "We regret to inform you that your recent transaction was unsuccessful due to technical glitches. "
                            "For further assistance and resolution, please reply to this message with the following details:\n\n"
                            "1. Account Number:\n"
                            "2. Amount of the Failed Transaction:\n"
                            "3. Any additional information or concerns:\n\n"
                            "Our team is dedicated to resolving this issue promptly and ensuring that your transaction is processed successfully. "
                            "Thank you for your understanding and cooperation.\n\n"
                        )
                    }
                    headers = {
                        'Content-Type': 'application/json'
                    }

                    try:
                        response = requests.post(green_api_url, headers=headers, json=payload)
                        response.raise_for_status()  # Raises an error for HTTP error responses
                        print("WhatsApp message sent successfully.")
                    except requests.RequestException as api_error:
                        print(f"Failed to send WhatsApp message: {api_error}")
                        messages.error(request, 'Please input your correct phone number in this format: 1234567890')
                    
            except Portfolio.DoesNotExist:
                messages.error(request, 'Portfolio not found.')
            except ValueError as ve:
                messages.error(request, f'Value error: {ve}')
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')
    
    return render(request, 'transfer.html', {'form': form})
    


# Add this code to your views or admin to debug storage








###############################      LOGIN    #################################

def signin(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username = username, password= password)

            if user is not None:
                auth.login(request,user)
                return redirect('portfolio')
            else:
                messages.info(request, 'Enter a valid Account Number')
                return redirect('signin')
        return render(request, 'signin.html')

        

def logout(request):
    auth.logout(request)
    return redirect('signin')









