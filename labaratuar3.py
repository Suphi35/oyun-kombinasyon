import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
IDEAL_DISTANCE = 120
GEÇİŞ_GECİKMESİ = 35  # ms

class Savasci:
    def __init__(self, root, ana_klasor, x, y, ters_bak=False):
        self.root = root
        self.ana_klasor = ana_klasor
        self.x = x
        self.y = y
        self.ters_bak = ters_bak
        self.animasyonlar = {}
        self.aktif_animasyon = "Yuru"
        self.kare_index = 0
        self.canvas_obj = None
        self.animasyon_bitti = False

    def animasyon_yukle(self):
        for hareket in os.listdir(self.ana_klasor):
            hareket_path = os.path.join(self.ana_klasor, hareket)
            if os.path.isdir(hareket_path):
                kareler = []
                pngler = sorted(
                    [f for f in os.listdir(hareket_path) if f.endswith(".png")],
                    key=lambda x: int(os.path.splitext(x)[0])
                )
                for png in pngler:
                    img = Image.open(os.path.join(hareket_path, png)).resize((256, 256))
                    if self.ters_bak:
                        img = img.transpose(Image.FLIP_LEFT_RIGHT)
                    kareler.append(ImageTk.PhotoImage(img))
                self.animasyonlar[hareket] = kareler

    def canvas_ekle(self, canvas):
        ilk_kare = self.animasyonlar[self.aktif_animasyon][self.kare_index]
        self.canvas_obj = canvas.create_image(self.x, self.y, anchor=tk.NW, image=ilk_kare)

    def animasyon_oynat(self, canvas):
        kareler = self.animasyonlar[self.aktif_animasyon]
        if self.aktif_animasyon == "Yuru":
            self.kare_index = (self.kare_index + 1) % len(kareler)
            canvas.itemconfig(self.canvas_obj, image=kareler[self.kare_index])
            self.animasyon_bitti = False
        else:
            if self.kare_index < len(kareler) - 1:
                self.kare_index += 1
                canvas.itemconfig(self.canvas_obj, image=kareler[self.kare_index])
                self.animasyon_bitti = False
            else:
                self.animasyon_bitti = True

    def animasyon_degistir(self, yeni_anim):
        if yeni_anim in self.animasyonlar:
            self.aktif_animasyon = yeni_anim
            self.kare_index = 0
            self.animasyon_bitti = False

class ArenaLabApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Kombinasyon Editörü")

        # ANA ÜST FRAME
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Sol panel
        self.left_panel = tk.Frame(self.main_frame, width=320, height=WINDOW_HEIGHT, bg="#eef")
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(self.left_panel, text="Kombinasyon Editörü", font=("Arial", 13, "bold"), bg="#eef").pack(pady=(10,5))
        tk.Label(self.left_panel, text="Sarı Hareketi", bg="#eef").pack()
        self.sari_listbox = tk.Listbox(self.left_panel, height=7, exportselection=0)
        self.sari_listbox.pack(fill=tk.X, padx=10)
        tk.Label(self.left_panel, text="Siyah Hareketi", bg="#eef").pack(pady=(10,0))
        self.siyah_listbox = tk.Listbox(self.left_panel, height=7, exportselection=0)
        self.siyah_listbox.pack(fill=tk.X, padx=10)
        tk.Label(self.left_panel, text="Sarı deltaX", bg="#eef").pack(pady=(10,0))
        self.sari_dx_entry = tk.Entry(self.left_panel)
        self.sari_dx_entry.insert(0, "0")
        self.sari_dx_entry.pack(fill=tk.X, padx=10)
        tk.Label(self.left_panel, text="Siyah deltaX", bg="#eef").pack()
        self.siyah_dx_entry = tk.Entry(self.left_panel)
        self.siyah_dx_entry.insert(0, "0")
        self.siyah_dx_entry.pack(fill=tk.X, padx=10)
        self.komb_oynat_btn = tk.Button(self.left_panel, text="Kombinasyonu Oynat", command=self.kombinasyon_oynat)
        self.komb_oynat_btn.pack(fill=tk.X, pady=10, padx=10)
        self.baslangic_btn = tk.Button(self.left_panel, text="Başlangıç Konumu", command=self.ideal_distansa_konumla)
        self.baslangic_btn.pack(fill=tk.X, padx=10, pady=(0,10))

        # Ana canvas
        self.canvas = tk.Canvas(self.main_frame, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.canvas.pack(side=tk.LEFT)
        self.bg_img = Image.open("background.png").resize((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.bg_photo = ImageTk.PhotoImage(self.bg_img)
        self.bg_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

        # Karakterler
        self.sari = Savasci(master, "Poz/Sarı", 200, 420, ters_bak=False)
        self.siyah = Savasci(master, "Poz/Siyah", 200 + IDEAL_DISTANCE, 420, ters_bak=True)
        self.sari.animasyon_yukle()
        self.siyah.animasyon_yukle()
        self.sari.canvas_ekle(self.canvas)
        self.siyah.canvas_ekle(self.canvas)
        self.ideal_distansa_konumla()

        for hareket in sorted(self.sari.animasyonlar.keys()):
            self.sari_listbox.insert(tk.END, hareket)
        for hareket in sorted(self.siyah.animasyonlar.keys()):
            self.siyah_listbox.insert(tk.END, hareket)

        # ALTTA YAN YANA İKİ PANEL
        self.alt_frame = tk.Frame(master, width=WINDOW_WIDTH, height=200, bg="#ddf")
        self.alt_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Dizi paneli (sol)
        self.dizi_panel = tk.Frame(self.alt_frame, width=WINDOW_WIDTH//2, height=180, bg="#ddf")
        self.dizi_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(self.dizi_panel, text="Sarı Dizisi", bg="#ddf").grid(row=0, column=0, sticky="ew", padx=5)
        tk.Label(self.dizi_panel, text="Siyah Dizisi", bg="#ddf").grid(row=0, column=2, sticky="ew", padx=5)
        self.sari_dizi_listbox = tk.Listbox(self.dizi_panel, height=5, selectmode="extended")
        self.sari_dizi_listbox.grid(row=1, column=0, padx=5)
        self.siyah_dizi_listbox = tk.Listbox(self.dizi_panel, height=5, selectmode="extended")
        self.siyah_dizi_listbox.grid(row=1, column=2, padx=5)

        tk.Label(self.dizi_panel, text="Sarı dx").grid(row=2, column=0)
        tk.Label(self.dizi_panel, text="Sarı dy").grid(row=2, column=1)
        tk.Label(self.dizi_panel, text="Siyah dx").grid(row=2, column=2)
        tk.Label(self.dizi_panel, text="Siyah dy").grid(row=2, column=3)

        self.sari_dx_entry2 = tk.Entry(self.dizi_panel, width=5)
        self.sari_dx_entry2.grid(row=3, column=0)
        self.sari_dy_entry2 = tk.Entry(self.dizi_panel, width=5)
        self.sari_dy_entry2.grid(row=3, column=1)
        self.siyah_dx_entry2 = tk.Entry(self.dizi_panel, width=5)
        self.siyah_dx_entry2.grid(row=3, column=2)
        self.siyah_dy_entry2 = tk.Entry(self.dizi_panel, width=5)
        self.siyah_dy_entry2.grid(row=3, column=3)

        self.dizi_ekle_btn = tk.Button(self.dizi_panel, text="Diziye Ekle", command=self.diziye_ekle)
        self.dizi_ekle_btn.grid(row=4, column=0, columnspan=4, sticky="ew", padx=8, pady=2)
        self.dizi_sil_btn = tk.Button(self.dizi_panel, text="Seçili Hamleyi Sil", command=self.diziden_sil)
        self.dizi_sil_btn.grid(row=5, column=0, columnspan=4, sticky="ew", padx=8, pady=2)
        self.dizi_oynat_btn = tk.Button(self.dizi_panel, text="Diziyi Oynat", command=self.diziyi_oynat)
        self.dizi_oynat_btn.grid(row=6, column=0, columnspan=4, sticky="ew", padx=8, pady=2)

        self.sari_dizisi = []
        self.siyah_dizisi = []
        self.dizi_index = 0
        self.dizi_animating = False

        # Kombinasyon Hamle Dökümü paneli (sağ)
        self.kombinasyon_panel = tk.Frame(self.alt_frame, width=WINDOW_WIDTH//2, height=180, bg="#eef")
        self.kombinasyon_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(self.kombinasyon_panel, text="Kombinasyon Hamle Dökümü", font=("Arial", 12, "bold"), bg="#eef").pack(pady=(8,4))
        self.kombinasyon_listbox = tk.Listbox(self.kombinasyon_panel, width=45, height=7, font=("Consolas", 10))
        self.kombinasyon_listbox.pack(padx=8, pady=3)

        self.kombinasyon_ekle_btn = tk.Button(self.kombinasyon_panel, text="Seçili Hamleyi Döküme Ekle", command=self.kombinasyon_hamle_ekle)
        self.kombinasyon_ekle_btn.pack(fill=tk.X, padx=12, pady=2)
        self.kombinasyon_sil_btn = tk.Button(self.kombinasyon_panel, text="Dökümden Sil", command=self.kombinasyon_hamle_sil)
        self.kombinasyon_sil_btn.pack(fill=tk.X, padx=12, pady=2)
        self.kopyala_btn = tk.Button(self.kombinasyon_panel, text="Dökümü Kopyala", command=self.kombinasyon_dokum_kopyala)
        self.kopyala_btn.pack(fill=tk.X, padx=12, pady=4)

        self.kombinasyon_dokum = []

        self.state = "idle"
        self.anim_counter = 0
        self.animate()

    # --- Kombinasyon paneli fonksiyonları ---
    def kombinasyon_hamle_ekle(self):
        sari_ind = self.sari_dizi_listbox.curselection()
        siyah_ind = self.siyah_dizi_listbox.curselection()
        if not sari_ind and not siyah_ind:
            messagebox.showinfo("Uyarı", "Döküme eklemek için en az bir hamle seçmelisin!")
            return
        sari_str = ""
        siyah_str = ""
        if sari_ind:
            sari_str = self.sari_dizi_listbox.get(sari_ind[0])
        if siyah_ind:
            siyah_str = self.siyah_dizi_listbox.get(siyah_ind[0])
        satir = f"{len(self.kombinasyon_dokum)+1} Sarı {sari_str} Siyah {siyah_str}"
        self.kombinasyon_listbox.insert(tk.END, satir)
        self.kombinasyon_dokum.append({
            "sira": len(self.kombinasyon_dokum)+1,
            "sari": sari_str,
            "siyah": siyah_str
        })

    def kombinasyon_hamle_sil(self):
        secim = self.kombinasyon_listbox.curselection()
        if secim:
            self.kombinasyon_listbox.delete(secim[0])
            del self.kombinasyon_dokum[secim[0]]
            # Sıra numaralarını güncelle
            self.kombinasyon_listbox.delete(0, tk.END)
            for i in range(len(self.kombinasyon_dokum)):
                satir = f"{i+1} Sarı {self.kombinasyon_dokum[i]['sari']} Siyah {self.kombinasyon_dokum[i]['siyah']}"
                self.kombinasyon_listbox.insert(tk.END, satir)

    def kombinasyon_dokum_kopyala(self):
        metin = "\n".join([self.kombinasyon_listbox.get(i) for i in range(self.kombinasyon_listbox.size())])
        self.master.clipboard_clear()
        self.master.clipboard_append(metin)
        messagebox.showinfo("Bilgi", "Kombinasyon hamle dökümü panoya kopyalandı!")

    def diziden_sil(self):
        sari_secim = self.sari_dizi_listbox.curselection()
        siyah_secim = self.siyah_dizi_listbox.curselection()
        if sari_secim:
            for index in reversed(sari_secim):
                self.sari_dizi_listbox.delete(index)
                del self.sari_dizisi[index]
        if siyah_secim:
            for index in reversed(siyah_secim):
                self.siyah_dizi_listbox.delete(index)
                del self.siyah_dizisi[index]
        self.dizi_index = 0

    def ideal_distansa_konumla(self):
        ortalama = WINDOW_WIDTH // 2
        self.sari.x = ortalama - IDEAL_DISTANCE // 2
        self.siyah.x = ortalama + IDEAL_DISTANCE // 2
        self.sari.y = 420
        self.siyah.y = 420
        self.canvas.coords(self.sari.canvas_obj, self.sari.x, self.sari.y)
        self.canvas.coords(self.siyah.canvas_obj, self.siyah.x, self.siyah.y)

    def kombinasyon_oynat(self):
        sari_secim = self.sari_listbox.curselection()
        siyah_secim = self.siyah_listbox.curselection()
        if not sari_secim or not siyah_secim:
            messagebox.showinfo("Uyarı", "Her iki karakter için hareket seçmelisin.")
            return
        sari_hareket = self.sari_listbox.get(sari_secim[0])
        siyah_hareket = self.siyah_listbox.get(siyah_secim[0])
        try:
            sari_dx = int(self.sari_dx_entry.get())
            siyah_dx = int(self.siyah_dx_entry.get())
        except ValueError:
            messagebox.showinfo("Uyarı", "deltaX değerleri sayı olmalı.")
            return
        self.ideal_distansa_konumla()
        self.sari.animasyon_degistir(sari_hareket)
        self.siyah.animasyon_degistir(siyah_hareket)
        self.sari.x += sari_dx
        self.siyah.x += siyah_dx
        self.state = "kombinasyon_anim"
        self.anim_counter = 0

    def diziye_ekle(self):
        sari_secim = self.sari_listbox.curselection()
        siyah_secim = self.siyah_listbox.curselection()
        try:
            sari_dx = int(self.sari_dx_entry2.get().strip())
        except ValueError:
            sari_dx = 0
        try:
            sari_dy = int(self.sari_dy_entry2.get().strip())
        except ValueError:
            sari_dy = 0
        try:
            siyah_dx = int(self.siyah_dx_entry2.get().strip())
        except ValueError:
            siyah_dx = 0
        try:
            siyah_dy = int(self.siyah_dy_entry2.get().strip())
        except ValueError:
            siyah_dy = 0
        if sari_secim:
            sari_hareket = self.sari_listbox.get(sari_secim[0])
            self.sari_dizisi.append({"ad": sari_hareket, "dx": sari_dx, "dy": sari_dy})
            self.sari_dizi_listbox.insert(tk.END, f"{sari_hareket} ({sari_dx},{sari_dy})")
        if siyah_secim:
            siyah_hareket = self.siyah_listbox.get(siyah_secim[0])
            self.siyah_dizisi.append({"ad": siyah_hareket, "dx": siyah_dx, "dy": siyah_dy})
            self.siyah_dizi_listbox.insert(tk.END, f"{siyah_hareket} ({siyah_dx},{siyah_dy})")

    def diziyi_oynat(self):
        if not self.sari_dizisi and not self.siyah_dizisi:
            messagebox.showinfo("Uyarı", "Diziyi oynatmak için en az bir hamle eklemelisin.")
            return
        self.ideal_distansa_konumla()
        self.dizi_index = 0
        if self.sari_dizisi:
            hamle = self.sari_dizisi[0]
            self.sari.animasyon_degistir(hamle["ad"])
            self.sari.x += hamle["dx"]
            self.sari.y += hamle["dy"]
        if self.siyah_dizisi:
            hamle = self.siyah_dizisi[0]
            self.siyah.animasyon_degistir(hamle["ad"])
            self.siyah.x += hamle["dx"]
            self.siyah.y += hamle["dy"]
        self.dizi_animating = True

    def animate(self):
        self.canvas.coords(self.sari.canvas_obj, self.sari.x, self.sari.y)
        self.canvas.coords(self.siyah.canvas_obj, self.siyah.x, self.siyah.y)
        if self.dizi_animating:
            sari_hamle_bitti = self.sari.animasyon_bitti
            siyah_hamle_bitti = self.siyah.animasyon_bitti
            self.sari.animasyon_oynat(self.canvas)
            self.siyah.animasyon_oynat(self.canvas)
            if sari_hamle_bitti and siyah_hamle_bitti:
                self.dizi_index += 1
                if self.dizi_index < max(len(self.sari_dizisi), len(self.siyah_dizisi)):
                    if self.dizi_index < len(self.sari_dizisi):
                        hamle = self.sari_dizisi[self.dizi_index]
                        self.sari.animasyon_degistir(hamle["ad"])
                        self.sari.x += hamle["dx"]
                        self.sari.y += hamle["dy"]
                    if self.dizi_index < len(self.siyah_dizisi):
                        hamle = self.siyah_dizisi[self.dizi_index]
                        self.siyah.animasyon_degistir(hamle["ad"])
                        self.siyah.x += hamle["dx"]
                        self.siyah.y += hamle["dy"]
                else:
                    self.dizi_animating = False
                    self.dizi_index = 0
            self.master.after(GEÇİŞ_GECİKMESİ, self.animate)
            return
        self.sari.animasyon_oynat(self.canvas)
        self.siyah.animasyon_oynat(self.canvas)
        self.master.after(50, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = ArenaLabApp(root)
    root.mainloop()
