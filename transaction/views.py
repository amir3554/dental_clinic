from dental_clinic_project import settings
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http.response import JsonResponse, HttpResponse
from django.core.mail import send_mail, get_connection
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from .models import Transaction , TransactionStatus, PaymentMethod
from clinic.forms import AppointmentModelForm
from clinic.models import Appointment
import stripe
from stripe.error import SignatureVerificationError #type: ignore
import paypal
from .forms import MyPayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
import math


def make_transaction(request, appointment_id, pm):
    appointment = get_object_or_404(
        Appointment,
        pk=appointment_id,
        patient=request.user.id,
    )
    #knowing that the appointment exists and it is owned by the user of the request
    # or we can return a ( 403 Forbidden page )
    #if appointment.patient != request.user:
    #   raise PermissionDenied("You are not allowed to. You dont have this appointment")
    
    transaction, created  = Transaction.objects.get_or_create(
        appointment=appointment,
        defaults={
            'amount' : math.ceil(appointment.get_price),
            'payment_method' : pm,
            'items' : appointment.get_dental_type, 
        }  
    )
    return transaction


#'tuple' object has no attribute 'amount'....while making a transaction


def transaction_complete(transaction_id):
    transaction = Transaction.objects.get(pk=transaction_id)
    transaction.transaction_status = TransactionStatus.DONE
    transaction.save()

    msg_html = render_to_string('transaction_complete_email.html',
        {
            'appointment': transaction.appointment, #type:ignore
            'operation': transaction.appointment.operations_and_surgeries, #type:ignore 
        }
    )

    connection = get_connection()

    send_mail(
        subject= 'Appointment Confirmed',
        connection=connection,
        message=msg_html,
        html_message=msg_html,
        recipient_list=[transaction.patient_email],  #type:ignore 
        from_email=settings.EMAIL_SENDER,
    )
    connection.close()





def check_out(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient = request.user
    )
    return render(
        request, 'check_out.html',
        {
            'appointment' : appointment
        }
    )


def check_out_complete(request):
    return render(
        request, 'check_out_complete.html'
    )





'''
                                  /////
                ////
    /////////  ////////  //////// /////  ////////////      ////////
  ///////////  ////////  //////// /////  /////////////   ////// /////
  //////       ////      ////     /////  ////     ///// /////     ////
    /////////  ////      ////     /////  ////      //// //////////////
         ///// ////      ////     /////  ////     /////  ////
  ///////////  ////////  ////     /////  /////////////    ///////////
   ////////      //////  ////     /////  //// //////        ///////
                                         ////
                                         ////
'''



import stripe


def get_publishable_key(request):
    return JsonResponse(
        { 
            'publishable_key' : settings.STRIPE_PUBLISHABLE_KEY
        }
    )


def stripe_transaction(request, appointment_id):
    try:
        transaction = make_transaction(request, appointment_id, PaymentMethod.STRIPE)
    
        stripe.api_key = settings.STRIPE_SECRET_KEY

        intent = stripe.PaymentIntent.create(
            amount = int(transaction.amount * 100),
            currency=settings.CURRENCY,
            payment_method_types=['card'],
            metadata={
                'transaction' : transaction.pk
            }
        )
        return JsonResponse(
            {
                'client_secret': intent["client_secret"]
            }
        )

    except Exception as e:
        return JsonResponse(
            { 
                "message" : f"while making a transaction, please try again ...",
            },
            status = 400
        )


    
@csrf_exempt
def stripe_webhook(request):
    payload = request.body # to get to the data of the request
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        stripe_event_webhook = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_ENDPOINT_SECRET
        )
    except ValueError:
        print('Invalid payload')
        return HttpResponse(status=400)
    
    except SignatureVerificationError:
        print('Invalid signature')
        return HttpResponse(status=400)
    
    try:
        print("Event type received:", stripe_event_webhook.type)
        # Handle the event
        if stripe_event_webhook.type == 'payment_intent.succeeded':
            payment_intent = stripe_event_webhook.data.object
            transaction_id = payment_intent.metadata.transaction #type:ignore
            transaction_complete(transaction_id)
        
    except:
        print("Exception in webhook:")
        return HttpResponse(status=422, message="Webhook payload is malformed or missing required fields")

    return HttpResponse(status=200)






'''
////////////////////////////////////////////////////////////////////////
///              ////////////////////////              /////////////////
///     /////      //////////////////////     /////      ///////////////
///    ///  ///    //////////////////////    ///  ///    ///////////////
///     /////      //////////////////////     /////      ///////////////
///              ////////////////////////              /////////////////
///    //////////////////////////////////    ///////////////////////////
///    //////////////////////////////////    ///////////////////////////
///    //////////////////////////////////    ///////////////////////////
///    //////////////////////////////////    ///////////////////////////
////////////////////////////////////////////////////////////////////////
'''


def paypal_transaction(request, appointment_id):
    transaction = make_transaction(request, appointment_id, PaymentMethod.PAYPAL)

    form = MyPayPalPaymentsForm(initial = {
        'business' : settings.PAYPAL_EMAIL,
        'amount' : transaction.amount,
        'invoice' : transaction.pk,
        'currency_mode' : settings.CURRENCY,
        'return_url': f'http://{request.get_host()}{reverse('CheckOutComplete')}',
        'cancel_url': f'http://{request.get_host()}{reverse('CheckOut', args=[appointment_id])}'
        }
    )
    return HttpResponse(form.render())


@csrf_exempt
def paypal_webhook(sender, **kwargs):
    if sender.payment_status == ST_PP_COMPLETED:
        if sender.reciever_email != settings.PAYPAL_EMAIL:
            return
        print('Payment intent was successful')
        transaction_complete(sender.invoice)

valid_ipn_received.connect(paypal_webhook)










