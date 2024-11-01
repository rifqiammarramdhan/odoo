from odoo import _, api, fields, models
import logging

_logging = logging.getLogger(__name__)


class TravelPackage(models.Model):
    _name = "travel.package"
    _description = "Travel Package"

    ref = fields.Char(string="Referensi", readonly=True, default="/")
    name = fields.Char(string="PO Number", default="New", readonly=True)
    tanggal_berangkat = fields.Date("Tanggal Berangkat", required=True)
    tanggal_kembali = fields.Date("Tanggal Kembali", required=True)

    sale_id = fields.Many2one("product.product", string="Sale")
    product_ids = fields.Many2many("product.product", string="Products")
    mrp_bom_id = fields.Many2one("mrp.bom", string="Mrp Bom")
    sale_order_id = fields.Many2one("sale.order", string="Sale Order")

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
    hpp_lines = fields.One2many("hpp.lines", "travel_package_id", string="HPP Lines")
    manifest_ids = fields.One2many("manifest", "travel_package_id", string="Manifest")

    total_cost = fields.Float(
        string="Total Cost", compute="_compute_total_cost", store=True
    )

    name = fields.Char(string="Package Name")
    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirm", "Confirmed"),
            ("cancel", "Cancelled"),
        ],
        string="Status",
        default="draft",
    )

    def func_confirm(self):
        if self.status == "draft":
            self.name = f"{self.ref}-Umroh Bintang 5"
            self.status = "confirm"

    @api.onchange("ref")
    def _onchange_mrp_bom_id(self):
        if self.name == "New":
            self.name = self.ref + "-" + "Umroh Bintang 5"

    @api.model
    def create(self, vals):
        vals["ref"] = self.env["ir.sequence"].next_by_code("travel.package")
        return super(TravelPackage, self).create(vals)

    # Hitung Total
    @api.depends("mrp_bom_id.bom_line_ids", "hpp_lines.subtotal")
    def _compute_total_cost(self):
        for package in self:
            total = 0.0
            if package.mrp_bom_id:
                # Menghitung total dari hpp_lines yang terkait dengan mrp_bom_id
                total += sum(line.subtotal for line in package.hpp_lines)
            package.total_cost = total

    @api.onchange("mrp_bom_id")
    def _onchange_mrp_bom_id(self):
        # for line in self.hpp_lines:
        #     line.unlink()  # Menghapus semua baris HPP sebelumnya

        if self.mrp_bom_id:
            for bom_line in self.mrp_bom_id.bom_line_ids:
                self.hpp_lines.create(
                    {
                        "travel_package_id": self.id,
                        "barang": bom_line.product_id.name,
                        "quantity": bom_line.product_qty,
                        "units": bom_line.product_uom_id.name,
                        "unit_price": bom_line.product_id.lst_price,
                        "subtotal": bom_line.product_qty
                        * bom_line.product_id.lst_price,
                    }
                )

    def func_update_jamaah(self):
        # for line in self.manifest_ids:
        #     line.unlink()

        # Ambil semua jamaah berdasarkan sale_order_id
        for rec in self:
            lines = [(5, 0, 0)]
            existing_jamaah = self.env["sale.order"].search(
                [("travel_package_id", "=", self.id), ("state", "in", ["sale", "done"])]
            )
            if existing_jamaah:
                for line in existing_jamaah.sale_order_ids:
                    vals = {
                        "title": line.title.name,
                        "nama_panjang": line.name,
                        "jenis_kelamin": line.jenis_kelamin,
                        "no_ktp": line.no_ktp,
                        "no_passport": line.no_passpor,
                        "tanggal_lahir": line.tanggal_lahir,
                        "tempat_lahir": line.tempat_lahir,
                        "tanggal_berlaku": line.tanggal_berlaku,
                        "tanggal_expired": line.tanggal_expired,
                        "imigrasi": line.imigrasi,
                        "tipe_kamar": line.tipe_kamar,
                        "nama_passport": line.nama_passpor,
                        "umur": line.umur,
                        "mahrom_id": line.mahrom_id.id,
                        "agent": line.agent,
                    }
                    lines.append((0, 0, vals))
                rec.write({"manifest_ids": lines})

            #     print("=================================>", line)
            #     self.write(
            #         {
            #             "manifest_ids": [(5, 0, 0)]
            #             + [
            #                 (
            #                     0,
            #                     0,
            #                     {
            #                         "title": line.title.name,
            #                         "nama_panjang": line.name,
            #                         "jenis_kelamin": line.jenis_kelamin,
            #                         "no_ktp": line.no_ktp,
            #                         "no_passport": line.no_passpor,
            #                         "tanggal_lahir": line.tanggal_lahir,
            #                         "tempat_lahir": line.tempat_lahir,
            #                         "tanggal_berlaku": line.tanggal_berlaku,
            #                         "tanggal_expired": line.tanggal_expired,
            #                         "imigrasi": line.imigrasi,
            #                         "tipe_kamar": line.tipe_kamar,
            #                         "nama_passport": line.nama_passpor,
            #                         "umur": line.umur,
            #                         "mahrom_id": line.mahrom_id.id,
            #                         "agent": line.agent,
            #                     },
            #                 )
            #             ]
            #         }
            #     )

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

    # def name_get(self):
    #     result = []
    #     for record in self:
    #         name = record.name or "Travel Package"
    #         result.append((record.id, name))
    #     return result


