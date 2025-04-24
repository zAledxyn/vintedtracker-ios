import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkhtmlview import HTMLLabel
import csv
import os
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime
import tempfile

DATA_FILE = "data.csv"
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class VintedApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("VintedTracker")
        self.geometry("900x600")
        self.resizable(False, False)

        self.init_data()

        self.sidebar = ctk.CTkFrame(self, width=150)
        self.sidebar.pack(side="left", fill="y")

        self.content = ctk.CTkFrame(self)
        self.content.pack(side="right", fill="both", expand=True)

        self.current_frame = None

        self.create_sidebar()
        self.show_dashboard()

    def init_data(self):
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Datum", "Artikel", "Einkauf", "Verkauf"])

    def create_sidebar(self):
        ctk.CTkLabel(self.sidebar, text="VintedTracker", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 20))
        ctk.CTkButton(self.sidebar, text="Dashboard", command=self.show_dashboard).pack(pady=5, fill="x", padx=10)
        ctk.CTkButton(self.sidebar, text="Artikelübersicht", command=self.show_article_table).pack(pady=5, fill="x", padx=10)
        ctk.CTkButton(self.sidebar, text="Artikel hinzufügen", command=self.show_add_item).pack(pady=5, fill="x", padx=10)
        ctk.CTkButton(self.sidebar, text="Artikel entfernen", command=self.show_remove_items).pack(pady=5, fill="x", padx=10)
        ctk.CTkButton(self.sidebar, text="Backup exportieren", command=self.export_backup).pack(pady=5, fill="x", padx=10)
        ctk.CTkButton(self.sidebar, text="Backup importieren (Datei)", command=self.import_backup).pack(pady=5, fill="x", padx=10)

    def clear_content(self):
        if self.current_frame:
            self.current_frame.destroy()

    def parse_number(self, text):
        return float(text.replace(",", ".").strip())

    def export_backup(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV-Dateien", "*.csv")])
        if file_path:
            with open(DATA_FILE, "r", newline="") as f_in, open(file_path, "w", newline="") as f_out:
                f_out.write(f_in.read())
            messagebox.showinfo("Export", f"Backup gespeichert unter:\n{file_path}")

    def import_backup(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV-Dateien", "*.csv")])
        if file_path:
            with open(file_path, "r", newline="") as f_in, open(DATA_FILE, "w", newline="") as f_out:
                f_out.write(f_in.read())
            messagebox.showinfo("Import", "Backup erfolgreich importiert!")
            self.show_dashboard()

    def show_dashboard(self):
        self.clear_content()
        frame = ctk.CTkFrame(self.content)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = frame

        ctk.CTkLabel(frame, text="Dashboard Übersicht", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=10)

        df = pd.read_csv(DATA_FILE)
        df["Datum"] = pd.to_datetime(df["Datum"], format="%d.%m.%Y", errors="coerce")
        df = df.dropna(subset=["Datum"])
        df["Gewinn"] = df["Verkauf"] - df["Einkauf"]

        total = df["Gewinn"].sum()
        monat = datetime.now().strftime("%m.%Y")
        df["Monat"] = df["Datum"].dt.strftime("%m.%Y")
        monat_gewinn = df[df["Monat"] == monat]["Gewinn"].sum()

        ctk.CTkLabel(
            frame,
            text=f"Gesamtgewinn: {total:.2f} €     Monatsgewinn: {monat_gewinn:.2f} €",
            font=ctk.CTkFont(size=16)
        ).pack(pady=10)

        chart_path = self.create_plotly_chart(df)
        HTMLLabel(frame, html=f'<iframe src="{chart_path}" width="100%" height="300" frameborder="0"></iframe>').pack(pady=10)

    def show_article_table(self):
        self.clear_content()
        frame = ctk.CTkFrame(self.content)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = frame

        ctk.CTkLabel(frame, text="Artikelübersicht", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=10)

        suchfeld = ctk.CTkEntry(frame, placeholder_text="Suche nach Artikelname")
        suchfeld.pack(fill="x", pady=5)

        table_frame = ctk.CTkScrollableFrame(frame)
        table_frame.pack(fill="both", expand=True, pady=10)

        def load_table(filter_text=""):
            for child in table_frame.winfo_children():
                child.destroy()
            with open(DATA_FILE, newline="") as f:
                reader = csv.reader(f)
                header = next(reader)
                header_str = f"{'Datum':<12} | {'Artikel':<20} | {'Einkauf':<8} | {'Verkauf':<8} | {'Gewinn':<8}"
                ctk.CTkLabel(table_frame, text=header_str, font=ctk.CTkFont(size=14, weight="bold"), anchor="w").pack(anchor="w", padx=10)
                for row in reader:
                    if filter_text.lower() in row[1].lower():
                        gewinn = float(row[3]) - float(row[2])
                        row_str = f"{row[0]:<12} | {row[1]:<20} | {float(row[2]):<8.2f} | {float(row[3]):<8.2f} | {gewinn:<8.2f}"
                        ctk.CTkLabel(table_frame, text=row_str, font=ctk.CTkFont(size=12), anchor="w").pack(anchor="w", padx=10)

        load_table()
        suchfeld.bind("<KeyRelease>", lambda e: load_table(suchfeld.get()))

    def show_add_item(self):
        self.clear_content()
        frame = ctk.CTkFrame(self.content)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = frame

        artikel = ctk.CTkEntry(frame, placeholder_text="Artikelname")
        einkauf = ctk.CTkEntry(frame, placeholder_text="Einkaufspreis (inkl. Gebühren)")
        verkauf = ctk.CTkEntry(frame, placeholder_text="Verkaufspreis")
        datum = ctk.CTkEntry(frame, placeholder_text="Datum (z. B. 2304 → 23.04.2025)")
        artikel.pack(pady=5, fill="x")
        einkauf.pack(pady=5, fill="x")
        verkauf.pack(pady=5, fill="x")
        datum.pack(pady=5, fill="x")

        def format_datum_eingabe(*args):
            raw = datum.get().replace(".", "").replace(" ", "")
            if len(raw) == 4 and raw.isdigit():
                tag, monat = raw[:2], raw[2:]
                datum.delete(0, "end")
                datum.insert(0, f"{tag}.{monat}.{datetime.now().year}")

        datum.bind("<KeyRelease>", format_datum_eingabe)

        def speichern():
            try:
                einkauf_val = self.parse_number(einkauf.get())
                verkauf_val = self.parse_number(verkauf.get())
                datum_val = datum.get().strip()
                if not datum_val:
                    datum_val = datetime.now().strftime("%d.%m.%Y")
                with open(DATA_FILE, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([datum_val, artikel.get(), einkauf_val, verkauf_val])
                self.show_dashboard()
            except ValueError:
                messagebox.showerror("Fehler", "Bitte gültige Zahlen und Datum eingeben.")

        ctk.CTkButton(frame, text="Speichern", command=speichern).pack(pady=10)

    def show_remove_items(self):
        self.clear_content()
        frame = ctk.CTkFrame(self.content)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = frame

        ctk.CTkLabel(frame, text="Artikel entfernen", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=10)

        suchfeld = ctk.CTkEntry(frame, placeholder_text="Suche nach Artikelname")
        suchfeld.pack(fill="x", pady=(0, 10))

        listbox = ctk.CTkScrollableFrame(frame)
        listbox.pack(fill="both", expand=True)

        items = []

        def load_items(filter_text=""):
            for widget in listbox.winfo_children():
                widget.destroy()
            items.clear()
            with open(DATA_FILE, newline="") as f:
                reader = list(csv.reader(f))
                header = reader[0]
                rows = reader[1:]
                for i, row in enumerate(rows):
                    if filter_text.lower() in row[1].lower():
                        gewinn = float(row[3]) - float(row[2])
                        text = f"{row[0]:<12} | {row[1]:<20} | {float(row[2]):<6.2f} → {float(row[3]):<6.2f} € | Gewinn: {gewinn:.2f} €"
                        checkbox = ctk.CTkCheckBox(listbox, text=text, font=ctk.CTkFont(size=12))
                        checkbox.grid(row=i, column=0, sticky="w", padx=5, pady=2)
                        items.append((checkbox, row))

        def entfernen():
            with open(DATA_FILE, newline="") as f:
                reader = list(csv.reader(f))
                header = reader[0]

            neue_daten = [header]
            for box, row in items:
                if not box.get():
                    neue_daten.append(row)

            with open(DATA_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(neue_daten)

            load_items(suchfeld.get())

        suchfeld.bind("<KeyRelease>", lambda e: load_items(suchfeld.get()))

        ctk.CTkButton(frame, text="Ausgewählte entfernen", command=entfernen).pack(pady=10)

        load_items()

    def create_plotly_chart(self, df):
        df = df.sort_values("Datum")
        df_monate = df.groupby(df["Datum"].dt.to_period("M"))["Gewinn"].sum().reset_index()
        df_monate["Datum"] = df_monate["Datum"].astype(str)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_monate["Datum"],
            y=df_monate["Gewinn"],
            mode="lines+markers",
            line=dict(color="lime", width=3),
            fill='tozeroy',
            hoverinfo="x+y"
        ))
        fig.update_layout(
            template="plotly_dark",
            margin=dict(l=0, r=0, t=30, b=0),
            height=300,
            paper_bgcolor="#1e1e1e",
            plot_bgcolor="#1e1e1e",
        )

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        fig.write_html(temp_file.name)
        return temp_file.name

if __name__ == "__main__":
    app = VintedApp()
    app.mainloop()
