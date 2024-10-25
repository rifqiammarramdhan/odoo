from odoo import _, api, fields, models


class ScheduleLines(models.Model):
    _name = "schedule.lines"
    _description = "Schedule Lines"

    travel_package_id = fields.Many2one(
        "travel.package", string="Travel Package", ondelete="cascade"
    )

    nama_kegiatan = fields.Char("Nama Kegiatan")
    tanggal_kegiatan = fields.Date("Tangal Kegiatan")
