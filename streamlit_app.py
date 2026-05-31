import streamlit as st

# 1. Konfigurasi Dasar Halaman
st.set_page_config(
    page_title="ChemSim - Game Simulator Lab", 
    page_icon="🧪", 
    layout="wide"
)

st.title("🧪 Virtual Beaker Simulator Game v2.0")
st.write("Koleksi zat diperbanyak! Pilih kombinasi yang tepat untuk memicu reaksi.")
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
        "3. Atur Suhu Sistem (°C):", 
        min_value=25, max_value=100, value=25, step=5
    )

# 3. LOGIKA GAME (WARNA, RUMUS, & STATUS REAKSI)
warna_cairan = "#e2e8f0"  
tinggi_cairan = "80px"    
rumus_kimia = "Menunggu Reaksi..."
status_teks = "Silakan masukkan sampel dan reagen untuk memulai simulasi."
status_tipe = "info"       
efek_asap = "opacity: 0;"  

if sampel != "-- Kosong --":
    warna_cairan = "#f8fafc"  # Bening awal
    tinggi_cairan = "140px"
    rumus_kimia = f"Sampel: {sampel}"
    status_teks = "Sampel masuk ke beaker. Masukkan reagen untuk melihat reaksi!"
    
    if reagen != "-- Tanpa Reagen --":
        tinggi_cairan = "200px"  
        
        # --- REAKSI 1: ALDEHIDA + TOLLENS (Cermin Perak) ---
        if "Aldehida" in sampel and reagen == "Pereaksi Tollens":
            if suhu >= 70:
                warna_cairan = "linear-gradient(135deg, #94a3b8 0%, #f1f5f9 50%, #64748b 100%)"
                rumus_kimia = "R-CHO + 2[Ag(NH3)2]+ -> R-COO- + 2Ag(s)"
                status_teks = "💥 POSITIF! Terbentuk cermin perak murni pada dinding gelas!"
                status_tipe = "success"
                efek_asap = "opacity: 1;"
            else:
                warna_cairan = "#cbd5e1"
                rumus_kimia = "R-CHO + Reagen Tollens"
                status_teks = "Tollens butuh panas. Naikkan suhu slider ke >= 70°C!"
                status_tipe = "warning"
                
        # --- REAKSI 2: GLUKOSA / ALDEHIDA + FEHLING (Merah Bata) ---
        elif ("Aldehida" in sampel or "Glukosa" in sampel) and reagen == "Pereaksi Fehling":
            if suhu >= 60:
                warna_cairan = "#b91c1c"  # Merah bata
                rumus_kimia = "R-CHO + 2Cu2+ + 5OH- -> R-COO- + Cu2O(s)"
                status_teks = "💥 POSITIF! Gugus reduksi mereduksi Fehling menjadi endapan Merah Bata (Cu2O)!"
                status_tipe = "success"
                efek_asap = "opacity: 1;"
            else:
                warna_cairan = "#1d4ed8"  # Biru khas fehling kalau dingin
                rumus_kimia = "R-CHO + Cu2+ (Fehling)"
                status_teks = "Warna tetap biru. Panaskan sistem ke >= 60°C untuk memicu endapan!"
                status_tipe = "warning"

        # --- REAKSI 3: KETON + TOLLENS/FEHLING (Negatif - Pembatas Keton vs Aldehida) ---
        elif "Keton" in sampel and reagen in ["Pereaksi Tollens", "Pereaksi Fehling"]:
            warna_cairan = "#fca5a5" if reagen == "Pereaksi Tollens" else "#1d4ed8"
            rumus_kimia = "R-CO-R + Reagen -> No Reaction"
            status_teks = "❌ NEGATIF! Keton tidak bisa dioksidasi oleh Tollens maupun Fehling karena tidak punya H-karbonil."
            status_tipe = "error"
                
        # --- REAKSI 4: FENOL + FeCl3 (Ungu Pekat) ---
        elif "Fenol" in sampel and reagen == "Larutan FeCl3":
            warna_cairan = "#4c1d95"  
            rumus_kimia = "6Ar-OH + Fe3+ -> [Fe(OAr)6]3- (Ungu)"
            status_teks = "💥 POSITIF! Terbentuk kompleks besi(III) fenolat berwarna ungu tua eksotis!"
            status_tipe = "success"
            if suhu >= 75:
                efek_asap = "opacity: 1;"

        # --- REAKSI 5: ASAM KARBOKSILAT + NaHCO3 (Gelembung Gas CO2) ---
        elif "Asam Karboksilat" in sampel and reagen == "Larutan NaHCO3 5%":
            warna_cairan = "#e2e8f0"
            rumus_kimia = "R-COOH + NaNaHCO3 -> R-COONa + H2O + CO2(g)"
            status_teks = "💥 POSITIF! Reaksi asam-basa menghasilkan pelepasan gas CO2 (ditandai busa/gelembung)!"
            status_tipe = "success"
            efek_asap = "opacity: 1;"  # Busa diwakili asap

        # --- REAKSI 6: ESTER + NaOH (Saponifikasi Sabun) ---
        elif "Ester" in sampel and reagen == "NaOH + Pemanasan":
            if suhu >= 60:
                warna_cairan = "#fef08a"  
                rumus_kimia = "R-COOR' + NaOH -> R-COONa + R'-OH"
                status_teks = "💥 POSITIF! Penyabunan (saponifikasi) menghasilkan garam karboksilat (sabun)!"
                status_tipe = "success"
                efek_asap = "opacity: 1;"
            else:
                warna_cairan = "#fef9c3"  
                rumus_kimia = "R-COOR' + NaOH"
                status_teks = "Campuran minyak-basa belum menyatu. Naikkan suhu ke >= 60°C!"
                status_tipe = "warning"
                
        # --- JIKA BERPASANGAN TAPI SALAH ---
        else:
            warna_cairan = "#fda4af"  
            rumus_kimia = "No Reaction"
            status_teks = "❌ NEGATIF! Reagen ini tidak memicu reaksi spesifik apa pun dengan sampel."
            status_tipe = "error"

