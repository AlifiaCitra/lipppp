import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman
st.set_page_config(page_title="ChemDex - Arsip Organik", page_icon="📑", layout="wide")

# =========================
# CUSTOM CSS: Konsep Buku Jurnal / Smart Dossier
# =========================
st.markdown("""
<style>
/* Background warna pastel lembut */
[data-testid="stAppViewContainer"] {
    background-color: #f8fafc;
}

/* Modifikasi garis batas kolom biar kaya pembatas buku */
[data-testid="column"] {
    padding: 15px;
}

/* Kotak Laporan Utama (Kanan) */
.report-card {
    background-color: white;
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    border-top: 6px solid #2563eb;
}

/* Label/Badge untuk Gugus Fungsi */
.badge {
    background-color: #e0e7ff;
    color: #3730a3;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: bold;
    display: inline-block;
    margin-bottom: 20px;
}

/* Kotak info khusus untuk visual hasil */
.visual-box {
    background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
    border: 1px solid #d1d5db;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    font-size: 20px;
    font-weight: bold;
    color: #1f2937;
}
</style>
""", unsafe_allow_html=True)

# 2. Database Uji Kualitatif
data_uji = {
    "Uji Tollens (Cermin Perak)": {
        "Gugus": "Aldehida", 
        "Reagen": "AgNO3 + NaOH + NH4OH",
        "Prosedur": "Tambahkan sampel ke reagen Tollens, panaskan perlahan di penangas air.",
        "Hasil": "Terbentuk endapan logam perak murni yang menempel di dinding kaca tabung reaksi.",
        "Visual": "🪞 Terbentuk Cermin Perak",
        "Warna": "#f8fafc"
    },
    "Uji FeCl3 (Besi Klorida)": {
        "Gugus": "Fenol", 
        "Reagen": "Larutan Besi(III) Klorida 1%",
        "Prosedur": "Larutkan sampel fenol dalam air murni, teteskan reagen FeCl3.",
        "Hasil": "Terjadi perubahan warna instan karena terbentuknya ion kompleks besi-fenolat.",
        "Visual": "🟣 Warna Ungu / Hijau Pekat",
        "Warna": "#faf5ff"
    },
    "Uji Baeyer (Oksidasi)": {
        "Gugus": "Alkena / Alkuna", 
        "Reagen": "Larutan KMnO4 1% netral",
        "Prosedur": "Teteskan kalium permanganat ke dalam larutan sampel sambil dikocok.",
        "Hasil": "Ion permanganat tereduksi menjadi mangan dioksida (MnO2) yang mengendap.",
        "Visual": "🟤 Warna Ungu Hilang & Endapan Coklat",
        "Warna": "#fdf8f6"
    },
    "Uji Lucas (Substitusi)": {
        "Gugus": "Alkohol Tersier/Sekunder", 
        "Reagen": "HCl pekat + Seng Klorida (ZnCl2)",
        "Prosedur": "Campurkan sampel dengan reagen pada suhu ruang, amati waktunya.",
        "Hasil": "Gugus -OH digantikan oleh Cl, membentuk alkil klorida yang tidak larut air.",
        "Visual": "⚪ Kekeruhan Terjadi (Fasa Terpisah)",
        "Warna": "#f0fdf4"
    }
}

# 3. HEADER APLIKASI
st.title("📑 ChemDex: Jurnal Kualitatif Organik")
st.write("Ensiklopedia digital untuk analisis gugus fungsi kimia.")
st.divider()

# 4. MEMBUAT LAYOUT 2 KOLOM (Kiri untuk Menu, Kanan untuk Laporan)
col_menu, col_laporan = st.columns([1, 2.5])

# BAGIAN KIRI: Menu Navigasi Sederhana
with col_menu:
    st.subheader("📋 Daftar Analisis")
    # Menggunakan radio button agar tampilannya berupa list vertikal (bukan kotak)
    pilihan = st.radio(
        "Pilih jenis uji yang ingin dilihat:",
        list(data_uji.keys()),
        label_visibility="collapsed"
    )

# BAGIAN KANAN: Lembar Laporan Digital
with col_laporan:
    # Mengambil data berdasarkan pilihan di sebelah kiri
    item = data_uji[pilihan]
    
    st.markdown(f"""
    <div class="report-card">
        <span class="badge">Target Analisis: {item['Gugus']}</span>
        <h1 style="color: #1e293b; margin-top: 0px;">{pilihan}</h1>
        <hr style="border: 1px solid #f1f5f9; margin-bottom: 30px;">
        
        <h4 style="color: #2563eb;">🧪 Komposisi Reagen</h4>
        <p style="font-size: 16px; color: #475569;">{item['Reagen']}</p>
        
        <br>
        
        <h4 style="color: #2563eb;">⚙️ Prosedur & Mekanisme Reaksi</h4>
        <p style="font-size: 16px; color: #475569;"><b>Cara Kerja:</b> {item['Prosedur']}</p>
        <p style="font-size: 16px; color: #475569;"><b>Analisis:</b> {item['Hasil']}</p>
        
        <br><br>
        
        <h4 style="color: #2563eb; text-align: center;">👁️ Visualisasi Hasil Positif</h4>
        <div class="visual-box">
            {item['Visual']}
        </div>
    </div>
    """, unsafe_allow_html=True)
