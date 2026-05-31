import streamlit as st

# 1. Konfigurasi Halaman Dasar
st.set_page_config(
    page_title="ChemSim - Virtual Test Tube", 
    page_icon="🧪", 
    layout="wide"
)

# CSS Global: Mengatur background laboratorium, teks kontras, dan panel kontrol lab
st.markdown("""
<style>
    /* Background Laboratorium dengan gradasi gelap estetik */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%) !important;
    }
    
    /* Panel Kontrol di Kiri (Latar Belakang Putih Cerah agar Tulisan Sangat Jelas) */
    .stSelectbox, .stSlider {
        background-color: #ffffff !important;
        padding: 18px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
        margin-bottom: 15px;
        border: 3px solid #a855f7;
    }
    
    /* Memaksa label kontrol teks di atas dropdown tetap putih terang */
    label, .stMarkdown p, h1, h2, h3 {
        color: #f8fafc !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.6);
    }
    
    /* Box Persamaan Reaksi di Kanan bergaya Monitor Hologram */
    .equation-box {
        background: #020617;
        color: #22d3ee;
        font-family: 'Courier New', monospace;
        padding: 18px;
        border-radius: 20px;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        border: 2px solid #22d3ee;
        box-shadow: 0 0 20px rgba(34, 211, 238, 0.3);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧪 Virtual Test Tube Simulator Game v6.0")
st.write("Atur sampel dan reagen, naikkan suhu untuk menyalakan api pemanas, dan lihat reaksinya!")
st.divider()

# 2. PANEL INPUT (Kiri)
col_input, col_visual = st.columns([1, 1.1])

with col_input:
    st.markdown("### 📋 Panel Kontrol Laboratorium")
    
    sampel = st.selectbox(
        "Pilih Sampel Utama:", 
        [
            "-- Kosong --", 
            "Formaldehida (Aldehida)", 
            "Aseton (Keton)",
            "Glukosa (Gula Pereduksi)",
            "Fenol", 
            "Asam Asetat (Asam Karboksilat)",
            "Minyak Goreng (Ester)"
        ]
    )
    
    reagen = st.selectbox(
        "Tambahkan Pereaksi (Reagen):", 
        [
            "-- Tanpa Reagen --", 
            "Pereaksi Tollens", 
            "Pereaksi Fehling",
            "Larutan FeCl3", 
            "Larutan NaHCO3 5%",
            "NaOH + Pemanasan"
        ]
    )
    
    suhu = st.slider(
        "Atur Suhu Pemanas (°C):", 
        min_value=25, max_value=100, value=25, step=5
    )

# 3. LOGIKA DETEKSI REAKSI & PERUBAHAN WARNA CAIRAN
warna_cairan = "rgba(255, 255, 255, 0.15)"
tinggi_cairan = "30px"
rumus_kimia = "Menunggu Reaksi..."
status_teks = "Silakan tentukan zat organik pada panel kiri."
status_tipe = "info"

# Kontrol Efek Animasi (Asap, Gelembung, Endapan)
efek_asap = "0"
efek_gelembung = "none"
efek_endapan = "none"

# Logika pemicu api: Menyala jika suhu di atas suhu kamar (25 derajat)
api_visible = "block" if suhu > 25 else "none"

if sampel != "-- Kosong --":
    warna_cairan = "rgba(241, 245, 249, 0.4)" 
    tinggi_cairan = "90px"
    rumus_kimia = f"Sampel: {sampel}"
    status_teks = "Sampel masuk ke tabung. Tambahkan reagen pembantu!"
    
    if reagen != "-- Tanpa Reagen --":
        tinggi_cairan = "180px" 
        
        # [UJI TOLLENS]
        if "Aldehida" in sampel and reagen == "Pereaksi Tollens":
            if suhu >= 70:
                warna_cairan = "linear-gradient(135deg, #cbd5e1 0%, #94a3b8 50%, #334155 100%)"
                rumus_kimia = "R-CHO + 2[Ag(NH3)2]+ -> R-COO- + 2Ag(s)"
                status_teks = "💥 POSITIF! Terbentuk lapisan cermin perak mengkilap di dinding tabung reaksi!"
                status_tipe = "success"
                efek_asap = "1"
                efek_gelembung = "block"
            else:
                warna_cairan = "rgba(203, 213, 225, 0.7)"
                rumus_kimia = "R-CHO + Reagen Tollens"
                status_teks = "Reaksi lambat. Nyalakan api pemanas lebih besar hingga suhu >= 70°C!"
                status_tipe = "warning"
                efek_asap = "0.3"
                
        # [UJI FEHLING]
        elif ("Aldehida" in sampel or "Glukosa" in sampel) and reagen == "Pereaksi Fehling":
            if suhu >= 60:
                warna_cairan = "linear-gradient(to bottom, #f87171, #ef4444)"
                rumus_kimia = "R-CHO + 2Cu2+ -> R-COO- + Cu2O(s)"
                status_teks = "💥 POSITIF! Terbentuk endapan Merah Bata (Cu2O) di dasar bulat tabung!"
                status_tipe = "success"
                efek_endapan = "block"
                efek_asap = "0.8"
            else:
                warna_cairan = "#1d4ed8" 
                rumus_kimia = "R-CHO + Cu2+ (Fehling)"
                status_teks = "Larutan tetap biru. Besarkan api pemanas hingga suhu >= 60°C!"
                status_tipe = "warning"
                efek_asap = "0.3"

        # [PEMBATAS KETON]
        elif "Keton" in sampel and reagen in ["Pereaksi Tollens", "Pereaksi Fehling"]:
            warna_cairan = "rgba(252, 165, 165, 0.6)" if reagen == "Pereaksi Tollens" else "#1d4ed8"
            rumus_kimia = "Keton + Reagen -> No Reaction"
            status_teks = "❌ NEGATIF! Keton tidak bereaksi karena tidak memiliki atom hidrogen pada gugus fungsi karbonil."
            status_tipe = "error"
            if suhu > 25:
                efek_asap = "0.4"
                
        # [UJI FENOL]
        elif "Fenol" in sampel and reagen == "Larutan FeCl3":
            warna_cairan = "linear-gradient(to bottom, #6b21a8, #3b0764)"
            rumus_kimia = "6Ar-OH + Fe3+ -> [Fe(OAr)6]3-"
            status_teks = "💥 POSITIF! Terbentuk senyawa kompleks besi(III) fenolat berwarna ungu gelap!"
            status_tipe = "success"
            if suhu >= 75:
                efek_asap = "1"
            elif suhu > 25:
                efek_asap = "0.4"

        # [UJI ASAM KARBOKSILAT]
        elif "Asam Karboksilat" in sampel and reagen == "Larutan NaHCO3 5%":
            warna_cairan = "rgba(241, 245, 249, 0.7)"
            rumus_kimia = "R-COOH + NaNaHCO3 -> CO2(g)"
            status_teks = "💥 POSITIF! Reaksi menghasilkan pelepasan gelembung busa gas CO2 aktif!"
            status_tipe = "success"
            efek_gelembung = "block"
            efek_asap = "0.5"

        # [UJI ESTER]
        elif "Ester" in sampel and reagen == "NaOH + Pemanasan":
            if suhu >= 60:
                warna_cairan = "linear-gradient(to bottom, #fef08a, #ca8a04)"
                rumus_kimia = "R-COOR' + NaOH -> R-COONa (Sabun)"
                status_teks = "💥 POSITIF! Hidrolisis basa (saponifikasi) berhasil membentuk emulsi sabun!"
                status_tipe = "success"
                efek_asap = "1"
            else:
                warna_cairan = "rgba(254, 249, 195, 0.8)"
                rumus_kimia = "R-COOR' + NaOH"
                status_teks = "Minyak belum menyatu. Pertahankan api pemanas hingga suhu >= 60°C!"
                status_tipe = "warning"
                efek_asap = "0.3"
        else:
            warna_cairan = "rgba(225, 29, 72, 0.5)"
            rumus_kimia = "Tidak Terjadi Reaksi"
            status_teks = "❌ NEGATIF! Karakteristik sampel tidak cocok dengan fungsi reagen."
            status_tipe = "error"
            if suhu > 25:
                efek_asap = "0.3"

# 4. MONITOR VISUAL TABUNG REAKSI + ANIMASI API BUNSEN (Kanan)
with col_visual:
    st.markdown("### 🖥️ Monitor Tabung Reaksi Virtual")
    
    st.markdown(f'<div class="equation-box">REACTION FORMULA: {rumus_kimia}</div>', unsafe_allow_html=True)
    
    # Render grafis HTML interaktif dengan animasi Api Bunsen di bawah rak kayu
    html_game = f"""
    <div style="text-align: center; font-family: Arial, sans-serif; padding-top: 10px; position: relative;">
        
        <div style="font-size: 3
