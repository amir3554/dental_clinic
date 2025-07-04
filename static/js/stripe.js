let stripe, elements;
const stripeSubmit = document.getElementById('stripe-submit');


 // دالة بسيطة لجلب قيمة الـ CSRF من الكوكيز
function getCookie(name) {
let cookieValue = null;
if (document.cookie && document.cookie !== '') {
    document.cookie.split(';').forEach(cookie => {
    let [key, val] = cookie.trim().split('=');
    if (key === name) cookieValue = decodeURIComponent(val);
    });
}
return cookieValue;
}

function getCsrfToken() {
  return document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute('content');
}





async function createStripeSession() {

        const appointmentElement = document.getElementById('appointment-id');
        const appointmentId = appointmentElement.getAttribute('data-appointment-id');

    switchPaymentMethod('srtipe', '')

    stripeSubmit.disabled = true;

    const headers = {
        'Content-Type' : 'application/json',
        'X-CSRFToken' : getCsrfToken()
    }

    try {
        const { data } = await axios.post(
            `/transaction/stripe/${appointmentId}`,
            {} ,// the body of the request (empty object if there are no date)
            { headers } // here comes the config that has the header
        );
        const { client_secret } = data;

        const appearance = { theme: 'flat' };
        elements = stripe.elements({ appearance, clientSecret: client_secret });
        const paymentElement = elements.create("payment")
        paymentElement.mount("#payment-element");

        document
        .querySelector("#payment-form")
        .addEventListener("submit", _stripeFormSubmit);

        document.getElementById('stripe-card').style.display = 'block';
        stripeSubmit.disabled = false;
        console.log("paymentElement", paymentElement);
          
    } catch (e) {
        notyf.error(e?.response?.data?.message
            || "An error occurred while creating a stripe session." );
    } 
}

async function _stripeFormSubmit(e) {
    e.preventDefault();
    stripeSubmit.disabled = true;
    const host = window.location.protocol + "//" + window.location.host;
    const { error } = await stripe.confirmPayment({
        elements,
        confirmParams: {
            return_url: `${host}/transaction/check-out-complete`,
        },
    });

    if (error.type === "card_error" || error.type === "validation_error") {
        notyf.error(error.message);
    } else {
        notyf.error("عذرًا، هنالك خطأ ما حصل خلال عملية الدفع.");
    }
    stripeSubmit.disabled = false;
}

async function _checkStripePaymentStatus() {
    const clientSecret = new URLSearchParams(window.location.search).get(
        "payment_intent_client_secret"
    );
    if (!clientSecret) {
        return;
    }
    const { paymentIntent } = await stripe.retrievePaymentIntent(clientSecret);
    switch (paymentIntent.status) {
        case "succeeded":
            notyf.success("لقد تمت عملية الدفع بنجاح!");
            break;
        case "processing":
            notyf.success("عملية الدفع قيد المعالجة");
            break;
        default:
            notyf.error("عذرًا، هنالك خطأ ما حصل خلال عملية الدفع.");
            break;
    }
}

async function _stripeInit() {
        const { data } = await axios("/transaction/stripe/config/publishable-key/");
        stripe = Stripe(data.publishable_key, { locale: 'ar' });
        _checkStripePaymentStatus();
}

_stripeInit();