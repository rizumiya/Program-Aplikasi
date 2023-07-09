from . import scan_module


class AdvanceScanModule(scan_module):
    def __init__(self):
        super().__init__()
        # Inisialisasi variable awal
        self.autosave = 0
        self.order_sid = None
        self.classroom_name = "Regular"
        self.total_student = 999
        self.subject_1 = ""
        self.subject_2 = None
        self.behaviour = "regular multiple choice"

        # Ambil data Subject dari database


        