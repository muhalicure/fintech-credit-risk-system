import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os

basvurular = []
CSV_DOSYA = "kredi_basvurulari.csv"

pencere = tk.Tk()
pencere.title("Fintech Kredi Risk Değerlendirme Sistemi")
pencere.geometry("1200x900")
pencere.configure(bg="#f4f8ff")


def csv_yukle():
    if os.path.exists(CSV_DOSYA):
        with open(CSV_DOSYA, "r", encoding="utf-8-sig") as dosya:
            okuyucu = csv.DictReader(dosya)
            for satir in okuyucu:
                try:
                    satir["gelir"] = float(satir["gelir"])
                    satir["gider"] = float(satir["gider"])
                    satir["borc"] = float(satir["borc"])
                    satir["skor"] = int(float(satir["skor"]))
                    basvurular.append(satir)
                except:
                    pass


def temiz_sayi_al(entry):
    return float(entry.get().replace(".", ""))


def format_para(event):
    widget = event.widget
    deger = widget.get().replace(".", "").strip()

    if deger == "":
        return

    if deger.isdigit():
        yeni_deger = "{:,}".format(int(deger)).replace(",", ".")
        widget.delete(0, tk.END)
        widget.insert(0, yeni_deger)


def skoru_animasyonla(hedef_skor, renk):
    skor_bar["value"] = 0
    skor_sayi.config(text="0", fg=renk)

    def artir(deger=0):
        if deger <= hedef_skor:
            skor_bar["value"] = deger
            skor_sayi.config(text=str(deger))
            pencere.after(12, lambda: artir(deger + 1))

    artir()


def skor_hesapla():
    try:
        ad_soyad = ad_entry.get().strip()
        gelir = temiz_sayi_al(gelir_entry)
        gider = temiz_sayi_al(gider_entry)
        borc = temiz_sayi_al(borc_entry)

        if ad_soyad == "":
            messagebox.showerror("Hata", "Lütfen ad soyad giriniz.")
            return

        if gelir <= 0:
            messagebox.showerror("Hata", "Gelir 0'dan büyük olmalıdır.")
            return

        skor = 0
        kalan_para = gelir - gider

        if kalan_para >= gelir * 0.5:
            skor += 25
        elif kalan_para >= gelir * 0.25:
            skor += 15
        else:
            skor += 5

        borc_orani = borc / gelir

        if borc_orani <= 0.2:
            skor += 20
        elif borc_orani <= 0.5:
            skor += 10
        else:
            skor += 3

        if kredi_gecmisi.get() == "İyi":
            skor += 20
        elif kredi_gecmisi.get() == "Orta":
            skor += 10
        else:
            skor += 3

        if teminat.get() == "Var":
            skor += 15
        else:
            skor += 5

        if calisma.get() == "Sigortalı":
            skor += 20
        elif calisma.get() == "Serbest":
            skor += 10
        else:
            skor += 2

        if skor >= 80:
            risk = "Düşük Risk"
            karar = "Kredi Onaylanabilir"
            renk = "#16a34a"
            mesaj = "Tebrikler! Kredi başvurusu olumlu değerlendirilebilir."
        elif skor >= 60:
            risk = "Orta Risk"
            karar = "Ek teminat istenebilir"
            renk = "#f59e0b"
            mesaj = "Başvuru orta risklidir. Ek teminat veya kefil istenebilir."
        else:
            risk = "Yüksek Risk"
            karar = "Kredi Reddedilebilir"
            renk = "#dc2626"
            mesaj = "Başvuru yüksek risklidir. Kredi verilmesi önerilmez."

        skoru_animasyonla(skor, renk)

        risk_badge.config(text=risk, fg=renk)
        sonuc_banka.config(text=banka.get())
        sonuc_ad.config(text=ad_soyad)
        sonuc_risk.config(text=risk, fg=renk)
        sonuc_karar.config(text=karar, fg=renk)
        sonuc_mesaj.config(text=mesaj, fg=renk)

        basvuru = {
            "banka": banka.get(),
            "ad_soyad": ad_soyad,
            "gelir": gelir,
            "gider": gider,
            "borc": borc,
            "skor": skor,
            "risk": risk,
            "karar": karar
        }

        basvurular.append(basvuru)

    except ValueError:
        messagebox.showerror("Hata", "Gelir, gider ve borç alanlarına sadece sayı giriniz.")


