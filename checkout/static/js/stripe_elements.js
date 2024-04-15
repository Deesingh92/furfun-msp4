document.addEventListener('DOMContentLoaded', function() {
    var stripe = Stripe(document.getElementById('id_stripe_public_key').textContent);
    var elements = stripe.elements();

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

    var card = elements.create('card', { style: style });
    card.mount('#card-element');

    card.addEventListener('change', function(event) {
        var displayError = document.getElementById('card-errors');
        if (event.error) {
            displayError.textContent = event.error.message;
        } else {
            displayError.textContent = '';
        }
    });

    var form = document.getElementById('payment-form');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        stripe.createPaymentMethod({
            type: 'card',
            card: card,
        }).then(function(result) {
            if (result.error) {
                var errorElement = document.getElementById('card-errors');
                errorElement.textContent = result.error.message;
            } else {
                var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
                var paymentMethodId = result.paymentMethod.id;

                fetch('/checkout/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({
                        'payment_method_id': paymentMethodId
                    })
                }).then(function(response) {
                    return response.json();
                }).then(function(data) {
                    if (data.success) {
                        window.location.href = data.redirect_url;
                    } else {
                        var errorElement = document.getElementById('card-errors');
                        errorElement.textContent = data.error_message;
                    }
                });
            }
        });
    });
});
