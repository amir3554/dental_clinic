from paypal.standard.forms import PayPalPaymentsForm
from django.utils.html import format_html  
from django.utils.translation import gettext as _


class MyPayPalPaymentsForm(PayPalPaymentsForm):
    def render(self, *args, **kwargs):
        if not args or kwargs:
            return format_html(u"""
                <form action="{0}" method="post">
                    {1} 
                    <div class="d-grid gap-2 my-3">
                        <button class="btn" type="submit"
                            style="background-color: rgb(140, 124, 212);">
                               
                            <i class="lni lni-paypal-original"></i> {2}
                               
                        </button>
                    </div>
                </form>"""
            , self.get_login_url(), self.as_p(), _('Pay Now'))
        else:
            return super().render(*args, **kwargs)