# Hotel Line
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


# Airline Lines
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


# Schedules Line
class ScheduleLines(models.Model):
    _name = "schedule.lines"
    _description = "Schedule Lines"

    travel_package_id = fields.Many2one(
        "travel.package", string="Travel Package", ondelete="cascade"
    )

    nama_kegiatan = fields.Char("Nama Kegiatan")
    tanggal_kegiatan = fields.Date("Tangal Kegiatan")


# Manifest
class Manifest(models.Model):
    _name = "manifest"
    _description = "Manifest"

    travel_package_id = fields.Many2one(
        "travel.package", string="Travel Package", ondelete="cascade"
    )
    sale_order_id = fields.Many2one("sale.order", string="Sale Order")

    title = fields.Char(string="Title")
    nama_panjang = fields.Char("nama_panjang")
    jenis_kelamin = fields.Char("jenis_kelamin")
    no_ktp = fields.Char("no_ktp")
    no_passport = fields.Char("no_passport")
    tanggal_lahir = fields.Date("tanggal_lahir")
    tempat_lahir = fields.Char("tempat_lahir")
    tanggal_berlaku = fields.Date("tanggal_berlaku")
    tanggal_expired = fields.Date("tanggal_expired")
    imigrasi = fields.Char("Imigrasi")
    nama_passport = fields.Char("nama_passport")
    tipe_kamar = fields.Char("tipe_kamar")
    umur = fields.Char("umur")
    agent = fields.Char("agent")
    notes = fields.Char("notes")
    mahrom_id = fields.Many2one("res.partner", string="Mahrom")

    scan_passpor = fields.Binary(string="Scan Paspor")
    scan_ktp = fields.Binary(string="Scan KTP")
    scan_buku_nikah = fields.Binary(string="Scan Buku Nikah")
    scan_kartu_keluarga = fields.Binary(string="Scan Kartu Keluarga")


# HPP Line
class HppLines(models.Model):
    _name = "hpp.lines"
    _description = "HPP Lines"

    travel_package_id = fields.Many2one(
        "travel.package", string="Travel Package", ondelete="cascade"
    )

    mrp_bom_id = fields.Many2one("mrp.bom", string="BOM")

    barang = fields.Char(string="Barang")
    quantity = fields.Integer("Quantity")
    units = fields.Char("Units")
    unit_price = fields.Float("Unit Price")
    subtotal = fields.Float("Subtotal")


class PassporSaleOrder(models.Model):
    _name = "passpor.sale.order"
    _description = "Passpor Sale Order"

    sale_order_id = fields.Many2one(
        "sale.order", string="Sale Order", ondelete="cascade"
    )

    partner_id = fields.Many2one(
        "res.partner", string="Partner", delegate=True, ondelete="cascade"
    )

    tipe_kamar = fields.Selection(
        [
            ("double", "Double"),
            ("triple", "Triple"),
            ("quad", "Quad"),
        ]
    )

    mahrom_id = fields.Many2one("res.partner", string="Mahrom")
    agent = fields.Char(string="Agent")
    notes = fields.Char("notes")


#  Sales Order
class SaleOrder(models.Model):
    _inherit = "sale.order"

    travel_package_id = fields.Many2one(
        "travel.package", string="Paket Perjalanan", ondelete="cascade"
    )

    jamaah_id = fields.Many2one("res.partner", string="Jamaah", required=True)

    # manifest_ids = fields.One2many("manifest", "sale_order_id", string="Manifest")
    sale_order_ids = fields.One2many(
        "passpor.sale.order", "sale_order_id", string="Sale Order"
    )

    # Action untuk wizard
    def action_open_jamaah_wizard(self):
        # Membuka wizard dengan otomatis mengisi `sale_order_id`
        return {
            "type": "ir.actions.act_window",
            "name": "Pilih Jamaah",
            "res_model": "jamaah.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_sale_order_id": self.id,
            },
        }

    @api.onchange("travel_package_id")
    def _onchange_travel_package_id(self):
        if self.travel_package_id:
            product = self.travel_package_id.sale_id
            if product:
                # Clear existing order lines
                self.order_line = [(5, 0, 0)]

                # Create a new order line for the product in sale_id
                self.order_line = [
                    (
                        0,
                        0,
                        {
                            "product_id": product.id,
                            "name": product.name,
                            "product_uom_qty": 1,
                            "price_unit": product.lst_price,
                        },
                    )
                ]
