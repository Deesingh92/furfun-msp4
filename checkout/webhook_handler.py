import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.conf import settings

# Configure logging
logger = logging.getLogger(__name__)

# Set the Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def webhook(request):
    payload = request.body
    sig_header = request.headers.get('Stripe-Signature', None)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
        )
    except ValueError as e:
        # Invalid payload
        logger.error("Invalid payload: %s", e)
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        logger.error("Invalid signature: %s", e)
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        # Perform actions based on payment success
        logger.info("Payment succeeded: %s", payment_intent)
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        # Perform actions based on payment failure
        logger.warning("Payment failed: %s", payment_intent)


    return JsonResponse({'message': 'Webhook received successfully'}, status=200)

class StripeWH_Handler:
    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        # Handle Stripe webhook event
        return HttpResponse(status=200)
