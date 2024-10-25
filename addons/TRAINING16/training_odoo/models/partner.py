# imo
from odoo import _, api, fields, models


# oomodel
class Partner(models.Model):
    _inherit = "res.partner"

    instructor = fields.Boolean(string="Instructure")
    session_line = fields.One2many(
        "training.session", "partner_id", string="Daftar Mengajar Sesi", readonly=True
    )  # Jika One2Many memerlukan Foreign Key
