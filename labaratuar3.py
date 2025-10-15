class DiziPaneli:
    def __init__(self, parent):
        self.dizi_panel = tk.Frame(parent)
        
        # Updated Listbox definitions
        self.sari_dizi_listbox = tk.Listbox(self.dizi_panel, height=5, selectmode="extended")
        self.siyah_dizi_listbox = tk.Listbox(self.dizi_panel, height=5, selectmode="extended")
        
        # ... rest of your existing code ...
