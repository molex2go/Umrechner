#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Umrechner – Einheitenumrechner mit Kategorien
Open Source MIT – molex2go
"""
import tkinter as tk
from tkinter import ttk

CATEGORIES = {
    "Länge": {
        "base": "m",
        "units": {"Meter m":1, "Kilometer km":1000, "Zentimeter cm":0.01, "Millimeter mm":0.001, "Meile mi":1609.344, "Yard yd":0.9144, "Fuß ft":0.3048, "Zoll in":0.0254, "Seemeile nmi":1852},
    },
    "Masse": {
        "base":"kg",
        "units":{"Kilogramm kg":1,"Gramm g":0.001,"Tonne t":1000,"Pfund lb":0.45359237,"Unze oz":0.0283495231},
    },
    "Leistung": {
        "base":"W",
        "units":{"Watt W":1,"Kilowatt kW":1000,"Pferdestärke PS":735.49875,"HP hp":745.7},
    },
    "Temperatur": {"is_temp":True, "units":["Celsius °C","Fahrenheit °F","Kelvin K"]},
    "Geschwindigkeit": {
        "base":"m/s",
        "units":{"Meter/s m/s":1,"Kilometer/h km/h":0.277777778,"Meile/h mph":0.44704,"Knoten kn":0.514444},
    },
}

def to_celsius(v,unit):
    if "°C" in unit: return v
    if "°F" in unit: return (v-32)*5/9
    if "K" in unit: return v-273.15
    return v
def from_celsius(c,unit):
    if "°C" in unit: return c
    if "°F" in unit: return c*9/5+32
    if "K" in unit: return c+273.15
    return c

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Umrechner – molex2go")
        self.geometry("560x360")
        self.resizable(False,False)
        self.cat_name = list(CATEGORIES.keys())[0]
        self.build_ui()
        self.change_category(self.cat_name)

    def build_ui(self):
        frm = ttk.Frame(self, padding=12)
        frm.pack(fill="both", expand=True)
        ttk.Label(frm, text="Kategorie").pack(anchor="w")
        self.cat_var = tk.StringVar()
        self.cat_cb = ttk.Combobox(frm, textvariable=self.cat_var, state="readonly")
        self.cat_cb.pack(fill="x", pady=4)
        self.cat_cb["values"] = list(CATEGORIES.keys())
        self.cat_cb.bind("<<ComboboxSelected>>", lambda e: self.change_category(self.cat_var.get()))

        ttk.Label(frm, text="Von").pack(anchor="w", pady=(8,0))
        self.from_var = tk.StringVar()
        self.from_cb = ttk.Combobox(frm, textvariable=self.from_var, state="readonly")
        self.from_cb.pack(fill="x")
        self.from_cb.bind("<<ComboboxSelected>>", lambda e: self.calc())

        ttk.Label(frm, text="Nach").pack(anchor="w", pady=(4,0))
        self.to_var = tk.StringVar()
        self.to_cb = ttk.Combobox(frm, textvariable=self.to_var, state="readonly")
        self.to_cb.pack(fill="x")
        self.to_cb.bind("<<ComboboxSelected>>", lambda e: self.calc())

        ttk.Label(frm, text="Wert").pack(anchor="w", pady=(8,0))
        self.val_var = tk.StringVar()
        self.val_entry = ttk.Entry(frm, textvariable=self.val_var)
        self.val_entry.pack(fill="x")
        self.val_var.trace_add("write", lambda *a: self.calc())

        self.result = ttk.Label(frm, text="—", font=("Segoe UI",16))
        self.result.pack(pady=16)

        self.cat_var.set(self.cat_name)
        self.cat_cb.current(0)

    def change_category(self, name):
        self.cat_name = name
        cat = CATEGORIES[name]
        units = []
        if cat.get("is_temp"):
            units = cat["units"]
        else:
            units = list(cat["units"].keys())
        self.from_cb["values"] = units
        self.to_cb["values"] = units
        if units:
            self.from_var.set(units[0])
            self.to_var.set(units[1] if len(units)>1 else units[0])
        self.calc()

    def calc(self):
        try:
            v = float(self.val_var.get().replace(",","."))
        except:
            self.result.config(text="—")
            return
        cat = CATEGORIES[self.cat_name]
        f = self.from_var.get()
        t = self.to_var.get()
        if cat.get("is_temp"):
            c = to_celsius(v,f)
            out = from_celsius(c,t)
        else:
            units = cat["units"]
            out = v * units[f] / units[t]
        self.result.config(text=f"{v} {f} = {out:.6g} {t}")

if __name__ == "__main__":
    App().mainloop()
