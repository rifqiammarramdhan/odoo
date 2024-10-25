from odoo import _, api, fields, models

import logging

_logger = logging.getLogger(__name__)


class HppLines(models.Model):
    _name = "hpp.lines"
    _description = "HPP Lines"

    travel_package_id = fields.Many2one(
        "travel.package", string="Travel Package", ondelete="cascade"
    )

    mrp_bom_id = fields.Many2one("mrp.bom", string="BOM", compute="_compute_mrp_bom_id")

    mrp_bom_lines = fields.One2many(  # Perbaiki menjadi One2many
        "mrp.bom.line", string="BOM Lines", related="mrp_bom_id.bom_line_ids"
    )

    barang_id = fields.Many2one(
        "product.product", string="Barang", related="mrp_bom_lines.product_id"
    )

    quantity = fields.Integer("Quantity", store=True)
    units = fields.Char("Units", store=True)
    unit_price = fields.Float("Unit Price", store=True)
    subtotal = fields.Float("Subtotal", store=True)

    # quantity = fields.Integer("Quantity", related="barang_id.quantity", store=True)
    # units = fields.Char("Units", related="barang_id.units", store=True)
    # unit_price = fields.Float("Unit Price", related="barang_id.unit_price", store=True)
    # subtotal = fields.Float("Subtotal", related="barang_id.subtotal", store=True)

    @api.depends("travel_package_id")
    def _compute_mrp_bom_id(self):
        for record in self:
            if record.travel_package_id:

                record.mrp_bom_id = record.travel_package_id.package_id
            else:
                record.mrp_bom_id = False
