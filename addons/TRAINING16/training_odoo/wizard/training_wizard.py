from odoo import api, fields, models


class TrainingWizard(models.TransientModel):  # TransientModel = Bersifat sementara
    _name = "training.wizard"
    _description = "Training Wizard"

    def _default_sesi(self):
        # Mencara session ID yang Active
        return self.env["training.session"].browse(self._context.get("active_ids"))

    session_id = fields.Many2one(
        "training.session", string="Sesi", default=_default_sesi
    )
    attendee_ids = fields.Many2many("training.attendee", string="Peserta")

    # menambahkan banyak siswa di semua sessi
    session_ids = fields.Many2many(
        "training.session", string="Sesi", default=_default_sesi
    )

    def tambah_banyak_peserta(self):
        for sesi in self.session_ids:
            sesi.attendee_ids |= self.attendee_ids

    def tambah_peserta(self):
        # Menambahkan Id Yang belum ada saja, Jika data sudah ada maka di skip
        self.session_id.attendee_ids |= self.attendee_ids

    def cron_expire_session(self):
        now = fields.Date.today()
        expired_ids = self.env["training.session"].search(
            [("end_date", "<", now), ("state", "=", "open")]
        )
        expired_ids.write({"state": "done"})
