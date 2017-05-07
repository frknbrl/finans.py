# -*- coding: utf-8 -*-

#Kutuphaneler

import re, urllib
import smtplib
import os
import time
import time
from datetime import datetime

import datetime
import html as html
from lxml import html
import requests

import smtplib


#Kodlar

print ("########################################################################################################\n"
       "########################################################################################################\n"
       "##" + " " * 35 + " FINANSAL VERI IZLEME PROGRAMI " + " " * 34 + "##" + "\n" 
       "##" + " " * 100 + "##" + "\n"
       "##" + " " * 100 + "##" + "\n"
       "##" + " " * 46 + "Merhabalar," + " " * 43 + "##" + "\n"
       "##" + " " * 11 + "Bu programla istediginiz altin, doviz veya hissenin anlik verisini gorebilir," + " " * 12 + "##" + "\n"
       "##" + " " * 11 + "belirlediginiz fiyat araliginda bilgilendirme alabilirsiniz." + " " * 29 + "##" + "\n"
       "##" + " " * 11 + "Lutfen degerini gormek istediginiz altin, doviz veya hisse icin oncelikle" + " " * 16 + "##" + "\n"
       "##" + " " * 11 + "veri karsiliginin numarasini giriniz." + " " * 52 + "##" + "\n"
       "##" + " " * 11 + "***Not : Hisseler icin lutfen hissenin kodunu dogru giriniz." + " " * 29 + "##" + "\n"
       "##" + " " * 11 + "***Not : Turkce karakter kullanmayiniz!!!" + " " * 48 + "##" + "\n"

       "##" + " " * 100 + "##" + "\n"
       "##" + " " * 100 + "##" + "\n"
       "##" + " " * 100 + "##" + "\n"
       "##" + " " * 40 + "Author  : Furkan Birol  " + " " * 36 + "##" + "\n"
       "##" + " " * 40 + "Version : 1.0  " + " " * 45 + "##" + "\n"
       "##" + " " * 40 + "Date    : 2017  " + " " * 44 + "##" + "\n"
       "########################################################################################################\n"
       "########################################################################################################\n"
       )

now = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")

#Connect to Mail Server
def baglan():
    sunucu = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    sunucu.login("furkanbiroll@gmail.com", "48586745366_f")
    return sunucu


input_type0 = " (0) - Sonucu Goster"
input_type1 = " (1) - Hisse"
input_type2 = " (2) - Doviz"
input_type3 = " (3) - Altin"
input_type4 = " (4) - Cikis"
input_type_End = " (q) - Bitir"

print input_type0
print input_type1
print input_type2
print input_type3
print input_type4
#print input_type_End

input_type_list = []
input_list = []
input_group = []

l = 1

while True:

    selected_input_type_number = raw_input("\nTakip etmek istediginiz finans ogesinin numarasini giriniz (Sonucu gormek icin 0) : ")
    if selected_input_type_number == "0":
        break
    elif selected_input_type_number == "q" or selected_input_type_number == "4":
        quit()

    else:
        input = raw_input("\n" + str(l) + ". Veri :")

    if selected_input_type_number == "1":
        selected_input_type = "Hisse"
    elif selected_input_type_number == "2":
        selected_input_type = "Doviz"
    elif selected_input_type_number == "3":
        selected_input_type = "Altin"
    else:
        print "\nLutfen dogru bir veri tipi giriniz. Ornek : 'Altin' veya 'Hisse' veya 'Doviz' icin esdegeri numara girilmelidir\n\n"

    print "\nSecilen " + str(l) + ". veri tipi : " + selected_input_type + "\n"
    print "Secilen " + str(l) + ". veri      : " + input + "\n"

    inputs = [selected_input_type, input]

    input_type_list.append(selected_input_type)
    input_list.append(input)

    input_group.append(inputs)

    l = l + 1

if len(input_list) < 1:

    print("\nEn az 1 veri girmelisiniz!\n")