# 4. MONITOR VISUAL GAME (Kanan)
with col_visual:
    st.subheader("🖥️ Monitor Beaker Virtual")
    
    # Box Rumus Atas
    st.markdown(
        f'<div class="equation-box">REACTION: {rumus_kimia}</div>', 
        unsafe_allow_html=True
    )
    
    # Grafis Gelas Beaker HTML Terisolasi
    html_gelas = f"""
    <div style="font-family: Arial, sans-serif; text-align: center; background-color: #f8fafc; padding: 10px;">
        <div style="font-size: 35px; height: 45px; transition: all 0.5s; {efek_asap}">💨</div>
        
        <div style="border: 6px solid #64748b; border-top: none; border-radius: 0 0 25px 25px; 
                    width: 200px; height: 240px; margin: 0 auto; position: relative; 
                    background: rgba(255,255,255,0.7); box-shadow: 0 10px 15px rgba(0,0,0,0.05);">
            
            <div style="position: absolute; top: 0; left: -16px; width: 0; height: 0; 
                        border-right: 16px solid #64748b; border-bottom: 16px solid transparent;"></div>
            
            <div style="background: {warna_cairan}; width: 100%; height: {tinggi_cairan}; 
                        position: absolute; bottom: 0; border-radius: 0 0 20px 20px; 
                        transition: all 0.6s ease-in-out; display: flex; align-items: center; justify-content: center;">
                <b style="color: #1e293b; font-size: 16px; opacity: 0.6;">{suhu}°C</b>
            </div>
            
            <div style="position: absolute; right: 12px; top: 40px; border-top: 3px solid #94a3b8; width: 20px;"></div>
            <div style="position: absolute; right: 12px; top: 90px; border-top: 3px solid #94a3b8; width: 12px;"></div>
            <div style="position: absolute; right: 12px; top: 140px; border-top: 3px solid #94a3b8; width: 20px;"></div>
            <div style="position: absolute; right: 12px; top: 190px; border-top: 3px solid #94a3b8; width: 12px;"></div>
        </div>
        <p style="margin-top: 12px; font-weight: bold; color: #64748b;">Beaker Glass 250 mL</p>
    </div>
    """
    
    st.components.v1.html(html_gelas, height=350)
    
    # Kotak Teks Status Hasil Real-time
    if status_tipe == "success":
        st.success(status_teks)
    elif status_tipe == "warning":
        st.warning(status_teks)
    elif status_tipe == "error":
        st.error(status_teks)
    else:
        st.info(status_teks)
