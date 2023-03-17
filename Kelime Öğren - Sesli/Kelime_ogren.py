

#------------------------------------------------------------------------ KÜTÜPHANELER
#------------------------------------------------------------------------
import speech_recognition as sr
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from AnaSayfaUI import *
from KelimeYokUI import *
import sqlite3
import random
import sys


#------------------------------------------------------------------------ VERİTABANI
#------------------------------------------------------------------------
global db, imlec
db = sqlite3.connect("english_database.db")
imlec = db.cursor()
imlec.execute("CREATE TABLE IF NOT EXISTS kelimeler (english,turkish)")
imlec.execute("CREATE TABLE IF NOT EXISTS ogrenilen_kelimeler (learned_english,learned_turkish)")


#------------------------------------------------------------------------ UYGULAMA
#------------------------------------------------------------------------
uygulama = QApplication(sys.argv)
penAna = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(penAna)
penAna.show()

penUyari1 = QDialog()
ui2 = Ui_KelimeYok()
ui2.setupUi(penUyari1)


#------------------------------------------------------------------------ GEREKEN VERİLER
#------------------------------------------------------------------------
ing_list = []
tr_list = []
global bitir,uyarı_gösterme,ses_kontrol,dil
uyarı_göster = True
bitir = False
ses_kontrol = False

def dinle(dil):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        ui.statusbar.showMessage("KONUŞUN..",10000)
        r.adjust_for_ambient_noise(source)
        data = r.record(source,duration=3)
    try:
        ses_cevap = r.recognize_google(data,language = dil)
        ui.statusbar.showMessage("Kelime : " + ses_cevap.upper(),5000)
    except sr.UnknownValueError:
        ses_cevap = ""
        ui.statusbar.showMessage("SİZİ DUYAMADIM :(",6000)
    except sr.RequestError as e:
        ui.statusbar.showMessage("HATA VAR :(",6000)
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return ses_cevap.lower()

def kelime_sayısı():
    imlec.execute("SELECT english FROM kelimeler ")
    veriler = imlec.fetchall()
    return len(veriler)

def gecici_liste():
    ing_list = []
    tr_list = []
    imlec.execute("SELECT english FROM kelimeler ")
    ing_veri = imlec.fetchall()
    imlec.execute("SELECT turkish FROM kelimeler ")
    tr_veri = imlec.fetchall()
    for i in range(len(ing_veri)):
        a=str(ing_veri[i])
        a=a[2:-3]
        b=str(tr_veri[i])
        b=b[2:-3]
        ing_list.append(a.lower())
        tr_list.append(b.lower())
    return ing_list, tr_list

def kelime_yok_uyarı():
    ui2.label.setStyleSheet("color: Default; font: 14pt;")
    ui2.label.setText("Kayıtlı kelime yok. Lütfen kelime ekleyin..")
    ui2.label_2.setText("UYARI !!")
    penUyari1.show()

def test_bitti_uyari():
    ui2.label.setStyleSheet("color: rgb(255, 0, 0); font: 16pt; ")
    ui2.label.setText("Test Bitti.")
    ui2.label_2.setText("")
    penUyari1.show()



####################################################################################################################
##################################### Öğrenmeye Başla #####################################

#------------------------------------------------------------------------ BAŞLA-BİTİR SEÇİMİ
#------------------------------------------------------------------------
def BASLA_BITIR_ING():
    global bitir
    if bitir == False:
        BASLA_ING()
    elif bitir == True:
        BITIR_ING()
        
def BASLA_BITIR_TR():
    global bitir, baslamadan_bitir
    if bitir == False:
        BASLA_TR()
    elif bitir == True:
        BITIR_TR()
        
def BASLA_BITIR_KARMA():
    global bitir
    if bitir == False:
        BASLA_KARMA()
    elif bitir == True:
        BITIR_KARMA()

#------------------------------------------------------------------------ BAŞLA
#------------------------------------------------------------------------
def BASLA_ING():
    kelime_sayi = kelime_sayısı()
    global ing_list, tr_list,bitir
    if kelime_sayi == 0:
        kelime_yok_uyarı()
    else:
        bitir = True
        ui.btn_ing_basla.setText("BİTİR")
        ing_list, tr_list = gecici_liste()
        ui.btn_ing_sor.setText("SOR("+str(len(ing_list))+")")
        ui.btn_ing_sor.setEnabled(True)
        ui.btn_ing_kontrol.setEnabled(True)
        ui.line_ing_cvb.setEnabled(True)
        ui.btn_ing_ses.setEnabled(True)
        ui.btn_tr_basla.setEnabled(False)
        ui.btn_sf_basla.setEnabled(False)
        ING_SOR()
        
