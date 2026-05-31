import streamlit as st

# 1. Konfigurasi Dasar Halaman
st.set_page_config(
    page_title="ChemSim - Game Tabung Reaksi", 
    page_icon="🧪", 
    layout="wide"
)

# Custom CSS Global untuk mewarnai Background Utama Aplikasi
st.markdown("""
<style>
    /* Mewarnai background seluruh aplikasi dengan gradasi pastel laboratory */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #e0f2fe 0%, #f3e8ff 100%);
    }
    
    /* Mempercantik kotak kontrol input */
    .stSelectbox, .stSlider {
        background-color: white;
        padding: 12px;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04);
        margin-bottom: 10px;
    }
    
    /* Box Persamaan Reaksi bergaya Arcade Game */
    .equation-box {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: #38bdf8;
        font-family: 'Courier New', monospace;
        padding: 15px;
        border-radius: 16px;
        text-align: center;
        font-size: 16px;
        font-weight: bold;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        margin-bottom: 15px;
        border: 2px solid #38bdf8;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧪 Virtual Test Tube Simulator Game")
st.write("Racik sampel organik ke dalam tabung reaksi dan lihat perubahan warnanya!")
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

# 3. LOGIKA SIMULATOR GAME
warna_cairan = "rgba(255,255,255,0.3)"  # Awal transparan kosong
tinggi_cairan = "40px"                   # Sedikit isi dasar
rumus_kimia = "Menunggu Reaksi..."
status_teks = "Silakan tentukan zat kimia pada panel kiri."
status_tipe = "info"       
efek_asap = "opacity: 0;"  

if sampel != "-- Kosong --":
    warna_cairan = "rgba(241, 245, 249, 0.6)"  # Cairan bening jernih sampel
    tinggi_cairan = "100px"
    rumus_kimia = f"Sampel: {sampel}"
    status_teks = "Sampel telah dituangkan. Pilih reagen pembantu!"
    
    if reagen != "-- Tanpa Reagen --":
        tinggi_cairan = "170px"  # Volume naik karena dicampur reagen
        
        # --- UJI TOLLENS ---
        if "Aldehida" in sampel and reagen == "Pereaksi Tollens":
            if suhu >= 70:
                warna_cairan = "linear-gradient(to bottom, #cbd5e1, #94a3b8, #475569)"
                rumus_kimia = "R-CHO + 2[Ag(NH3)2]+ -> R-COO- + 2Ag(s)"
                status_teks = "💥 POSITIF! Lapisan logam cermin perak terbentuk di dinding tabung reaksi!"
                status_tipe = "success"
                efek_asap = "opacity: 1;"
            else:
                warna_cairan = "#e2e8f0"
                rumus_kimia = "R-CHO + Reagen Tollens"
                status_teks = "Larutan Tollens dingin. Panaskan tabung hingga >= 70°C!"
                status_tipe = "warning"
                
        # --- UJI FEHLING ---
        elif ("Aldehida" in sampel or "Glukosa" in sampel) and reagen == "Pereaksi Fehling":
            if suhu >= 60:
                warna_cairan = "linear-gradient(to bottom, #ef4444, #b91c1c)"
                rumus_kimia = "R-CHO + 2Cu2+ + 5OH- -> R-COO- + Cu2O(s)"
                status_teks = "💥 POSITIF! Terbentuk endapan Merah Bata (Cu2O) di bagian bawah tabung reaksi!"
                status_tipe = "success"
                efek_asap = "opacity: 1;"
            else:
                warna_cairan = "#2563eb"  # Biru reagen asli
                rumus_kimia = "R-CHO + Cu2+ (Fehling)"
                status_teks = "Warna tetap biru. Panaskan tabung reaksi hingga >= 60°C!"
                status_tipe = "warning"

        # --- KETON + REAGEN PEMBEDA ---
        elif "Keton" in sampel and reagen in ["Pereaksi Tollens", "Pereaksi Fehling"]:
            warna_cairan = "#fca5a5" if reagen == "Pereaksi Tollens" else "#2563eb"
            rumus_kimia = "R-CO-R + Reagen -> No Reaction"
            status_teks = "❌ NEGATIF! Keton tidak bereaksi dengan Tollens/Fehling karena tidak memiliki atom H-karbonil."
            status_tipe = "error"
                
        # --- UJI FENOL ---
        elif "Fenol" in sampel and reagen == "Larutan FeCl3":
            warna_cairan = "linear-gradient(to bottom, #6b21a8, #4c1d95)"  
            rumus_kimia = "6Ar-OH + Fe3+ -> [Fe(OAr)6]3- (Ungu)"
            status_teks = "💥 POSITIF! Terbentuk senyawa kompleks besi(III) fenolat berwarna ungu pekat!"
            status_tipe = "success"
            if suhu >= 75:
                efek_asap = "opacity: 1;"

        # --- UJI ASAM KARBOKSILAT ---
        elif "Asam Karboksilat" in sampel and reagen == "Larutan NaHCO3 5%":
            warna_cairan = "linear-gradient(to bottom, #f1f5f9, #cbd5e1)"
            rumus_kimia = "R-COOH + NaNaHCO3 -> R-COONa + H2O + CO2(g)"
            status_teks = "💥 POSITIF! Terbentuk banyak gelembung gas CO2 di dalam tabung reaksi!"
            status_tipe = "success"
            efek_asap = "opacity: 0.7;"  

        # --- UJI ESTER (SAPONIFIKASI) ---
        elif "Ester" in sampel and reagen == "NaOH + Pemanasan":
            if suhu >= 60:
                warna_cairan = "linear-gradient(to bottom, #fef08a, #eab308)"  
                rumus_kimia = "R-COOR' + NaOH -> R-COONa + R'-OH"
                status_teks = "💥 POSITIF! Hidrolisis basa (saponifikasi) menghasilkan emulsi sabun!"
                status_tipe = "success"
                efek_asap = "opacity: 1;"
            else:
                warna_cairan = "#fef9c3"  
                rumus_kimia = "R-COOR' + NaOH"
                status_teks = "Lapisan masih terpisah. Panaskan tabung reaksi hingga >= 60°C!"
                status_tipe = "warning"
                
        # --- NEGATIF LAINNYA ---
        else:
            warna_cairan = "#fecdd3"  
            rumus_kimia = "No Reaction"
            status_teks = "❌ NEGATIF! Tidak terjadi perubahan kimia. Reagen tidak cocok."
            status_tipe = "error"

# 4. MONITOR VISUAL TABUNG REAKSI (Kanan)
with col_visual:
    st.subheader("🖥️ Monitor Tabung Reaksi Virtual")
    
    # Box Rumus Atas
    st.markdown(f'<div class="equation-box">REACTION: {rumus_kimia}</div>', unsafe_allow_html=True)
    
    # HTML Grafis Baru: Desain Tabung Reaksi + Rak Kayu dengan background transparan menyatu
    html_tabung = f"""
    <div style="text-align: center; padding: 10px;">
        <div style="font-size: 35px; height: 40px; margin-bottom: 5px; transition: all 0.5s; {efek_asap}">💨</div>
        
        <div style="border: 5px solid #64748b; border-top: none; 
                    border-radius: 0 0 50px 50px; 
                    width: 90px; height: 260px; margin: 0 auto; position: relative; 
                    background: rgba(255, 255, 255, 0.5); box-shadow: 0 10px 25px rgba(0,0,0,0.08);
                    z-index: 2;">
            
            <div style="position: absolute; top: -5px; left: -1
