from odoo import fields,models,api

class softPurchase(models.Model):
    
    _inherit='purchase.order'
    
    monstate=fields.Selection([('prePurchase','commande fournisseur brouillon'),
                               ('Purchase','commande fournisseur valide')
                                ], string='Status', readonly=True, index=True, copy=False, default='prePurchase', track_visibility='onchange')
    
    @api.multi
    def button_approve(self, force=False):
        self.write({'state': 'purchase'})
        self.write({'monstate': 'Purchase'})
        self._create_picking()
        if self.company_id.po_lock == 'lock':
            self.write({'state': 'done'})
        return {}
    
    
    @api.multi
    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step'\
                    or (order.company_id.po_double_validation == 'two_step'\
                        and order.amount_total < self.env.user.company_id.currency_id.compute(order.company_id.po_double_validation_amount, order.currency_id))\
                    or order.user_has_groups('purchase.group_purchase_manager'):
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
        return True