def basvuru_metni_ekle(metin, liste):
    for i, basvuru in enumerate(liste, start=1):
        metin.insert(tk.END, f"{i}. Başvuru\n")
        metin.insert(tk.END, f"Banka: {basvuru['banka']}\n")
        metin.insert(tk.END, f"Ad Soyad: {basvuru['ad_soyad']}\n")
        metin.insert(tk.END, f"Gelir: {basvuru['gelir']}\n")
        metin.insert(tk.END, f"Gider: {basvuru['gider']}\n")
        metin.insert(tk.END, f"Borç: {basvuru['borc']}\n")
        metin.insert(tk.END, f"Skor: {basvuru['skor']}/100\n")
        metin.insert(tk.END, f"Risk: {basvuru['risk']}\n")
        metin.insert(tk.END, f"Karar: {basvuru['karar']}\n")
        metin.insert(tk.END, "-" * 70 + "\n")


def liste_penceresi_ac(baslik_yazi, liste):
    if len(liste) == 0:
        messagebox.showinfo("Kayıtlar", "Gösterilecek kayıt yok.")
        return

    liste_penceresi = tk.Toplevel(pencere)
    liste_penceresi.title(baslik_yazi)
    liste_penceresi.geometry("800x500")
    liste_penceresi.configure(bg="#f4f8ff")

    tk.Label(
        liste_penceresi,
        text=baslik_yazi,
        font=("Arial", 20, "bold"),
        bg="#f4f8ff",
        fg="#0f172a"
    ).pack(pady=20)

    metin = tk.Text(
        liste_penceresi,
        width=95,
        height=23,
        font=("Arial", 11),
        bg="white",
        fg="#0f172a"
    )
    metin.pack(pady=10)

    basvuru_metni_ekle(metin, liste)


def basvurulari_listele():
    liste_penceresi_ac("📋 Kayıtlı Başvurular", basvurular)


def csv_kaydet():
    if len(basvurular) == 0:
        messagebox.showwarning("Uyarı", "Kaydedilecek başvuru yok.")
        return

    with open(CSV_DOSYA, "w", newline="", encoding="utf-8-sig") as dosya:
        alanlar = ["banka", "ad_soyad", "gelir", "gider", "borc", "skor", "risk", "karar"]
        yazici = csv.DictWriter(dosya, fieldnames=alanlar)
        yazici.writeheader()
        yazici.writerows(basvurular)

    messagebox.showinfo("Başarılı", "Başvurular kredi_basvurulari.csv dosyasına kaydedildi.")


def csv_kayitlarini_goster():
    if not os.path.exists(CSV_DOSYA):
        messagebox.showwarning("Uyarı", "Henüz CSV dosyası oluşturulmamış.")
        return

    csv_liste = []

    with open(CSV_DOSYA, "r", encoding="utf-8-sig") as dosya:
        okuyucu = csv.DictReader(dosya)
        for satir in okuyucu:
            try:
                satir["gelir"] = float(satir["gelir"])
                satir["gider"] = float(satir["gider"])
                satir["borc"] = float(satir["borc"])
                satir["skor"] = int(float(satir["skor"]))
                csv_liste.append(satir)
            except:
                pass

    liste_penceresi_ac("📄 CSV Dosyasındaki Kayıtlar", csv_liste)


def formu_temizle():
    ad_entry.delete(0, tk.END)
    gelir_entry.delete(0, tk.END)
    gider_entry.delete(0, tk.END)
    borc_entry.delete(0, tk.END)

    banka.set("Ziraat Bankası")
    kredi_gecmisi.set("İyi")
    teminat.set("Var")
    calisma.set("Sigortalı")

    skor_bar["value"] = 0
    skor_sayi.config(text="0", fg="#64748b")
    risk_badge.config(text="Bekleniyor", fg="#64748b")

    sonuc_banka.config(text="-")
    sonuc_ad.config(text="-")
    sonuc_risk.config(text="-", fg="#64748b")
    sonuc_karar.config(text="-", fg="#64748b")
    sonuc_mesaj.config(text="Henüz değerlendirme yapılmadı.", fg="#64748b")


