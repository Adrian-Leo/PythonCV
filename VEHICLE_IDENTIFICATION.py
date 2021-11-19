import cv2
import numpy as np
from time import sleep
min_lebar=80 #Lebar Minimal Kotak
min_tinggi=80 #Tinggi Minimal Kotak
deteksi = []
offset=6#Error piksel
pos_garis=600 #Posisi Garis
delay=60 #FPS Video
jumlahmobil= 0
def posisi_tengah(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy

cap = cv2.VideoCapture('C:/Users/LEO/Documents/PROGRAMMING/PHYTON1/CV/Roadtraffic.mp4')
substraksibg = cv2.bgsegm.createBackgroundSubtractorMOG()

while True:
    ret, frame1 = cap.read()
    tempo = float(1 / delay)
    sleep(tempo)
    grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (3, 3), 5)
    img_sub = substraksibg.apply(blur)
    dilatasi = cv2.dilate(img_sub, np.ones((5, 5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilatasi1 = cv2.morphologyEx(dilatasi, cv2.MORPH_CLOSE, kernel)
    dilatasi2 = cv2.morphologyEx(dilatasi1, cv2.MORPH_CLOSE, kernel)
    contour, h = cv2.findContours(dilatasi2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.line(frame1, (0, pos_garis), (1200, pos_garis), (255, 150, 10),3)

    for (i, c) in enumerate(contour):
        (x, y, w, h) = cv2.boundingRect(c)
        validasi_contour = (w >= min_lebar) and (h >= min_tinggi)
        if not validasi_contour:
            continue

        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 205, 0), 2)
        titiktengah = posisi_tengah(x, y, w, h)
        deteksi.append(titiktengah)
        cv2.circle(frame1, titiktengah, 10, (0, 0, 255), -1)

    for (x, y) in deteksi:
        if y < (pos_garis + offset) and y > (pos_garis - offset):
            jumlahmobil += 1
            cv2.line(frame1, (25, pos_garis), (1200, pos_garis), (10,127, 255), 3)

        deteksi.remove((x, y))
        print("Jumlah kendaraan saat ini: " +str(jumlahmobil) + " buah")
        cv2.putText(frame1, "Kendaraan: " + str(jumlahmobil), (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,
        (0, 0, 255), 5)
        cv2.imshow("Video Original", frame1)
        cv2.imshow("Detectar", dilatasi2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()