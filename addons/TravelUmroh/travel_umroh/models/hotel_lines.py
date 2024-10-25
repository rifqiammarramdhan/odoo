from odoo import _, api, fields, models


class HotelLine(models.Model):
    _name = "hotel.line"
    _description = "HotelLine"

    travel_package_id = fields.Many2one(
        "travel.package", string="Travel Package", ondelete="cascade"
    )

    partner_id = fields.Many2one("res.partner", string="Parner")
    date_check_in = fields.Date(string="Check In Hotel")
    date_check_out = fields.Date(string="Check Out Hotel")
    city = fields.Char(string="Kota", related="partner_id.city")
    is_hotel = fields.Boolean(string="Hotel")
