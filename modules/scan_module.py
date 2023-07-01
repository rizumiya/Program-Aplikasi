import cv2

import config as cfg
from modules import general_functions as func


class scan_module:
    def __init__(self, userp, passw):

        # ambil data setting dan subject
        self.funct = func.Functions()
        setting = self.funct.getSettingData(userp, passw)
        detailSub, jawaban = self.funct.ambilJawaban(self.selectedSub)
        
        # Mengisi variable utama

        # variable setting
        self.idLogin = setting[1]
        self.selectedCamera = setting[2]
        self.selectedSub = setting[3]
        self.showAnswer = setting[4]
        self.autoSave = setting[5]

        # variable subject
        self.bykTanya = detailSub[2]
        self.bykJawab = detailSub[3]
        self.jawaban = jawaban


    def start_scanning(self):
        print("test")

    
        