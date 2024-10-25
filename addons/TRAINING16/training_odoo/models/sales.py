# imo
from odoo import _, api, fields, models


# oomodel
class Sales(models.Model):
    _inherit = "sale.order"

    company = fields.Char(string="company")


# Jika ingin menambahkan field baru di page order line
class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    test_line = fields.Char(string="test line")
