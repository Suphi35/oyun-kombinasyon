# Değişiklikler:
# - Dizi panelindeki listbox'lar tekli seçim moduna alındı (selectmode="browse")
# - Seçim eventlerinde senkronizasyon fonksiyonu sadeleştirildi ve multi-seçim engellendi

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
IDEAL_DISTANCE = 120
GEÇİŞ_GECİKMESİ = 35  # ms

class Savasci:
    ...

class ArenaLabApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Kombinasyon Editörü")

        # ... diğer kodlar ...

        # Dizi paneli (sol)
        self.dizi_panel = tk.Frame(self.alt_frame, width=WINDOW_WIDTH//2, height=180, bg="#ddf")
        self.dizi_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(self.dizi_panel, text="Sarı Dizisi", bg="#ddf").grid(row=0, column=0, sticky="ew", padx=5)
        tk.Label(self.dizi_panel, text="Siyah Dizisi", bg="#ddf").grid(row=0, column=2, sticky="ew", padx=5)
        # ---- DİKKAT! Tekli seçim moduna alındı ----
        self.sari_dizi_listbox = tk.Listbox(self.dizi_panel, height=5, selectmode="browse")
        self.sari_dizi_listbox.grid(row=1, column=0, padx=5)
        self.siyah_dizi_listbox = tk.Listbox(self.dizi_panel, height=5, selectmode="browse")
        self.siyah_dizi_listbox.grid(row=1, column=2, padx=5)

        # ... diğer kodlar ...

        # Listbox seçim senkronizasyonu için event binding
        self.sari_dizi_listbox.bind('<<ListboxSelect>>', self._on_sari_dizi_select)
        self.siyah_dizi_listbox.bind('<<ListboxSelect>>', self._on_siyah_dizi_select)

        # ... diğer kodlar ...

    def _sync_listbox_selection(self, source_listbox, target_listbox):
        selection = source_listbox.curselection()
        if selection:
            index = selection[0]
            # Diğer listbox'ta sadece aynı index'i seçili yap!
            target_listbox.selection_clear(0, tk.END)
            if index < target_listbox.size():
                target_listbox.selection_set(index)

    def _on_sari_dizi_select(self, event):
        self._sync_listbox_selection(self.sari_dizi_listbox, self.siyah_dizi_listbox)

    def _on_siyah_dizi_select(self, event):
        self._sync_listbox_selection(self.siyah_dizi_listbox, self.sari_dizi_listbox)

    # ... geri kalan kodlar ...