def BASLA_TR():
    kelime_sayi = kelime_sayısı()
    global ing_list, tr_list,bitir
    if kelime_sayi == 0:
        kelime_yok_uyarı()
    else:
        bitir = True
        ui.btn_tr_basla.setText("BİTİR")
        ing_list, tr_list = gecici_liste()
        ui.btn_tr_sor.setText("SOR("+str(len(ing_list))+")")
        ui.btn_tr_sor.setEnabled(True)
        ui.btn_tr_kontrol.setEnabled(True)
        ui.line_tr_cvb.setEnabled(True)
        ui.btn_tr_ses.setEnabled(True)
        ui.btn_ing_basla.setEnabled(False)
        ui.btn_sf_basla.setEnabled(False)
        TR_SOR()

def BASLA_KARMA():
    kelime_sayi = kelime_sayısı()
    global ing_list, tr_list, bitir
    if kelime_sayi == 0:
        kelime_yok_uyarı()
    else:
        bitir = True
        ui.btn_sf_basla.setText("BİTİR")
        ing_list, tr_list = gecici_liste()
        ui.btn_sf_sor.setText("SOR("+str(len(ing_list))+")")
        ui.btn_sf_sor.setEnabled(True)
        ui.btn_sf_kontrol.setEnabled(True)
        ui.line_sf_cvb.setEnabled(True)
        ui.btn_sf_ses.setEnabled(True)
        ui.btn_tr_basla.setEnabled(False)
        ui.btn_ing_basla.setEnabled(False)
        KARMA_SOR()

#------------------------------------------------------------------------ SOR
#------------------------------------------------------------------------
def ING_SOR():
    global ing_list, tr_list, deger, cevap, kelime_sor, bitir, uyarı_göster
    if len(ing_list)==0:
        ui.btn_ing_sor.setText("SOR")
        ui.lbl_ing_sor.clear()
        ui.lbl_ing_sonuc.clear()
        ui.lbl_ing_sonuc_3.clear()
        if uyarı_göster == True:
            test_bitti_uyari()
        ui.btn_ing_basla.setText("BAŞLA")
        ui.btn_tr_basla.setEnabled(True)
        ui.btn_sf_basla.setEnabled(True)
        ui.btn_ing_sor.setEnabled(False)
        ui.btn_ing_kontrol.setEnabled(False)
        ui.line_ing_cvb.setEnabled(False)
        ui.btn_ing_ses.setEnabled(False)
    else:
        deger = random.randrange(0,len(ing_list))
        kelime_sor = ing_list[deger]
        cevap = tr_list[deger]
        ui.lbl_ing_sor.setText(kelime_sor)

def TR_SOR():
    global ing_list, tr_list, deger, cevap, kelime_sor, bitir, uyarı_göster
    if len(ing_list) == 0:
        ui.btn_tr_sor.setText("SOR")
        ui.lbl_tr_sor.clear()
        ui.lbl_tr_sonuc.clear()
        ui.lbl_tr_sonuc_3.clear()
        if uyarı_göster == True:
            test_bitti_uyari()
        ui.btn_tr_basla.setText("BAŞLA")
        ui.btn_ing_basla.setEnabled(True)
        ui.btn_sf_basla.setEnabled(True)
        ui.btn_tr_sor.setEnabled(False)
        ui.btn_tr_kontrol.setEnabled(False)
        ui.line_tr_cvb.setEnabled(False)
        ui.btn_tr_ses.setEnabled(False)
    else:
        deger = random.randrange(0,len(ing_list))
        kelime_sor = tr_list[deger]
        cevap = ing_list[deger]
        ui.lbl_tr_sor.setText(kelime_sor)

