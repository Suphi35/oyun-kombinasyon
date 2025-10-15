import tkinter as tk
from tkinter import ttk, messagebox
from itertools import combinations

class OyunKombinasyonUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Oyun Kombinasyon Uygulaması")
        self.root.geometry("800x600")
        
        # Ana frame
        self.ana_frame = tk.Frame(root, padx=10, pady=10)
        self.ana_frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlık
        baslik = tk.Label(self.ana_frame, text="Oyun Kombinasyon Uygulaması", 
                         font=("Arial", 16, "bold"))
        baslik.pack(pady=10)
        
        # Dizi paneli oluştur
        self.dizi_paneli = DiziPaneli(self.ana_frame)
        self.dizi_paneli.dizi_panel.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Kontrol paneli
        self.kontrol_paneli_olustur()
        
        # Sonuç paneli
        self.sonuc_paneli_olustur()
        
    def kontrol_paneli_olustur(self):
        kontrol_frame = tk.Frame(self.ana_frame)
        kontrol_frame.pack(pady=10)
        
        # Kombinasyon boyutu
        tk.Label(kontrol_frame, text="Kombinasyon Boyutu:").grid(row=0, column=0, padx=5)
        self.kombinasyon_boyut = tk.Spinbox(kontrol_frame, from_=1, to=10, width=10)
        self.kombinasyon_boyut.grid(row=0, column=1, padx=5)
        self.kombinasyon_boyut.delete(0, tk.END)
        self.kombinasyon_boyut.insert(0, "3")
        
        # Kombinasyon oluştur butonu
        tk.Button(kontrol_frame, text="Kombinasyon Oluştur", 
                 command=self.kombinasyon_olustur, bg="green", fg="white",
                 font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5)
        
        # Temizle butonu
        tk.Button(kontrol_frame, text="Temizle", 
                 command=self.temizle).grid(row=0, column=3, padx=5)
        
    def sonuc_paneli_olustur(self):
        sonuc_frame = tk.LabelFrame(self.ana_frame, text="Sonuçlar", padx=10, pady=10)
        sonuc_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Sonuç Listbox - Çoklu seçim desteğiyle
        scrollbar = tk.Scrollbar(sonuc_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.sonuc_listbox = tk.Listbox(sonuc_frame, height=10, 
                                        yscrollcommand=scrollbar.set,
                                        selectmode="extended")
        self.sonuc_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.sonuc_listbox.yview)
        
    def kombinasyon_olustur(self):
        try:
            # Seçilen sarı dizileri al
            sari_secimler = self.dizi_paneli.sari_dizi_listbox.curselection()
            siyah_secimler = self.dizi_paneli.siyah_dizi_listbox.curselection()
            
            if not sari_secimler and not siyah_secimler:
                messagebox.showwarning("Uyarı", "Lütfen en az bir dizi seçin!")
                return
            
            # Seçilen elemanları al
            secilen_elemanlar = []
            for idx in sari_secimler:
                secilen_elemanlar.append(self.dizi_paneli.sari_dizi_listbox.get(idx))
            for idx in siyah_secimler:
                secilen_elemanlar.append(self.dizi_paneli.siyah_dizi_listbox.get(idx))
            
            # Kombinasyon boyutu
            boyut = int(self.kombinasyon_boyut.get())
            
            if boyut > len(secilen_elemanlar):
                messagebox.showerror("Hata", 
                    f"Kombinasyon boyutu ({boyut}) seçilen eleman sayısından ({len(secilen_elemanlar)}) büyük olamaz!")
                return
            
            # Kombinasyonları oluştur
            kombinasyonlar = list(combinations(secilen_elemanlar, boyut))
            
            # Sonuçları göster
            self.sonuc_listbox.delete(0, tk.END)
            for i, komb in enumerate(kombinasyonlar, 1):
                self.sonuc_listbox.insert(tk.END, f"{i}. {' - '.join(komb)}")
            
            messagebox.showinfo("Başarılı", 
                f"{len(kombinasyonlar)} adet kombinasyon oluşturuldu!")
            
        except ValueError as e:
            messagebox.showerror("Hata", f"Geçersiz giriş: {str(e)}")
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")
    
    def temizle(self):
        self.sonuc_listbox.delete(0, tk.END)
        self.dizi_paneli.sari_dizi_listbox.selection_clear(0, tk.END)
        self.dizi_paneli.siyah_dizi_listbox.selection_clear(0, tk.END)

class DiziPaneli:
    def __init__(self, parent):
        self.dizi_panel = tk.Frame(parent)
        
        # Sarı dizi paneli
        sari_frame = tk.LabelFrame(self.dizi_panel, text="Sarı Diziler", 
                                   padx=10, pady=10)
        sari_frame.grid(row=0, column=0, padx=10, sticky="nsew")
        
        # Sarı dizi Listbox - Çoklu seçim desteği ile (Shift + Ctrl)
        sari_scrollbar = tk.Scrollbar(sari_frame)
        sari_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.sari_dizi_listbox = tk.Listbox(sari_frame, height=10, 
                                            yscrollcommand=sari_scrollbar.set,
                                            selectmode="extended")
        self.sari_dizi_listbox.pack(fill=tk.BOTH, expand=True)
        sari_scrollbar.config(command=self.sari_dizi_listbox.yview)
        
        # Sarı dizilere örnek veriler ekle
        sari_diziler = [
            "Sarı-1", "Sarı-2", "Sarı-3", "Sarı-4", "Sarı-5",
            "Sarı-6", "Sarı-7", "Sarı-8", "Sarı-9", "Sarı-10"
        ]
        for dizi in sari_diziler:
            self.sari_dizi_listbox.insert(tk.END, dizi)
        
        # Siyah dizi paneli
        siyah_frame = tk.LabelFrame(self.dizi_panel, text="Siyah Diziler", 
                                    padx=10, pady=10)
        siyah_frame.grid(row=0, column=1, padx=10, sticky="nsew")
        
        # Siyah dizi Listbox - Çoklu seçim desteği ile (Shift + Ctrl)
        siyah_scrollbar = tk.Scrollbar(siyah_frame)
        siyah_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.siyah_dizi_listbox = tk.Listbox(siyah_frame, height=10, 
                                             yscrollcommand=siyah_scrollbar.set,
                                             selectmode="extended")
        self.siyah_dizi_listbox.pack(fill=tk.BOTH, expand=True)
        siyah_scrollbar.config(command=self.siyah_dizi_listbox.yview)
        
        # Siyah dizilere örnek veriler ekle
        siyah_diziler = [
            "Siyah-1", "Siyah-2", "Siyah-3", "Siyah-4", "Siyah-5",
            "Siyah-6", "Siyah-7", "Siyah-8", "Siyah-9", "Siyah-10"
        ]
        for dizi in siyah_diziler:
            self.siyah_dizi_listbox.insert(tk.END, dizi)
        
        # Grid yapılandırması
        self.dizi_panel.grid_columnconfigure(0, weight=1)
        self.dizi_panel.grid_columnconfigure(1, weight=1)
        
        # Açıklama etiketi
        aciklama = tk.Label(self.dizi_panel, 
                           text="Çoklu seçim için: Ctrl + fare (tekil) veya Shift + fare (blok seçim)",
                           font=("Arial", 9, "italic"), fg="blue")
        aciklama.grid(row=1, column=0, columnspan=2, pady=5)

def main():
    root = tk.Tk()
    uygulama = OyunKombinasyonUygulamasi(root)
    root.mainloop()

if __name__ == "__main__":
    main()