def label(parent, text, size=11, bold=False, color="#1e293b", bg="white"):
    font = ("Arial", size, "bold") if bold else ("Arial", size)
    return tk.Label(parent, text=text, font=font, fg=color, bg=bg)


def entry(parent):
    return tk.Entry(
        parent,
        font=("Arial", 13),
        width=20,
        bg="#ffffff",
        fg="#0f172a",
        relief="solid",
        bd=1
    )


def renkli_buton(parent, text, command, bg, hover, width=22):
    buton = tk.Label(
        parent,
        text=text,
        font=("Arial", 13, "bold"),
        bg=bg,
        fg="white",
        width=width,
        height=2,
        cursor="hand2"
    )

    buton.bind("<Button-1>", lambda event: command())
    buton.bind("<Enter>", lambda event: buton.config(bg=hover))
    buton.bind("<Leave>", lambda event: buton.config(bg=bg))

    return buton


ana_alan = tk.Frame(pencere, bg="#f4f8ff")
ana_alan.pack(expand=True)

header = tk.Frame(ana_alan, bg="#f4f8ff")
header.pack(fill="x", pady=(10, 18))

logo = tk.Label(header, text="🏦", font=("Arial", 42), bg="#f4f8ff")
logo.grid(row=0, column=0, rowspan=2, padx=(0, 18))

tk.Label(
    header,
    text="Fintech Kredi Risk\nDeğerlendirme Sistemi",
    font=("Arial", 30, "bold"),
    bg="#f4f8ff",
    fg="#0f172a",
    justify="left"
).grid(row=0, column=1, sticky="w")

tk.Label(
    header,
    text="Müşteri finansal bilgilerini girerek kredi risk skorunu hesaplayın.",
    font=("Arial", 13),
    bg="#f4f8ff",
    fg="#475569"
).grid(row=1, column=1, sticky="w", pady=(6, 0))

mini_card = tk.Frame(header, bg="white", padx=22, pady=16, highlightbackground="#cbd5e1", highlightthickness=1)
mini_card.grid(row=0, column=2, rowspan=2, padx=(120, 0))

tk.Label(
    mini_card,
    text="🛡️ Güvenli • Hızlı • Akıllı",
    font=("Arial", 12, "bold"),
    bg="white",
    fg="#1e3a8a"
).pack(anchor="w")

tk.Label(
    mini_card,
    text="Finansal geleceğinizi\nbirlikte değerlendiriyoruz.",
    font=("Arial", 10),
    bg="white",
    fg="#475569",
    justify="left"
).pack(anchor="w", pady=(6, 0))

content = tk.Frame(ana_alan, bg="#f4f8ff")
content.pack()

form_card = tk.Frame(content, bg="white", padx=28, pady=22, highlightbackground="#dbeafe", highlightthickness=1)
form_card.grid(row=0, column=0, sticky="n", padx=(0, 35))

label(form_card, "🏛️  Başvuru Yapılan Banka", 11, True, "#1e3a8a").grid(
    row=0, column=0, columnspan=2, sticky="w", pady=(0, 8)
)

banka = tk.StringVar()
banka.set("Ziraat Bankası")
banka_menu = tk.OptionMenu(
    form_card,
    banka,
    "Ziraat Bankası",
    "İş Bankası",
    "Garanti BBVA",
    "Akbank",
    "Yapı Kredi",
    "VakıfBank",
    "Halkbank"
)
banka_menu.config(font=("Arial", 12), width=39, bg="white", fg="#0f172a")
banka_menu.grid(row=1, column=0, columnspan=2, sticky="we", pady=(0, 18))

label(form_card, "👤  Ad Soyad", 10, True, "#334155").grid(row=2, column=0, sticky="w")
label(form_card, "💰  Aylık Gelir (₺)", 10, True, "#334155").grid(row=2, column=1, sticky="w")

ad_entry = entry(form_card)
gelir_entry = entry(form_card)

ad_entry.grid(row=3, column=0, padx=(0, 20), pady=(7, 18), ipady=6)
gelir_entry.grid(row=3, column=1, pady=(7, 18), ipady=6)

