class DiziPaneli:
    def __init__(self, parent):
        self.dizi_panel = tk.Frame(parent)
        
        # Updated Listbox definitions for multi-select
        self.sari_dizi_listbox = tk.Listbox(self.dizi_panel, height=5, selectmode="extended")
        self.siyah_dizi_listbox = tk.Listbox(self.dizi_panel, height=5, selectmode="extended")
        
        # Açıklama:
        # selectmode="extended" ile hem Ctrl + fare tıklamasıyla çoklu tekil seçim
        # hem de Shift + fare ile blok seçim yapılabilir.
        # Tkinter Listbox bu iki davranışı otomatik olarak sağlar.
        # Kodda ekstra bir değişiklik yapmaya gerek yoktur, sadece selectmode="extended" yeterlidir.
        
        # ... rest of your existing code ...
