from odoo import api, fields, models, _


class Achat(models.Model):   
    _inherit='purchase.order'
    
   
    
    timbre_fiscal=fields.Float('Timbre Fiscal',default=0.500)
    
    
    
    @api.model
    def _amount_all(self):

        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                # FORWARDPORT UP TO 10.0
                if order.company_id.tax_calculation_rounding_method == 'round_globally':
                    taxes = line.taxes_id.compute_all(line.price_unit, line.order_id.currency_id, line.product_qty, product=line.product_id, partner=line.order_id.partner_id)
                    amount_tax += sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
                else:
                    amount_tax += line.price_tax
            order.update({
                'amount_untaxed': order.currency_id.round(amount_untaxed),
                'amount_tax': order.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax + 0.500,
            })    
        
        

