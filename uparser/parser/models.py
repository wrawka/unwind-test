from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderLine(models.Model):
    """Represents a single order line record from source table."""

    line_no = models.PositiveBigIntegerField(verbose_name=_('Line number'))
    order_no = models.PositiveBigIntegerField(verbose_name=_('Order number'))
    due_date = models.DateField(verbose_name=_('Order due date'))
    value_usd = models.PositiveBigIntegerField(verbose_name=_('Order line value in USD'))
    value_rub = models.FloatField(
        verbose_name=_('Order line value in RUB'), blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['line_no', 'order_no'], name='order_line_pk')
        ]

    def __str__(self) -> str:
        return f'Order line no.{self.order_no}'