def KARMA_SOR():
    global ing_list, tr_list, deger, cevap, kelime_sor, bitir, uyarı_göster, dil
    if len(ing_list) == 0:
        ui.btn_sf_sor.setText("SOR")
        ui.lbl_sf_sor.clear()
        ui.lbl_sf_sonuc.clear()
        ui.lbl_sf_sonuc_3.clear()
        if uyarı_göster == True:
            test_bitti_uyari()
        ui.btn_sf_basla.setText("BAŞLA")
        ui.line_sf_cvb.setPlaceholderText("")
        ui.btn_tr_basla.setEnabled(True)
        ui.btn_ing_basla.setEnabled(True)
        ui.btn_sf_sor.setEnabled(False)
        ui.btn_sf_kontrol.setEnabled(False)
        ui.line_sf_cvb.setEnabled(False)
        ui.btn_sf_ses.setEnabled(False)
    else:
        deger = random.randrange(0,len(ing_list))
        dil_secim = random.randint(0,1)
        if dil_secim == 0:
            kelime_sor = ing_list[deger]
            cevap = tr_list[deger]
            dil = "tr"
            ui.line_sf_cvb.setPlaceholderText("Türkçesi ?")
        else:
            kelime_sor = tr_list[deger]
            cevap = ing_list[deger]
            dil = "eng"
            ui.line_sf_cvb.setPlaceholderText("İngilizcesi ?")
        ui.lbl_sf_sor.setText(kelime_sor)


#------------------------------------------------------------------------ KONTROL ET
#------------------------------------------------------------------------
def ING_KONTROL():
    global  ses_kontrol,cevabim
    if ses_kontrol == False:
        cevabim = ui.line_ing_cvb.text().lower()
    if cevap == cevabim:
        ui.lbl_ing_sonuc.setStyleSheet("")
        ui.lbl_ing_sonuc.setText(" DOĞRU " + cevabim )
        ui.lbl_ing_sonuc_3.clear()
        del tr_list[deger], ing_list[deger]
        ui.btn_ing_sor.setText("SOR("+str(len(ing_list))+")")
    if cevap != cevabim:
        ui.lbl_ing_sonuc.setStyleSheet("color: rgb(255, 0, 0);")
        ui.lbl_ing_sonuc.setText(cevabim + " YANLIŞ")
        ui.lbl_ing_sonuc_3.setText(kelime_sor + ":" + cevap)
    ING_SOR()
    ui.line_ing_cvb.clear()
    
def TR_KONTROL():
    global  ses_kontrol,cevabim
    if ses_kontrol == False:
        cevabim = ui.line_tr_cvb.text().lower()
    if cevap == cevabim:
        ui.lbl_tr_sonuc.setStyleSheet("")
        ui.lbl_tr_sonuc.setText(" DOĞRU " + cevabim )
        ui.lbl_tr_sonuc_3.clear()
        del tr_list[deger], ing_list[deger]
        ui.btn_tr_sor.setText("SOR("+str(len(ing_list))+")")
    if cevap != cevabim:
        ui.lbl_tr_sonuc.setStyleSheet("color: rgb(255, 0, 0);")
        ui.lbl_tr_sonuc.setText(cevabim + " YANLIŞ")
        ui.lbl_tr_sonuc_3.setText(kelime_sor + "->" + cevap)
    TR_SOR()
    ui.line_tr_cvb.clear()

def KARMA_KONTROL():
    global  ses_kontrol,cevabim
    if ses_kontrol == False:
        cevabim = ui.line_sf_cvb.text().lower()
    if cevap == cevabim:
        ui.lbl_sf_sonuc.setStyleSheet("")
        ui.lbl_sf_sonuc.setText(" DOĞRU " + cevabim )
        ui.lbl_sf_sonuc_3.clear()
        del tr_list[deger], ing_list[deger]
        ui.btn_sf_sor.setText("SOR("+str(len(ing_list))+")")
    if cevap != cevabim:
        ui.lbl_sf_sonuc.setStyleSheet("color: rgb(255, 0, 0);")
        ui.lbl_sf_sonuc.setText(cevabim + " YANLIŞ")
        ui.lbl_sf_sonuc_3.setText(kelime_sor + "->" + cevap)
    KARMA_SOR()
    ui.line_sf_cvb.clear()

#------------------------------------------------------------------------ BİTİR
#------------------------------------------------------------------------
def BITIR_ING():
    global ing_list, tr_list, bitir, uyarı_göster
    uyarı_göster = False
    bitir = False
    ing_list,tr_list = [],[]
    ING_SOR()

def BITIR_TR():
    global ing_list, tr_list, bitir, uyarı_göster
    uyarı_göster = False
    bitir = False
    ing_list,tr_list = [],[]
    TR_SOR()

def BITIR_KARMA():
    global ing_list, tr_list, bitir, uyarı_göster
    uyarı_göster = False
    bitir = False
    ing_list,tr_list = [],[]
    KARMA_SOR()


def SES_ING():
    global ses_kontrol, cevabim
    ses_kontrol = True
    cevabim = dinle("tr")
    if cevabim != "" :
        ING_KONTROL()
    ses_kontrol = False

