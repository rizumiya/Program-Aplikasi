from assets.libs.utils import kotakContour, getCornerPoints, reorder, splitBoxes, showAnswers, stackImages
import numpy as np
import datetime
import openpyxl
import cv2

# define variables ========================================

imgPath = "../paper/jwb1-10.png"
xlPath = "assets/temps/omray.xlsx"

widthImg = 600
heightImg = 800
kernel = np.ones((5, 5), np.uint8)

questions = 0 # 10
choices = 0 # 5

ansid = 0
ans = [[2, 3, 1, 2, 3, 2, 2, 3, 1, 3],
       [1, 2, 2, 2, 3, 2, 1, 1, 1, 4]]

webcamOn = True
cameraNo = 0
checking = True

now = datetime.datetime.now()
waktu = now.strftime("%Y-%m-%d %H:%M")

def newScanning(questions, choices, ansid, ans, webcamOn, cameraNo, checking):
    grade = 0
    score = 0
    salah = []
    NoW = []

    cap = cv2.VideoCapture(cameraNo)
    cap.set(10, 150)

    while checking:
        if webcamOn:
            success, img = cap.read()
        else:
            img = cv2.imread(imgPath)
        
        # preprocessing 
        img = cv2.resize(img, (widthImg, heightImg))
        imgContourTerbesar = img.copy()
        imgContours = img.copy()
        imgFinal = img.copy()
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
        imgCanny = cv2.Canny(imgBlur, 10, 40)
        imgDilate = cv2.dilate(imgCanny, kernel, iterations=1)

        try:
            # mencari seluruh contour
            contours, hierarchy = cv2.findContours(
                imgDilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10)

            # mencari persegi
            kotakCon = kotakContour(contours)
            contourTerbesar = getCornerPoints(kotakCon[0])

            if contourTerbesar.size != 0:
                cv2.drawContours(imgContourTerbesar, contourTerbesar, 
                                 -1, (0, 255, 0), 20)
                # diurutkan dari kotak terbesar ke terkecil
                contourTerbesar = reorder(contourTerbesar)

                ttk1 = np.float32(contourTerbesar)
                ttk2 = np.float32([[0, 0], [widthImg, 0], 
                                   [0, heightImg], [widthImg, heightImg]])
                matrix = cv2.getPerspectiveTransform(ttk1, ttk2)
                imgWrapBerwarna = cv2.warpPerspective(img, matrix, 
                                                      (widthImg, heightImg))
                
                imgWrapGray = cv2.cvtColor(imgWrapBerwarna, cv2.COLOR_BGR2GRAY)
                imgTresh = cv2.threshold(imgWrapGray, 130, 255,
                                         cv2.THRESH_BINARY_INV)[1]
                kotakan = splitBoxes(imgTresh)

                # cari no zero pixel value di setiap jawaban
                jawabanPixelVal = np.zeros((questions, choices))
                hitC = 0
                hitR = 0

                for gambar in kotakan:
                    if hitC == 0:
                        jawabanPixelVal[hitR][hitC] = 0
                        hitC += 1
                        continue
                        
                    totalPixels = cv2.countNonZero(gambar)
                    jawabanPixelVal[hitR][hitC] = totalPixels
                    
                    hitC += 1
                    if (hitC == choices):
                        hitR += 1
                        hitC = 0

                # mencari nilai index di tiap jawaban
                jawabanIndex = []
                for x in range(0, questions):
                    arr = jawabanPixelVal[x]
                    nilaiJawabanIndex = np.where(arr == np.amax(arr))
                    jawabanIndex.append(nilaiJawabanIndex[0][0])

                # proses penilaian
                penilaian = []
                salah = []
                for x in range(0, questions):
                    if ans[ansid][x] == jawabanIndex[x]:
                        penilaian.append(1)
                    else:
                        penilaian.append(0)
                        salah.append(x + 1)
                
                score = (sum(penilaian)/questions) * 20 # 1 nilai bernilai 2

                # menampilkan jawaban yang benar
                imgHasil = imgWrapBerwarna.copy()
                showAnswers(imgHasil, jawabanIndex, penilaian, ans,
                                  questions, choices, ansid)
                imgGambarMentah = np.zeros_like(imgWrapBerwarna)
                showAnswers(imgGambarMentah, jawabanIndex, penilaian, ans,
                                  questions, choices, ansid)
                invMatrix = cv2.getPerspectiveTransform(ttk2, ttk1)
                imgInWarp = cv2.warpPerspective(imgGambarMentah, invMatrix,
                                                (widthImg, heightImg))
                imgFinal = cv2.addWeighted(imgFinal, 1, imgInWarp, 1, 0)
                cv2.putText(imgFinal, str(int(score)), (25, 100),
                            cv2.FONT_HERSHEY_COMPLEX, 3, (50, 255, 100), 4)
                
            imgBlank = np.zeros_like(img)
            imgArray = ([img, imgGray, imgBlur, imgCanny],
                        [imgContours, imgContourTerbesar, imgWrapBerwarna, imgTresh])
        
        except:
            imgBlank = np.zeros_like(img)
            imgArray = ([img, imgGray, imgBlur, imgCanny],
                        [imgBlank, imgBlank, imgBlank, imgBlank])
        
        imgStacked = stackImages(imgArray, 0.5)
        cv2.imshow("Final Grade", imgFinal)
        cv2.imshow("Stacked images", imgStacked)

        if cv2.waitKey(1) & 0xFF == 13:
            cv2.imwrite("FinalResult.jpg", imgFinal)

            if ansid <= 1:
                grade += score
                i = ansid * 10

                print("Nilai akhir anda : " + str(int(grade)))
                ansid += 1
                for x in range(0, len(salah)):
                    if len(salah) == 0:
                        print("Tidak ada nomor yang salah")
                    else:
                        NoW.append(salah[x] + i)
                        print("Nomor yang salah: " + str(salah[x] + i))


            else:
                # menyimpan data ke sheet 1
                workbook0 = openpyxl.load_workbook(xlPath)
                workbook0._active_sheet_index = 0
                sheet0 = workbook0.active
                sheet0.append([waktu, "Matematika", "7A"])
                workbook0.save(xlPath)
            
                # menyimpan data ke sheet 2
                workbook1 = openpyxl.load_workbook(xlPath)
                workbook1._active_sheet_index = 1
                sheet1 = workbook1.active
                sheet1.append([waktu, "Matematika", "7A", "1900018014", grade, str(NoW)])
                workbook1.save(xlPath)

                checking = False
                webcamOn = False
                cv2.destroyAllWindows()
                # cara menutup layar webcam
                # cara deiconify tkinter beda file

            cv2.waitKey(0)

# newScanning(10, 5, 0, ans, True, 0)


