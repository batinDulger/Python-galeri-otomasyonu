import sqlite3
import time


class Araba():

    def __init__(self):
        
        self.DataBase()
        self.Admin()
        self.Arabalar()
        self.Kayitli_musteriler()
        self.giris_secim()

    def DataBase(self):
        self.con = sqlite3.connect("Car.db")
        self.cursor = self.con.cursor()

    def Admin(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS admin(Isim TEXT, Soyisim TEXT, admin TEXT, sifre TEXT, Tel_no INT, E_Posta TEXT)")

    def Arabalar(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS arabalar(ID INT, Marka TEXT, Model TEXT, Model_Yili INT, HP INT, Renk TEXT, Fiyat INT)")

    def Kayitli_musteriler(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS kayitli_musteriler(Isim TEXT, Soyisim TEXT, Tel_no INT, E_Posta TEXT, sifre INT)")

    def giris_secim(self):

        secenek = input("1.Müşteri Girişi\n2.admin Girişi\nSeçim:")
        
        if secenek == "1":
            self.musteri_girisi()
        elif secenek == "2":
            self.Admin_sign_in()

    def musteri_girisi(self):

        e_posta = input("E-Posta:")
        sifre = int(input("Şifre:"))

        self.cursor.execute("SELECT * FROM kayitli_musteriler WHERE E_Posta = ? AND sifre = ?",(e_posta,sifre))

        musteri = self.cursor.fetchone()

        while True:
            if(musteri):
                secenek = input("1.Kataloğu İncele\n2.Test Sürüşüne Çık\n3.Araba al\n4.Şikayette bulun\n5.Çıkış\nSeçenek:")

                if secenek == "1":
                    self.cursor.execute("SELECT * FROM arabalar")
                    cars = self.cursor.fetchall()
                    for car in cars:
                        print(f"Marka:{car[1]} - Model:{car[2]} - Model Yılı:{car[3]} - HP:{car[4]} - Renk:{car[5]} - Fiyat:{car[6]}")
                elif secenek == "2":
                    time.sleep(1)
                    self.cursor.execute("SELECT * FROM arabalar")
                    cars = self.cursor.fetchall()
                    for car in cars:
                        print(f"Marka:{car[1]} - Model:{car[2]} - Model Yılı:{car[3]} - HP:{car[4]} - Renk:{car[5]}")
                        deneme = input("Seçim:")
                        if deneme == car[0] and deneme == car[1] and deneme == car[4]:
                            print("Araç satıldı")
                    else:
                        time.sleep(1)
                        print("Araç bulunamadı")

                elif secenek == "3":                    
                    self.cursor.execute("SELECT * FROM arabalar")
                    cars = self.cursor.fetchall()
                    for car in cars:
                        print(f"Marka:{car[1]} - Model:{car[2]} - Model Yılı:{car[3]} - HP:{car[4]} - Renk:{car[5]} - Fiyat:{car[6]}")
                    arac_markasi = input("Aracın markası:")
                    arac_modeli = input("Aracın modeli:")
                    arac_renk = input("Araç renk:")
                    if arac_markasi == car[1] and arac_modeli == car[2] and arac_renk == car[3]:
                        self.cursor.execute("DELETE FROM arabalar WHERE marka = ? and model = ? and renk = ?",(arac_markasi,arac_modeli,arac_renk))
                        self.con.commit()
                    else:
                        print("Araç Bulunamadı")
                        continue

                elif secenek == "4":

                    sikayet = input("Şikayetiniz Nedir ?")
                    print(f"{sikayet} incelenmek üzere tarafımıza gönderilmiştir.")

                elif secenek == "5":
                    print("Çıkış Yapılıyor")
                    time.sleep(1)
                    print("Çıkış yapıldı")

    ##### Admin işlemleri #####

    def Admin_sign_in(self):

        admin = input("Admin:")
        sifre = input("Şifre:")

        while True:
            self.cursor.execute("SELECT * FROM Admin WHERE admin = ? AND sifre = ?",(admin,sifre))
            user = self.cursor.fetchone()
            if(user):
                secim = input("1-)Araba Girişi Yap\n2-)Araba Satışı\n3-)Kataloğu İncele\n4-)Araba Güncelle\n5-)Çıkış\nSeçim:")
                if secim == "1":
                    self.araba_kaydet()
                elif secim == "2":
                    self.arac_satis()
                elif secim == "3":
                    self.cursor.execute("SELECT * FROM arabalar")
                    cars = self.cursor.fetchall()
                    for car in cars:
                        print(f"Marka:{car[1]} - Model:{car[2]} - Model Yılı:{car[3]} - HP:{car[4]} - Renk:{car[5]} - Fiyat:{car[6]}")
                elif secim == "4":
                    self.arac_guncelle()
                elif secim == "5":
                    self.con.close()
                    break
            else:
                print("Tekrar Dene")
                self.Admin_sign_in()

    def araba_kaydet(self):

        Id = int(input("ID:"))
        Marka = input("Marka:")
        Model = input("Model:")
        Model_Yili = int(input("Model Yılı:"))
        Hp = int(input("HP:"))
        Renk = input("Renk:")
        Fiyat = int(input("Fiyat:"))

        self.cursor.execute("INSERT INTO arabalar VALUES(?,?,?,?,?,?,?)",(Id,Marka,Model,Model_Yili,Hp,Renk,Fiyat))
        self.con.commit()

    def arac_satis(self):

        self.cursor.execute("SELECT * FROM arabalar")
        cars = self.cursor.fetchall()
        for car in cars:
            print(f"Marka:{car[1]} - Model:{car[2]} - Model Yılı:{car[3]} - HP:{car[4]} - Renk:{car[5]} - Fiyat:{car[6]}")
        
        arac_markasi = input("Aracın markası:")
        arac_modeli = input("Aracın modeli:")
        arac_renk = input("Araç renk:")
        if arac_markasi == car[0] and arac_modeli == car[1] and arac_renk == car[4]:
            self.cursor.execute("DELETE FROM arabalar WHERE marka = ? and model = ? and renk = ?",(arac_markasi,arac_modeli,arac_renk))
            self.con.commit()
        else:
            print("Araç Bulunamadı")

    def arac_guncelle(self):

        guncellenecek_araba = input("1-)Marka Değiştir\n2-)Model Değiştir\n3-)HP Değiştir\n4-)Renk Değiştir\n5-)Fiyat Değiştir\nSeçim:")

        if guncellenecek_araba == "1":
            self.cursor.execute("SELECT * FROM arabalar")
            cars = self.cursor.fetchall()
            for car in cars:
                print(f"Id:{car[0]} - Marka:{car[1]} - Model:{car[2]} - Model Yılı:{car[3]} - HP:{car[4]} - Renk:{car[5]} - Fiyat:{car[6]}")
            id_sec = int(input("Güncellenecek Arabanın Id numarasını seçiniz:"))

            selected_car = None
            for car in cars:
                if car[0] == id_sec:
                    selected_car = car
                    break

            if selected_car:
                yeni_marka = input("Marka:")
                yeni_model = input("Model:")
                yeni_model_yili = int(input("Model Yılı:"))
                H_p = int(input("HP:"))
                renk = input("Renk:")
                fiyat = int(input("Fiyat:"))

                self.cursor.execute("UPDATE arabalar SET Marka = ?, Model = ?, Model_yili = ?, HP = ?, Renk = ?, Fiyat = ? WHERE ID = ?",
                                    (yeni_marka, yeni_model, yeni_model_yili, H_p, renk, fiyat, id_sec))
                self.con.commit()
            else:
                print("Araba bulunamadı.")
        ##########################################
        elif guncellenecek_araba == "2":

            self.cursor.execute("SELECT * FROM arabalar")
            cars = self.cursor.fetchall()
            for car in cars:
                print(f"Id:{car[0]} - Marka:{car[1]} - Model:{car[2]} - Model Yılı:{car[3]} - HP:{car[4]} - Renk:{car[5]} - Fiyat:{car[6]}")

            guncellenecek_arabanin_id_numarası = input("Güncellencek aracın id numarasını giriniz:")
            self.cursor.execute("SELECT * FROM arabalar WHERE ID = ?",(guncellenecek_arabanin_id_numarası,))
            control = self.cursor.fetchone()

            if control:
                guncellenecek_model = input("Model:")
                self.cursor.execute("UPDATE arabalar SET Model = ? WHERE ID = ?",(guncellenecek_model,guncellenecek_arabanin_id_numarası))
                self.con.commit()
            else:
                print("Hatalı id girişi")
                    
        ##########################################
        elif guncellenecek_araba == "3":

            self.cursor.execute("SELECT * FROM arabalar")
            cars = self.cursor.fetchall()
            for car in cars:
                print(f"Id:{car[0]} - Marka:{car[1]} - Model:{car[2]} - Model Yılı:{car[3]} - HP:{car[4]} - Renk:{car[5]} - Fiyat:{car[6]}")

            guncellenecek_arabanin_id_numarası = input("Güncellencek aracın id numarasını giriniz:")
            self.cursor.execute("SELECT * FROM arabalar WHERE ID = ?",(guncellenecek_arabanin_id_numarası,))
            control = self.cursor.fetchone()

            if control:
                guncellenecek_hp = input("HP:")
                self.cursor.execute("UPDATE arabalar SET HP = ? WHERE ID = ?",(guncellenecek_hp,guncellenecek_arabanin_id_numarası))
                self.con.commit()
            else:
                print("Hatalı id girişi")
        ##########################################
        elif guncellenecek_araba == "4":

            self.cursor.execute("SELECT * FROM arabalar")
            cars = self.cursor.fetchall()
            for car in cars:
                print(f"Id:{car[0]} - Marka:{car[1]} - Model:{car[2]} - Model Yılı:{car[3]} - HP:{car[4]} - Renk:{car[5]} - Fiyat:{car[6]}")
            
            guncellenecek_arabanin_id_numarası = input("Güncellencek aracın id numarasını giriniz:")
            self.cursor.execute("SELECT * FROM arabalar WHERE ID = ?",(guncellenecek_arabanin_id_numarası,))
            control = self.cursor.fetchone()

            if control:
                guncellenecek_renk = input("Renk:")
                self.cursor.execute("UPDATE arabalar SET Renk = ? WHERE ID = ?",(guncellenecek_renk,guncellenecek_arabanin_id_numarası))
                self.con.commit()
            else:
                print("Hatalı id girişi")
        ##########################################
        elif guncellenecek_araba == "5":

            self.cursor.execute("SELECT * FROM arabalar")
            cars = self.cursor.fetchall()
            for car in cars:
                print(f"Id:{car[0]} - Marka:{car[1]} - Model:{car[2]} - Model Yılı:{car[3]} - HP:{car[4]} - Renk:{car[5]} - Fiyat:{car[6]}")

            guncellenecek_arabanin_id_numarası = input("Güncellencek aracın id numarasını giriniz:")
            self.cursor.execute("SELECT * FROM arabalar WHERE ID = ?",(guncellenecek_arabanin_id_numarası,))
            control = self.cursor.fetchone()

            if control:
                guncellenecek_fiyat = int(input("Fiyat:"))
                self.cursor.execute("UPDATE arabalar SET Fiyat = ? WHERE ID = ?",(guncellenecek_fiyat,guncellenecek_arabanin_id_numarası))
                self.con.commit()
            else:
                print("Hatalı id girişi")

if __name__ == "__main__":
    app = Araba()