def SES_TR():
    global ses_kontrol, cevabim
    ses_kontrol = True
    cevabim = dinle("eng")
    if cevabim != "" :
        TR_KONTROL()
    ses_kontrol = False
    
def SES_KARMA():
    global ses_kontrol, cevabim,dil
    ses_kontrol = True
    cevabim = dinle(dil)
    if cevabim != "" :
        KARMA_KONTROL()
    ses_kontrol = False


###################################################################################################################
##################################### Kelime Listesi #####################################
def KELIME_LISTE():
    ui.listw_kelime.clear()
    imlec.execute("SELECT * FROM kelimeler")
    veriler = imlec.fetchall()
    for veri in veriler:
        ui.listw_kelime.addItem(veri[0].lower() + " : " + veri[1].lower())
    ui.lbl_kelime_sayisi.setText(str(kelime_sayısı()))
    ui.line_ing_duzelt.clear()
    ui.line_tr_duzelt.clear()
    ui.line_ing_ekle.clear()
    ui.line_tr_ekle.clear()

def KELIME_EKLE():
    ing_kelime = ui.line_ing_ekle.text().lower()
    tr_kelime = ui.line_tr_ekle.text().lower()
    if bool(ing_kelime)==False or bool(tr_kelime)==False:
        pass
    else:
        sorgu = "INSERT INTO kelimeler VALUES ('{}','{}') ".format(ing_kelime,tr_kelime)
        imlec.execute(sorgu)
        db.commit()
        KELIME_LISTE()

def KELIME_SIL():
    secili = ui.listw_kelime.selectedItems()
    if bool(secili) == True: 
        cevap_sil = QMessageBox().question(penAna,"KELİME SİL","Kelimeyi silmek istediğinize emin misiniz?",\
                    QMessageBox.Yes | QMessageBox.No )
        if cevap_sil == QMessageBox.Yes:
            secili_str = secili[0].text()
            silinecek = ""
            for i in secili_str:
                if i == ':' :
                    silinecek = silinecek[0:-1]
                    break
                silinecek += i
            try:
                imlec.execute("DELETE FROM kelimeler WHERE english='{}' ".format(silinecek))
                db.commit()
                ui.statusbar.showMessage("SİLME İŞLEMİ BAŞARILI...",6000)
                KELIME_LISTE()
            except Exception as hata:
                ui.statusbar.showMessage("SİLME SIRASINDA HATA İLE KARŞILAŞILDI: "+str(hata),10000)
        else:
            ui.statusbar.showMessage("SİLME İŞLEMİ İPTAL EDİLDİ...",6000)

def KELIME_DOLDUR():
    secili = ui.listw_kelime.selectedItems()
    if bool(secili) == True:
        secili_str = secili[0].text()
        ing_verb = ""
        for i in secili_str:
            if i == ":" :
                ing_verb = ing_verb[0:-1]
                break
            ing_verb += i
        imlec.execute("SELECT * FROM kelimeler WHERE english='{}'".format(ing_verb))
        verb = imlec.fetchone()
        ui.line_ing_duzelt.setText(verb[0])
        ui.line_tr_duzelt.setText(verb[1])

def KELIME_DUZELT():
    secili = ui.listw_kelime.selectedItems()
    if bool(secili) == True:
        secili_str = secili[0].text().lower()
        ing_aranan = ""
        for i in secili_str:
            if i == ':' :
                ing_aranan = ing_aranan[0:-1]
                break
            ing_aranan += i
        ing_verb = ui.line_ing_duzelt.text().lower()
        tr_verb = ui.line_tr_duzelt.text().lower()
        imlec.execute("UPDATE kelimeler SET english='{}',turkish='{}' WHERE english='{}'".format(ing_verb,tr_verb,ing_aranan))
        db.commit()
        KELIME_LISTE()

def KELIME_OGRENILDI():
    secili = ui.listw_kelime.selectedItems()
    if bool(secili) == True: 
        cevap_sil = QMessageBox().question(penAna,"UYARI","Kelime öğrenilenler listesine eklenecek?",\
                    QMessageBox.Yes | QMessageBox.No )
        if cevap_sil == QMessageBox.Yes:
            secili_str = secili[0].text()
            silinecek = ""
            for i in secili_str:
                if i == ':' :
                    silinecek = silinecek[0:-1]
                    break
                silinecek += i
            imlec.execute("SELECT * FROM kelimeler WHERE english='{}'".format(silinecek))
            verb = imlec.fetchone()
            try:
                imlec.execute("DELETE FROM kelimeler WHERE english='{}' ".format(silinecek))
                imlec.execute("INSERT INTO ogrenilen_kelimeler VALUES ('{}','{}')".format(verb[0],verb[1]))
                db.commit()
                ui.statusbar.showMessage("İŞLEM BAŞARIYLA GERÇEKLEŞTİ...",6000)
                KELIME_LISTE()
            except Exception as hata:
                ui.statusbar.showMessage("İŞLEM SIRASINDA HATA İLE KARŞILAŞILDI: "+str(hata),10000)
        else:
            ui.statusbar.showMessage("İŞLEMİ İPTAL EDİLDİ...",6000)
        KELIME_LISTE()
        KELIME_OGRENILEN_LISTE()
        

