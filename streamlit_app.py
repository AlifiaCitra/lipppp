import streamlit as st

# 1. Konfigurasi Halaman & Tema Warna Gradient Background
st.set_page_config(
    page_title="ChemSim - Game Tabung Reaksi", 
    page_icon="🧪", 
    layout="wide"
)

# Menambahkan CSS untuk background utama aplikasi dan box reaksi
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #1e1b4b 0%, #311042 100%) !important;
    }
    .stSelectbox, .stSlider {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 15px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        margin-bottom: 12px;
    }
    .stMarkdown h1, .stMarkdown h3, .stMarkdown p {
        color: #f8fafc !important;
    }
    .equation-box {
        background: #0f172a;
        color: #38bdf8;
        font-family: 'Courier New', monospace;
        padding: 15px;
        border-radius: 16px;
        text-align: center;
        font-size: 16px;
        font-weight: bold;
        border: 2px solid #38bdf8;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

st.title("🧪 Virtual Test Tube Simulator Game v3.0")
st.write("Racik sampel organik ke dalam tabung reaksi dan lihat perubahan warnanya secara real-time!")
st.divider()

# 2. PANEL INPUT (Kiri)
col_input, col_visual = st.columns([1, 1.1])

with col_input:
    st.subheader("📋 Panel Kontrol Laboratorium")
    
    sampel = st.selectbox(
        "1. Pilih Sampel Utama:", 
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
        "2. Tambahkan Pereaksi (Reagen):", 
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
        "3. Atur Suhu Pemanas (°C):", 
        min_value=25, max_value=100, value=25, step=5
    )

# 3. LOGIKA SIMULATOR PENENTU WARNA CAIRAN
warna_cairan = "rgba(255,255,255,0.2)"
tinggi_cairan = "40px"
rumus_kimia = "Menunggu Reaksi..."
status_teks = "Silakan tentukan zat kimia pada panel kiri."
status_tipe = "info"
asap_visible = "0"

if sampel != "-- Kosong --":
    warna_cairan = "rgba(241, 245, 249, 0.5)"
    tinggi_cairan = "100px"
    rumus_kimia = f"Sampel terdeteksi: {sampel}"
    status_teks = "Sampel siap di dalam tabung. Masukkan reagen kimia!"
    
    if reagen != "-- Tanpa Reagen --":
        tinggi_cairan = "180px"
        
        # Skenario 1: Tollens (Cermin Perak)
        if "Aldehida" in sampel and reagen == "Pereaksi Tollens":
            if suhu >= 70:
                warna_cairan = "linear-gradient(to bottom, #cbd5e1, #94a3b8, #475569)"
                rumus_kimia = "R-CHO + 2[Ag(NH3)2]+ -> R-COO- + 2Ag(s)"
                status_teks = "💥 POSITIF! Terbentuk endapan cermin perak murni di dinding tabung reaksi!"
                status_tipe = "success"
                asap_visible = "1"
            else:
                warna_cairan = "#cbd5e1"
                rumus_kimia = "R-CHO + Reagen Tollens"
                status_teks = "Reaksi Tollens butuh panas. Naikkan suhu slider ke >= 70°C!"
                status_tipe = "warning"
                
        # Skenario 2: Fehling (Merah Bata)
        elif ("Aldehida" in sampel or "Glukosa" in sampel) and reagen == "Pereaksi Fehling":
            if suhu >= 60:
                warna_cairan = "linear-gradient(to bottom, #f87171, #991b1b)"
                rumus_kimia = "R-CHO + 2Cu2+ + 5OH- -> R-COO- + Cu2O(s)"
                status_teks = "💥 POSITIF! Terbentuk endapan Merah Bata (Cu2O) hasil reduksi gugus gula!"
                status_tipe = "success"
                asap_visible = "1"
            else:
                warna_cairan = "#1d4ed8"
                rumus_kimia = "R-CHO + Cu2+"
                status_teks = "Warna reagen tetap biru. Panaskan tabung reaksi hingga >= 60°C!"
                status_tipe = "warning"

        # Skenario 3: Keton Pembatas (Negatif)
        elif "Keton" in sampel and reagen in ["Pereaksi Tollens", "Pereaksi Fehling"]:
            warna_cairan = "#fca5a5" if reagen == "Pereaksi Tollens" else "#1d4ed8"
            rumus_kimia = "Keton + Reagen -> No Reaction"
            status_teks = "❌ NEGATIF! Keton tidak bereaksi karena tidak memiliki atom hidrogen alfa-karbonil."
            status_tipe = "error"
                
        # Skenario 4: Fenol + FeCl3 (Ungu Pekat)
        elif "Fenol" in sampel and reagen == "Larutan FeCl3":
            warna_cairan = "linear-gradient(to bottom, #7e22ce, #3b0764)"
            rumus_kimia = "6Ar-OH + Fe3+ -> [Fe(OAr)6]3-"
            status_teks = "💥 POSITIF! Terbentuk senyawa kompleks koordinasi fenolat berwarna ungu pekat!"
            status_tipe = "success"
            if suhu >= 75:
                asap_visible = "1"

        # Skenario 5: Asam Karboksilat (Gelembung CO2)
        elif "Asam Karboksilat" in sampel and reagen == "Larutan NaHCO3 5%":
            warna_cairan = "linear-gradient(to bottom, #e2e8f0, #94a3b8)"
            rumus_kimia = "R-COOH + NaNaHCO3 -> R-COONa + H2O + CO2(g)"
            status_teks = "💥 POSITIF! Gas CO2 terlepas memicu banyak gelembung udara dalam larutan!"
            status_tipe = "success"
            asap_visible = "1"

        # Skenario 6: Saponifikasi Ester
        elif "Ester" in sampel and reagen == "NaOH + Pemanasan":
            if suhu >= 60:
                warna_cairan = "linear-gradient(to bottom, #fef08a, #ca8a04)"
                rumus_kimia = "R-COOR' + NaOH -> R-COONa + R'-OH"
                status_teks = "💥 POSITIF! Hidrolisis basa berhasil memecah ester dan membentuk emulsi sabun!"
                status_tipe = "success"
                asap_visible = "1"
            else:
                warna_cairan = "#fef9c3"
                rumus_kimia = "R-COOR' + NaOH"
                status_teks = "Zat belum menyatu. Naikkan panas pemanas ke >= 60°C!"
                status_tipe = "warning"
        else:
            warna_cairan = "rgba(225, 29, 72, 0.4)"
            rumus_kimia = "Tidak Bereaksi"
            status_teks = "❌ NEGATIF! Gugus fungsi sampel tidak cocok dengan pereaksi ini."
            status_tipe = "error"

# 4. MONITOR VISUAL TABUNG REAKSI (Kanan)
with col_visual:
    st.subheader("🖥️ Monitor Tabung Reaksi Virtual")
    
    # Render rumus reaksi
    st.markdown(f'<div class="equation-box">REACTION: {rumus_kimia}</div>', unsafe_allow_html=True)
    
    # Desain HTML Tabung Reaksi Murni tanpa interpolasi f-string rumit agar tidak error lagi
    html_template = f"""
    <div style="text-align: center; font-family: Arial, sans-serif; padding-top: 10px;">
        <div style="font-size: 35px; height: 40px; margin-bottom: 5px; opacity: {asap_visible}; transition: opacity 0.5s;">💨</div>
        
        <div style="border: 5px solid #cbd5e1; border-top: none; 
                    border-radius: 0 0 50px 50px; 
                    width: 90px; height: 260px; margin: 0 auto; position: relative; 
                    background: rgba(255, 255, 255, 0.2); box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                    z-index: 2;">
            
            <div style="position: absolute; top: -5px; left: -10px; width: 100px; height: 10px; 
                        background-color: #cbd5e1; border-radius: 4px;"></div>
            
            <div style="background: {warna_cairan}; width: 100%; height: {tinggi_cairan}; 
                        position: absolute; bottom: 0; border-radius: 0 0 45px 45px; 
                        transition: height 0.6s, background 0.6s ease-in-out; display: flex; align-items: center; justify-content: center;">
                <b style="color: #ffffff; font-size: 14px; text-shadow: 1px 1px 4px #000;">{suhu}°C</b>
            </div>
        </div>
        
        <div style="width: 170px; height: 18px; background-color: #b45309; margin: -30px auto 0 auto; border-radius: 6px; position: relative; z-index: 1;"></div>
        <div style="width: 130px; height: 40px; border-left: 10px solid #d97706; border-right: 10px solid #d97706; margin: 0 auto; position: relative; z-index: 1;"></div>
        <div style="width: 190px; height: 15px; background-color: #b45309; margin: 0 auto; border-radius: 4px; position: relative; z-index: 1;"></div>
        
        <p style="margin-top: 15px; font-weight: bold; color: #cbd5e1;">Test Tube & Rack Stand</p>
    </div>
    """
    
    st.components.v1.html(html_template, height=420)
    
    # Kotak Pesan Info Status
    if status_tipe == "success":
        st.success(status_teks)
    elif status_tipe == "warning":
        st.warning(status_teks)
    elif status_tipe == "error":
        st.error(status_teks)
    else:
        st.info(status_teks)