label(form_card, "💳  Aylık Gider (₺)", 10, True, "#334155").grid(row=4, column=0, sticky="w")
label(form_card, "📄  Mevcut Borç (₺)", 10, True, "#334155").grid(row=4, column=1, sticky="w")

gider_entry = entry(form_card)
borc_entry = entry(form_card)

gider_entry.grid(row=5, column=0, padx=(0, 20), pady=(7, 18), ipady=6)
borc_entry.grid(row=5, column=1, pady=(7, 18), ipady=6)

gelir_entry.bind("<FocusOut>", format_para)
gider_entry.bind("<FocusOut>", format_para)
borc_entry.bind("<FocusOut>", format_para)

label(form_card, "🛡️  Kredi Geçmişi", 10, True, "#334155").grid(row=6, column=0, sticky="w")
label(form_card, "✅  Teminat Durumu", 10, True, "#334155").grid(row=6, column=1, sticky="w")

kredi_gecmisi = tk.StringVar()
kredi_gecmisi.set("İyi")
kredi_menu = tk.OptionMenu(form_card, kredi_gecmisi, "İyi", "Orta", "Kötü")
kredi_menu.config(font=("Arial", 12), width=16, bg="white")
kredi_menu.grid(row=7, column=0, sticky="w", pady=(7, 18))

teminat = tk.StringVar()
teminat.set("Var")
teminat_menu = tk.OptionMenu(form_card, teminat, "Var", "Yok")
teminat_menu.config(font=("Arial", 12), width=16, bg="white")
teminat_menu.grid(row=7, column=1, sticky="w", pady=(7, 18))

label(form_card, "💼  Çalışma Durumu", 10, True, "#334155").grid(row=8, column=0, sticky="w")

calisma = tk.StringVar()
calisma.set("Sigortalı")
calisma_menu = tk.OptionMenu(form_card, calisma, "Sigortalı", "Serbest", "İşsiz")
calisma_menu.config(font=("Arial", 12), width=16, bg="white")
calisma_menu.grid(row=9, column=0, sticky="w", pady=(7, 22))

hesapla_button = renkli_buton(
    form_card,
    "🧮  Kredi Skorunu Hesapla ve Kaydet",
    skor_hesapla,
    "#0052ff",
    "#003ecb",
    width=42
)
hesapla_button.grid(row=10, column=0, columnspan=2, pady=(2, 2), sticky="we")

result_card = tk.Frame(
    content,
    bg="white",
    padx=30,
    pady=25,
    highlightbackground="#bfdbfe",
    highlightthickness=1
)
result_card.grid(row=0, column=1, sticky="n")

tk.Label(
    result_card,
    text="📊 Değerlendirme Sonucu",
    font=("Arial", 20, "bold"),
    bg="white",
    fg="#0f172a"
).pack(pady=(0, 14))

tk.Label(
    result_card,
    text="Kredi Skoru",
    font=("Arial", 14, "bold"),
    bg="white",
    fg="#1e3a8a"
).pack()

skor_sayi = tk.Label(
    result_card,
    text="0",
    font=("Arial", 50, "bold"),
    bg="white",
    fg="#64748b"
)
skor_sayi.pack()

tk.Label(result_card, text="/100", font=("Arial", 14), bg="white", fg="#334155").pack()

skor_bar = ttk.Progressbar(
    result_card,
    orient="horizontal",
    length=300,
    mode="determinate",
    maximum=100
)
skor_bar.pack(pady=14)

risk_badge = tk.Label(
    result_card,
    text="Bekleniyor",
    font=("Arial", 12, "bold"),
    bg="#f8fafc",
    fg="#64748b",
    padx=15,
    pady=6
)
risk_badge.pack(pady=(0, 18))

info_frame = tk.Frame(result_card, bg="white")
info_frame.pack(fill="x")