###################################################################################################################
##################################### Öğrenilenler Listesi ###################################
def KELIME_OGRENILEN_LISTE():
    ui.listw_ogrenilen.clear()
    imlec.execute("SELECT * FROM ogrenilen_kelimeler")
    veriler = imlec.fetchall()
    for veri in veriler:
        ui.listw_ogrenilen.addItem(veri[0] + " : " + veri[1])
    imlec.execute("SELECT COUNT(*) FROM ogrenilen_kelimeler")
    sayi = imlec.fetchone()
    ui.lbl_ogrenilen_sayisi.setText(str(sayi[0]))

def TEKRAR_OGREN():
    secili = ui.listw_ogrenilen.selectedItems()
    if bool(secili) == True:
        secili_str = secili[0].text()
        silinecek = ""
        for i in secili_str:
            if i == ':' :
                silinecek = silinecek[0:-1]
                break
            silinecek += i
        imlec.execute("SELECT * FROM ogrenilen_kelimeler WHERE learned_english='{}'".format(silinecek))
        verb = imlec.fetchone()
        imlec.execute("INSERT INTO kelimeler VALUES ('{}','{}')".format(verb[0],verb[1]))
        imlec.execute("DELETE FROM ogrenilen_kelimeler WHERE learned_english='{}'".format(silinecek))
        db.commit()
        KELIME_LISTE()
        KELIME_OGRENILEN_LISTE()

def OGRENILEN_SIL():
    secili = ui.listw_ogrenilen.selectedItems()
    if bool(secili) == True:
        secili_str = secili[0].text()
        silinecek = ""
        for i in secili_str:
            if i == ':' :
                silinecek = silinecek[0:-1]
                break
            silinecek += i
        imlec.execute("DELETE FROM ogrenilen_kelimeler WHERE learned_english='{}'".format(silinecek))
        db.commit()
    KELIME_OGRENILEN_LISTE()

KELIME_OGRENILEN_LISTE()
KELIME_LISTE()


###################################################################################################################
##################################### BUTON KONTROLÜ ###################################

ui.btn_ing_basla.clicked.connect(BASLA_BITIR_ING)
ui.btn_ing_sor.clicked.connect(ING_SOR)
ui.btn_ing_kontrol.clicked.connect(ING_KONTROL)
ui.line_ing_cvb.returnPressed.connect(ING_KONTROL)
ui.btn_ing_ses.clicked.connect(SES_ING)

ui.btn_tr_basla.clicked.connect(BASLA_BITIR_TR)
ui.btn_tr_sor.clicked.connect(TR_SOR)
ui.btn_tr_kontrol.clicked.connect(TR_KONTROL)
ui.line_tr_cvb.returnPressed.connect(TR_KONTROL)
ui.btn_tr_ses.clicked.connect(SES_TR)

ui.btn_sf_basla.clicked.connect(BASLA_BITIR_KARMA)
ui.btn_sf_sor.clicked.connect(KARMA_SOR)
ui.btn_sf_kontrol.clicked.connect(KARMA_KONTROL)
ui.line_sf_cvb.returnPressed.connect(KARMA_KONTROL)
ui.btn_sf_ses.clicked.connect(SES_KARMA)

ui.btn_sil.clicked.connect(KELIME_SIL)
ui.btn_ekle.clicked.connect(KELIME_EKLE)
ui.listw_kelime.itemClicked.connect(KELIME_DOLDUR)
ui.btn_duzelt_kaydet.clicked.connect(KELIME_DUZELT)
ui.btn_kelime_ogrenildi.clicked.connect(KELIME_OGRENILDI)

ui.btn_tekrar_ogren.clicked.connect(TEKRAR_OGREN)
ui.btn_ogrenildi_sil.clicked.connect(OGRENILEN_SIL)


sys.exit(uygulama.exec())











