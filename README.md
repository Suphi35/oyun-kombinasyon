# Oyun Kombinasyon Uygulaması

Tkinter tabanlı bir oyun kombinasyon oluşturma uygulamasıdır.

## Özellikler

- **Sarı Diziler**: 10 adet sarı dizi elemanı
- **Siyah Diziler**: 10 adet siyah dizi elemanı
- **Çoklu Seçim Desteği**: Tüm Listbox'larda `selectmode="extended"` ile:
  - **Ctrl + fare tıklaması**: Tekil çoklu seçim (birden fazla elemanı tek tek seçme)
  - **Shift + fare tıklaması**: Blok seçim (bir aralıktaki tüm elemanları seçme)
- **Kombinasyon Oluşturma**: Seçilen elemanlardan belirtilen boyutta kombinasyonlar oluşturma
- **Sonuç Görüntüleme**: Oluşturulan kombinasyonları liste halinde görüntüleme

## Kullanım

### Gereksinimler

- Python 3.x
- Tkinter (Python ile birlikte gelir)

### Çalıştırma

```bash
python3 labaratuar3.py
```

### Nasıl Kullanılır?

1. **Sarı Diziler** veya **Siyah Diziler** listesinden elemanları seçin:
   - Tek eleman seçmek için: Eleman üzerine tıklayın
   - Çoklu eleman seçmek için: 
     - **Ctrl tuşunu basılı tutarak** seçmek istediğiniz elemanlara tek tek tıklayın
     - **Shift tuşunu basılı tutarak** bir aralık seçin (ilk elemanı tıklayın, sonra son elemanı tıklayın)

2. **Kombinasyon Boyutu** alanında kaç elemanlı kombinasyon istediğinizi belirleyin

3. **Kombinasyon Oluştur** butonuna tıklayın

4. Sonuçlar, **Sonuçlar** bölümünde listelenecektir

5. Seçimleri ve sonuçları temizlemek için **Temizle** butonunu kullanın

## Kod Yapısı

### Ana Sınıflar

- **OyunKombinasyonUygulamasi**: Ana uygulama sınıfı
  - Kontrol paneli
  - Sonuç paneli
  - Kombinasyon oluşturma mantığı

- **DiziPaneli**: Sarı ve siyah dizi listelerini yöneten sınıf
  - Sarı dizi Listbox (`selectmode="extended"`)
  - Siyah dizi Listbox (`selectmode="extended"`)

### Listbox Yapılandırması

Tüm Listbox'lar `selectmode="extended"` ile yapılandırılmıştır:

```python
self.sari_dizi_listbox = tk.Listbox(sari_frame, height=10, 
                                    yscrollcommand=sari_scrollbar.set,
                                    selectmode="extended")

self.siyah_dizi_listbox = tk.Listbox(siyah_frame, height=10, 
                                     yscrollcommand=siyah_scrollbar.set,
                                     selectmode="extended")

self.sonuc_listbox = tk.Listbox(sonuc_frame, height=10, 
                                yscrollcommand=scrollbar.set,
                                selectmode="extended")
```

Bu yapılandırma sayesinde:
- **Ctrl + fare** ile çoklu tekil seçim
- **Shift + fare** ile blok seçim
özellikleri otomatik olarak etkinleştirilir.

## Lisans

Bu proje açık kaynaklıdır.
