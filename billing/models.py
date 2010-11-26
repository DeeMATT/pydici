# coding: utf-8
"""
Database access layer for pydici billing module
@author: Sébastien Renard (sebastien.renard@digitalfox.org)
@license: GPL v3 or newer
"""


from django.db import models
from django.utils.translation import ugettext_lazy as _

from datetime import date

from pydici.leads.models import Lead

class Bill(models.Model):
    #TODO: add number of bill (unique per lead)
    BILL_STATE = (
            ('1_SENT', _("Sent")),
            ('2_PAID', _("Paid")),
            ('3_LITIGIOUS', _("Litigious")),
            ('4_CANCELED', _("Canceled")),)

    lead = models.ForeignKey(Lead)
    amount = models.DecimalField(_(u"Amount (k€ excl tax)"), max_digits=10, decimal_places=3)
    due_date = models.DateField(_("Due date"))
    creation_date = models.DateField(_("Creation date"), default=date.today())
    payment_date = models.DateField(_("Payment date"), blank=True, null=True)
    state = models.CharField(_("State"), max_length=30, choices=BILL_STATE, default="1_SENT")
    comment = models.CharField(_("Comments"), max_length=500, blank=True, null=True)

    def __unicode__(self):
        return u"%s/%s" % (self.lead, self.id)

    def save(self, force_insert=False, force_update=False):
        if self.state == "2_PAID":
            self.payment_date = date.today()
        super(Bill, self).save(force_insert, force_update)
