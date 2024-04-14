

document.addEventListener('DOMContentLoaded', function () {
    var stripePublicKey = document.getElementById('id_stripe_public_key').textContent.trim();
    var clientSecret = document.getElementById('id_client_secret').textContent.trim();
    var stripe = Stripe(stripePublicKey);
    var elements = stripe.elements();

    // Custom styling can be passed to options when creating an Element
    var style = {
        base: {
            color: '#32325d',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
                color: '#aab7c4'
            }
        },
        invalid: {
            color: '#fa755a',
            iconColor: '#fa755a'
        }
    };

    // Create an instance of the card Element
    var card = elements.create('card', { style: style });

    // Add an instance of the card Element into the card-element div
    card.mount('#card-element');

    // Handle real-time validation errors on the card Element
    card.on('change', function (event) {
        var displayError = document.getElementById('card-errors');
        if (event.error) {
            displayError.textContent = event.error.message;
        } else {
            displayError.textContent = '';
        }
    });

    // Handle form submission
    var form = document.getElementById('payment-form');
    form.addEventListener('submit', function (event) {
        event.preventDefault();
        // Disable the submit button to prevent multiple submissions
        document.getElementById('submit-button').disabled = true;

        // Extract additional form data as needed
        var formData = new FormData(form);

        // Confirm the payment using Stripe.js
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    // Include additional billing details if needed
                    name: formData.get('full_name'),
                    email: formData.get('email'),
                    phone: formData.get('phone_number'),
                    address: {
                        line1: formData.get('street_address1'),
                        line2: formData.get('street_address2'),
                        city: formData.get('town_or_city'),
                        postal_code: formData.get('postcode'),
                        state: formData.get('county'),
                        country: formData.get('country')
                    }
                }
            }
        }).then(function (result) {
            if (result.error) {
                // Show any error message to the user
                var errorElement = document.getElementById('card-errors');
                errorElement.textContent = result.error.message;
                // Re-enable the submit button
                document.getElementById('submit-button').disabled = false;
            } else {
                // The payment has been processed!
                if (result.paymentIntent.status === 'succeeded') {
                    // Submit the form
                    form.submit();
                }
            }
        });
    });
});
