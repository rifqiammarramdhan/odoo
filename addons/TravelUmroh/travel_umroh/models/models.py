from odoo import _, api, fields, models


class TravelPackage(models.Model):
    _name = "travel.package"
    _description = "TravelPackage"

    tanggal_berangkat = fields.Date("Tanggal Berangkat", required=True)
    tanggal_kembali = fields.Date("Tanggal Kembali", required=True)

    sale_id = fields.Many2one("product.product", string="Sale")
    package_id = fields.Many2one("product.product", string="Package")

    quota = fields.Integer("Quota")
    remaining_quota = fields.Integer(
        "Remaining Quota", compute="_compute_remaining_quota"
    )

    quota_progress = fields.Float("Quota Progress", compute="compute_quota_progress")

    # Jamaah
    jamaah_ids = fields.Many2many(
        "res.partner",
        "travelpackage_jamaah_rel",
        "travel_package_id",
        "partner_id",
        "Peserta",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    nama_hotel = fields.Many2one("product.product", string="Nama Hotel")
    check_in_hotel = fields.Date("Check In")
    check_out_hotel = fields.Date("Check Out")

    hotel_line = fields.One2many("hotel.line", "travel_package_id", string="Hotel Line")
    airline_line = fields.One2many(
        "airline.line", "travel_package_id", string="Airline Line"
    )
    schedule_lines = fields.One2many(
        "schedule.lines", "travel_package_id", string="Schedule Lines"
    )
    hpp_lines = fields.One2many("hpp.lines", "travel_package_id", string="Hpp Lines")

    # @api.depends("jamaah_ids")
    # def _compute_taken_seats(self):
    #     for package in self:
    #         package.taken_seats = len(package.jamaah_ids)

    @api.depends("quota", "jamaah_ids")
    def compute_quota_progress(self):
        for package in self:
            if package.quota > 0:
                package.quota_progress = 100 * len(package.jamaah_ids) / package.quota
            else:
                package.quota_progress = 0.0

    @api.depends("quota", "jamaah_ids")
    def _compute_remaining_quota(self):
        for package in self:
            package.remaining_quota = package.quota - len(package.jamaah_ids)
