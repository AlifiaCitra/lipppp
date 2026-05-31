import streamlit as st

# ... (CSS Global tetap sama seperti kode sebelumnya) ...

# 3. LOGIKA DETEKSI REAKSI & PENJELASAN
# ... (Simpan logika if-elif kamu sebelumnya) ...

# Tambahkan variabel baru untuk penjelasan ilmiah
penjelasan_ilmiah = ""

if status_tipe == "success":
    penjelasan_ilmiah = """
    **Mengapa Positif?**
    Reaksi ini terjadi karena gugus fungsi sampel spesifik terhadap reagen yang digunakan. 
    Contoh: Aldehida memiliki atom H yang terikat pada karbonil, sehingga mampu mereduksi 
    ion logam (seperti Ag+ atau Cu2+) menjadi endapan padat.
    """
elif status_tipe == "error":
    penjelasan_ilmiah = """
    **Mengapa Negatif?**
    Sampel tidak memiliki gugus fungsi yang tepat untuk bereaksi dengan reagen ini. 
    Keton, misalnya, tidak memiliki atom H pada karbon karbonil sehingga tidak bisa 
    dioksidasi oleh reagen Tollens atau Fehling.
    """

# 4. TAMPILKAN HASIL DI PANEL KANAN
with col_visual:
    st.markdown("### 🖥️ Monitor Tabung Reaksi")
    st.markdown(f'<div class="equation-box">REACTION: {rumus_kimia}</div>', unsafe_allow_html=True)
    
    # Render HTML Game (dengan escape {{ dan %% untuk CSS)
    # ... (Gunakan blok html_game yang sudah kita perbaiki tadi) ...
    
    # Tampilkan Status
    if status_tipe == "success":
        st.success(status_teks)
    elif status_tipe == "error":
        st.error(status_teks)
    else:
        st.info(status_teks)
    
    # TAMPILKAN PENJELASAN ILMIAH
    if penjelasan_ilmiah:
        st.markdown("---")
        st.markdown("### 🧬 Penjelasan Ilmiah")
        st.write(penjelasan_ilmiah)