else:

    x = 0
    y = 1
    w = 0

    send_Mail_Boolean = 0

    while w < 5:

        for value in input_group:

            if input_group[x][0] == "Hisse":

                main_page = 'http://bigpara.hurriyet.com.tr/borsa/hisse-fiyatlari/'
                page = main_page + input_group[x][1] + "-detay/"
                req_page = requests.get(page)
                tree = html.fromstring(req_page.content)

                hisseDurum = tree.xpath('//*[@id="content"]/div[2]/div[4]/text/ul/li[1]/span/text()')

                hYuzde = tree.xpath('//*[@id="content"]/div[2]/div[4]/text/ul/li[2]/span/text()')

                def hisseSonDurum():
                    i = 0
                    hisseAlisFiyati = hisseDurum[i]
                    return hisseAlisFiyati

                def hisseYuzde():
                    i = 0
                    yuzdeDegisim = hYuzde[i]
                    return yuzdeDegisim

                now = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")

                #Display in Console

                print "\n--------------- " + input_group[x][1] + " Hisse Fiyati ---------------"
                print "-"*50
                print " | " + hisseSonDurum() + "  | " + " "*7 + " | " + hisseYuzde() + " | " + str(now) + " | "
                print "-" * 50

                #Send an e-mail

                global latestValueString, latestValueArray, latestValueFloat
                latestValueString = hisseYuzde()
                latestValueArray = latestValueString.partition("%")
                latestValueFloat = float(latestValueArray[0].replace(',', '.'))

                if latestValueFloat > 1:
                    if send_Mail_Boolean == 0:

                        def mailgonder():
                            sunucu = baglan()

                            gonderici = "furkanbiroll@gmail.com"
                            alici = "furkanbirol1905@gmail.com"
                            konu = "\n\nALIM VEYA SATIM FIRSATI OLABİLİR!!!\n"
                            icerik = "\n\n" + input_group[x][1] + " " + latestValueString + "  oldu!" + \
                                     "\n\nAlım veya Satım firsati olabilir. \n\nSon durum asagidaki gibidir:\n\n" + \
                                     "Tarih                   : " + str(now) + \
                                     "\n" + "Fiyati                  : " + hisseSonDurum() + \
                                     "\n" + "Yüzdelik Değişim  : " + hisseYuzde()
                            mail = """
                                    Gönderen:   %s
                                    Konu:       %s
                                    Mesaj:      %s
                            """ % (gonderici, konu, icerik)

                            try:
                                # maili gönderiyoruz. Aldığı parametreler gonderenin mail adresi, alıcının mail adresi, ve mail içeriği
                                sunucu.sendmail(gonderici, alici, mail)
                                print "Mail basarili bir sekilde gonderildi."
                            except EOFError:
                                print "Mail gonderilirken hata olustu."

                            sunucu.quit()

                        # mail gönder fonksiyonunu çağırdık
                        mailgonder()
                        send_Mail_Boolean = 1
                    else:
                        pass
                else:
                    pass

                    #Write to Database

            elif input_group[x][0] == "Doviz":

                page = requests.get('http://bigpara.hurriyet.com.tr/doviz/%s/' % (input_group[x][1]))
                tree = html.fromstring(page.content)

                veriSatis = tree.xpath('//*[@id="content"]/div[2]/div[1]/div[2]/div[2]/span[2]/text()')
                veriAlis = tree.xpath('//*[@id="content"]/div[2]/div[1]/div[2]/div[3]/span[2]/text()')
                vYuzde = tree.xpath('//*[@id="content"]/div[2]/div[1]/div[2]/div[4]/span[3]/text()')

                def satisSonDurum():
                    j = 0
                    satisFiyati = veriSatis[j]
                    return satisFiyati

                def alisSonDurum():
                    i = 0
                    alisFiyati = veriAlis[i]
                    return alisFiyati

                def veriYuzde():
                    i = 0
                    yuzdeDegisim = vYuzde[i]
                    return yuzdeDegisim

                now = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")

                #Display in Console
                print "\n--------------- " + input_group[x][1] + " Doviz Fiyati ---------------"
                print "-"*50
                print " | " + satisSonDurum() + " | " + alisSonDurum() + " | " + veriYuzde() + " | " + str(now) + " | "
                print "-"*50

                #Send an e-mail

                #global latestValueString, latestValueArray, latestValueFloat
                latestValueString = veriYuzde()
                latestValueArray = latestValueString.partition("%")
                latestValueFloat = float(latestValueArray[0].replace(',', '.'))

                if latestValueFloat > 5:
                    if send_Mail_Boolean == 0:

                        def baglan():
                            sunucu = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                            sunucu.login("furkanbiroll@gmail.com", "48586745366_f")
                            return sunucu

                        def mailgonder():
                            sunucu = baglan()

                            gonderici = "furkanbiroll@gmail.com"
                            alici = "furkanbirol1905@gmail.com"
                            konu = "\n\nALIM VEYA SATIM FIRSATI OLABİLİR!!!\n"
                            icerik = "\n\n" + input_group[x][1] + " " + latestValueString + "  oldu!" + \
                                     "\n\nAlım veya Satım firsati olabilir. \n\nSon durum asagidaki gibidir:\n\n" + \
                                     "Tarih                   : " + str(now) + \
                                     "\n" + "Satış Fiyati            : " + satisSonDurum() + \
                                     "\n" + "Alış Fiyati             : " + alisSonDurum() + \
                                     "\n" + "Yüzdelik Değişim  : " + veriYuzde()
                            mail = """
                                    Gönderen:   %s
                                    Konu:       %s
                                    Mesaj:      %s
                            """ % (gonderici, konu, icerik)

                            try:
                                # maili gönderiyoruz. Aldığı parametreler gonderenin mail adresi, alıcının mail adresi, ve mail içeriği
                                sunucu.sendmail(gonderici, alici, mail)
                                print "Mail basarili bir sekilde gonderildi."
                            except EOFError:
                                print "Mail gonderilirken hata olustu."

                            sunucu.quit()

                        # mail gönder fonksiyonunu çağırdık
                        mailgonder()
                        send_Mail_Boolean = 1
                    else:
                        pass
                else:
                    pass

                    #Write to Database

            elif input_group[x][0] == "Altin":

                main_page = 'http://bigpara.hurriyet.com.tr/altin/'
                page = main_page + input_group[x][1] + "-altin-fiyati/"
                req_page = requests.get(page)
                tree = html.fromstring(req_page.content)

                veriSatis = tree.xpath('//*[@id="content"]/div[2]/div[1]/div[2]/div[2]/span[2]/text()')
                veriAlis = tree.xpath('//*[@id="content"]/div[2]/div[1]/div[2]/div[3]/span[2]/text()')
                vYuzde = tree.xpath('//*[@id="content"]/div[2]/div[1]/div[2]/div[4]/span[3]/text()')

                def satisSonDurum():
                    j = 0
                    satisFiyati = veriSatis[j]
                    return satisFiyati

                def alisSonDurum():
                    i = 0
                    alisFiyati = veriAlis[i]
                    return alisFiyati

                def veriYuzde():
                    i = 0
                    yuzdeDegisim = vYuzde[i]
                    return yuzdeDegisim

                now = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")

                #Display in Console
                print "\n--------------- " + input_group[x][1] + " Altin Fiyati ---------------"
                print "-"*50
                print " | " + satisSonDurum() + " | " + alisSonDurum() + " | " + veriYuzde() + " | " + str(now) + " | "
                print "-"*50

                #Send an e-mail

                #global latestValueString, latestValueArray, latestValueFloat
                latestValueString = veriYuzde()
                latestValueArray = latestValueString.partition("%")
                latestValueFloat = float(latestValueArray[0].replace(',', '.'))

                if latestValueFloat > 5:
                    if send_Mail_Boolean == 0:

                        def baglan():
                            sunucu = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                            sunucu.login("furkanbiroll@gmail.com", "48586745366_f")
                            return sunucu

                        def mailgonder():
                            sunucu = baglan()

                            gonderici = "furkanbiroll@gmail.com"
                            alici = "furkanbirol1905@gmail.com"
                            konu = "\n\nALIM VEYA SATIM FIRSATI OLABİLİR!!!\n"
                            icerik = "\n\n" + input_group[x][1] + " " + latestValueString + "  oldu!" + \
                                     "\n\nAlım veya Satım firsati olabilir. \n\nSon durum asagidaki gibidir:\n\n" + \
                                     "Tarih                   : " + str(now) + \
                                     "\n" + "Satış Fiyati            : " + satisSonDurum() + \
                                     "\n" + "Alış Fiyati             : " + alisSonDurum() + \
                                     "\n" + "Yüzdelik Değişim  : " + veriYuzde()
                            mail = """
                                    Gönderen:   %s
                                    Konu:       %s
                                    Mesaj:      %s
                            """ % (gonderici, konu, icerik)

                            try:
                                # maili gönderiyoruz. Aldığı parametreler gonderenin mail adresi, alıcının mail adresi, ve mail içeriği
                                sunucu.sendmail(gonderici, alici, mail)
                                print "Mail basarili bir sekilde gonderildi."
                            except EOFError:
                                print "Mail gonderilirken hata olustu."

                            sunucu.quit()

                        # mail gönder fonksiyonunu çağırdık
                        mailgonder()
                        send_Mail_Boolean = 1
                    else:
                        pass
                else:
                    pass

                    #Write to Database

            else:

                print "\nLutfen dogru bir veri tipi giriniz. Ornek : 'Altin' veya 'Hisse' veya 'Doviz' icin esdegeri numara girilmelidir\n\n"

            time.sleep(1)

            x = x + 1

        x = 0
        w = w + 1

        print "\n" + "%" * 50

        time.sleep(5)