def sonuc_satir(icon, baslik):
    row = tk.Frame(info_frame, bg="white")
    row.pack(fill="x", pady=8)

    tk.Label(
        row,
        text=icon,
        font=("Arial", 15),
        bg="white",
        width=3,
        anchor="w"
    ).pack(side="left")

    tk.Label(
        row,
        text=baslik,
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#334155",
        width=14,
        anchor="w"
    ).pack(side="left")

    deger_label = tk.Label(
        row,
        text="-",
        font=("Arial", 12),
        bg="white",
        fg="#0f172a",
        width=22,
        anchor="w"
    )
    deger_label.pack(side="left", padx=(25, 0))

    return deger_label


sonuc_banka = sonuc_satir("🏦", "Banka")
sonuc_ad = sonuc_satir("👤", "Ad Soyad")
sonuc_risk = sonuc_satir("⚠️", "Risk Seviyesi")
sonuc_karar = sonuc_satir("✅", "Kredi Kararı")

mesaj_kutu = tk.Frame(
    result_card,
    bg="#f0fdf4",
    padx=18,
    pady=14,
    highlightbackground="#bbf7d0",
    highlightthickness=1
)
mesaj_kutu.pack(fill="x", pady=(24, 0))

tk.Label(
    mesaj_kutu,
    text="✅ Sistem Mesajı",
    font=("Arial", 12, "bold"),
    bg="#f0fdf4",
    fg="#166534"
).pack(anchor="w")

sonuc_mesaj = tk.Label(
    mesaj_kutu,
    text="Henüz değerlendirme yapılmadı.",
    font=("Arial", 10),
    bg="#f0fdf4",
    fg="#64748b",
    justify="left",
    wraplength=300
)
sonuc_mesaj.pack(anchor="w", pady=(5, 0))

action_frame = tk.Frame(ana_alan, bg="#f4f8ff")
action_frame.pack(pady=18)

listele_button = renkli_buton(
    action_frame,
    "☰  Başvuruları Listele",
    basvurulari_listele,
    "#7c3aed",
    "#6d28d9",
    width=18
)
listele_button.grid(row=0, column=0, padx=8)

csv_goster_button = renkli_buton(
    action_frame,
    "📄  CSV Kayıtlarını Göster",
    csv_kayitlarini_goster,
    "#0f766e",
    "#115e59",
    width=22
)
csv_goster_button.grid(row=0, column=1, padx=8)

csv_button = renkli_buton(
    action_frame,
    "💾  CSV'ye Kaydet",
    csv_kaydet,
    "#16a34a",
    "#15803d",
    width=18
)
csv_button.grid(row=0, column=2, padx=8)

temizle_button = renkli_buton(
    action_frame,
    "🧹  Temizle",
    formu_temizle,
    "#ef4444",
    "#dc2626",
    width=14
)
temizle_button.grid(row=0, column=3, padx=8)

features = tk.Frame(
    ana_alan,
    bg="white",
    padx=25,
    pady=12,
    highlightbackground="#dbeafe",
    highlightthickness=1
)
features.pack(fill="x", pady=(0, 12))

ozellikler = [
    ("🧠", "Akıllı Skorlama", "Kredi skoru üretir."),
    ("🔒", "Güvenli Kayıt", "Başvuruları saklar."),
    ("⚡", "Hızlı İşlem", "Anında analiz yapar."),
    ("📊", "CSV Raporlama", "Verileri dışa aktarır.")
]

for i, (ikon, baslik_ozellik, aciklama) in enumerate(ozellikler):
    kutu = tk.Frame(features, bg="white")
    kutu.grid(row=0, column=i, padx=45)

    tk.Label(kutu, text=ikon, font=("Arial", 22), bg="white").pack()
    tk.Label(
        kutu,
        text=baslik_ozellik,
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#1e3a8a"
    ).pack()
    tk.Label(
        kutu,
        text=aciklama,
        font=("Arial", 9),
        bg="white",
        fg="#64748b"
    ).pack()

footer = tk.Frame(pencere, bg="#eaf2ff")
footer.pack(side="bottom", fill="x")

tk.Label(
    footer,
    text="© 2025 Fintech Kredi Risk Değerlendirme Sistemi   |   🔒 Tüm hakları saklıdır.   |   💻 Developed by MAC",
    font=("Arial", 12, "bold"),
    bg="#eaf2ff",
    fg="#2563eb"
).pack(pady=10)

csv_yukle()
pencere.mainloop()