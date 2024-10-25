from odoo import _, api, fields, models


class AirlineLine(models.Model):
    _name = "airline.line"
    _description = "Airline Line"

    travel_package_id = fields.Many2one(
        "travel.package", string="Travel Package", ondelete="cascade"
    )

    partner_id = fields.Many2one("res.partner", string="Parner")

    tanggal_berangkat = fields.Date(string="Tanggal Berangkat")
    kota_asal = fields.Char(string="Kota Asal")
    kota_tujuan = fields.Char(string="Kota Tujuan")
