import streamlit as st
import pandas as pd
import re
import plotly.express as px
import joblib
import os
import base64
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# --- 
# FUNGSI MEMBACA FOTO LOKAL (ADZKIA.JPG) ---
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Inisialisasi string foto
bin_str = ""
if os.path.exists("adzkia.png"):
    bin_str = get_base64("adzkia.png")

# --- 1. KONFIGURASI HALAMAN & UI ---
st.set_page_config(page_title="PRODI INFORMATIKA UNVERSITAS ADZKIA", layout="wide")

st.markdown(f"""
    <style>
    /* BAGIAN BARU: Menambahkan Foto Background ke CSS kamu */
    .stApp {{
        background: {f'linear-gradient(rgba(0, 20, 39, 0.8), rgba(0, 20, 39, 0.8)), url("data:image/jpg;base64,{bin_str}")' if bin_str else '#001427'} !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}

    
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    html, body, [class*="css"]
            {{ font-family: 'Poppins', sans-serif;
            color: #2c3e50; }}
    
    .role-card {{
        background-color: #01161e; 
        padding: 20px; border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08); text-align: center;
        border: 2px solid #598392; margin-bottom: 10px;
    }}

    [data-testid="stSidebar"] {{ 
            background-color: #3e5c76; 
            color: #284b63; 
            }}
    
    .stRadio label, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h3 
    {{ 
        color: white !important; 
    }}

    [data-testid="stMetric"] {{
        background-color: #ffffff; padding: 20px; border-radius: 15px;
        box-shadow: 0 8px 15px rgba(0,0,0,0.05); border-left: 10px solid #a8dadc;
    }}
    [data-testid="stMetricValue"] {{ color: #01161e !important; font-weight: 600 !important; }}
    [data-testid="stMetricLabel"] {{ color: #555555 !important; }}

    /* Menargetkan container tombol agar bisa digeser ke tengah */
    [data-testid="column"] .stButton {{
        display: flex;
        justify-content: center; /* Memindahkan tombol ke tengah kolom */
        width: 100%;
        margin-top: 10px; /* Jarak antara kartu dan tombol */
    }}

    /* Mengatur lebar tombol agar pas (tidak kepanjangan) */
    [data-testid="column"] .stButton button {{
        width: 200px !important; /* Sesuaikan lebar tombol sesuai keinginanmu */
    }}
    .stButton>button {{
        width: 100%; border-radius: 25px;
        background: linear-gradient(135deg, #124559 0%, #598392 100%);
        color: white !important; border: none; font-weight: 600;
    }}

    div[data-baseweb="input"] > div, 
    div[data-baseweb="textarea"] > div {{
        background-color: #ffffff !important;
        border-radius: 10px !important;
    }}

    .stTextInput input, .stTextArea textarea {{
        color: #01161e !important;
        -webkit-text-fill-color: #01161e !important;
        background-color: #ffffff !important;
    }}

    div[data-baseweb="input"] > div:focus-within, 
    div[data-baseweb="textarea"] > div:focus-within {{
        border: 1px solid #598392 !important;
        box-shadow: none !important;
    }}

    div.stButton > button {{
        background: linear-gradient(135deg, #b0c4b1 0%, #598392 100%) !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        transition: 0.3s !important;
    }}

    div.stButton > button:hover {{
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(18, 69, 89, 0.4);
        color: #aec3b0 !important;
    }}
            
    div[data-baseweb="select"] > div {{
        background-color: #598392 !important; 
        border: 1px solid #aec3b0 !important;
        border-radius: 10px !important;
    }}

    div[data-baseweb="select"] span, div[data-baseweb="select"] div {{
        color: white !important;
    }}

    svg[title="open"] {{
        fill: white !important;
    }}

    ul[role="listbox"] {{
        background-color: #598392 !important; 
    }}

    ul[role="listbox"] li {{
        color: white !important;
    }}

    ul[role="listbox"] li:hover {{
        background-color: #598392 !important;
        color: #aec3b0 !important;
    }}
    
    .stTabs [data-baseweb="tab"] p {{
        color: #ade8f4 !important; 
        font-weight: 400 !important;
        transition: 0.3s;
    }}

    .stTabs [aria-selected="true"] p {{
        color: #ffffff !important; 
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }}

    .stTabs [data-baseweb="tab-highlight"] {{
        background-color: #ffffff !important; 
    }}

    .stTabs [data-baseweb="tab"]:hover p {{
        color: #ffffff !important;
        text-shadow: 0 0 10px rgba(168, 218, 220, 0.8); 
    }}
    



   /* Menghilangkan label standar */
    [data-testid="stSidebarNav"] {{display: none;}}
    
    /* Container Menu Navigasi */
    div[role="radiogroup"] {{
        display: flex;
        flex-direction: column;
        gap: 0px; 
        /* Trik margin negatif agar garis menempel ke pinggir sidebar */
        margin-left: -1rem !important;
        margin-right: -1rem !important;
        margin-top: 10px;
        width: calc(100% + 2rem) !important;
    }}

    /* Styling per item menu */
    div[role="radiogroup"] label {{
        background-color: transparent;
        /* Garis pembatas bawah yang sejajar/full lebar sidebar */
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important; 
        padding: 18px 25px !important; 
        border-radius: 0px !important;
        transition: 0.3s all ease;
        width: 100% !important;
        margin: 0 !important;
    }}

    /* Efek Hover (Saat kursor di atas menu) */
    div[role="radiogroup"] label:hover {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        /* Garis penanda di kiri saat disentuh */
        border-left: 5px solid #598392 !important;
        padding-left: 30px !important;
    }}

    /* Styling saat menu dipilih (Aktif) */
    div[role="radiogroup"] label[data-selected="true"] {{
        background-color: rgba(89, 131, 146, 0.2) !important;
        border-left: 5px solid #ffffff !important;
        font-weight: bold;
    }}

    /* Sembunyikan bulatan radio button-nya */
    div[role="radiogroup"] [data-testid="stWidgetLabel"] div div {{
        display: none;
    }}

    /* --- CSS NAVIGASI FULL WIDTH --- */
    div[role="radiogroup"] {{
        display: flex;
        flex-direction: column;
        gap: 0px; 
        margin-left: -1rem !important; /* Menarik garis ke kiri sidebar */
        margin-right: -1rem !important; /* Menarik garis ke kanan sidebar */
        margin-top: 10px;
        width: calc(100% + 2rem) !important;
    }}

    div[role="radiogroup"] label {{
        background-color: transparent;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important; 
        padding: 18px 25px !important; 
        border-radius: 0px !important;
        transition: 0.3s all ease;
        width: 100% !important;
        margin: 0 !important;
    }}

    /* Efek Hover Navigasi */
    div[role="radiogroup"] label:hover {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-left: 5px solid #598392 !important;
        padding-left: 30px !important;
    }}

    /* --- CSS TOMBOL LOGOUT MERAH CORAL --- */
    /* Kita menargetkan tombol logout agar selalu di bawah */
    .stButton > button {{
        border-radius: 12px !important;
        transition: 0.3s all ease !important;
    }}

    /* Warna spesifik Merah Coral untuk tombol Keluar */
    button:has(div:contains("Keluar")) {{
        background: linear-gradient(135deg, #d90429 0%, #d90429 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        position: fixed !important;
        bottom: 20px !important;
        left: 10px !important;
        width: 280px !important; /* Sesuaikan lebar sidebar kamu */
        z-index: 1000;
    }}

    button:has(div:contains("Keluar")):hover {{
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(221, 45, 74, 0.4) !important;
    }}
    
    </style>
    """, unsafe_allow_html=True)


# --- 2. LOGIKA DATA & PREPROCESSING ---
@st.cache_resource
def get_tools():
    return StemmerFactory().create_stemmer(), StopWordRemoverFactory().create_stop_word_remover()

stemmer, stopword_remover = get_tools()

# --- FUNGSI DATABASE USER (UNTUK LOGIN SATU PINTU) ---
def load_users():
    if not os.path.exists("users_db.csv"):
        # Role 'Admin' untuk admin, 'User Umum' untuk mahasiswa
        df = pd.DataFrame(columns=["username", "password", "role"])
        # Daftarkan Admin pertama kali secara otomatis
        df.loc[0] = ["admin", "admin123", "Admin"] 
        df.to_csv("users_db.csv", index=False)
    return pd.read_csv("users_db.csv")

def save_user(username, password):
    df = load_users()
    if username in df['username'].values:
        return False
    # Pendaftar baru otomatis menjadi 'User Umum'
    new_user = pd.DataFrame([[username, password, "User Umum"]], columns=["username", "password", "role"])
    new_user.to_csv("users_db.csv", mode='a', header=False, index=False)
    return True

def clean_text_fast(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = stopword_remover.remove(text)
    return " ".join([stemmer.stem(w) for w in text.split()])

# --- PEMBACAAN DATA ---
if 'main_df' not in st.session_state:
    if os.path.exists('evaluasi matkul.xlsx'):
        df_file = pd.read_excel('evaluasi matkul.xlsx')
        
        # CEK: Apakah ini file hasil simpanan (sudah rapi) atau file kuesioner asli?
        if 'Matkul' in df_file.columns and 'Suka' in df_file.columns:
            # Jika file sudah rapi, langsung ambil saja
            st.session_state.main_df = df_file
        else:
            # Jika ini masih file kuesioner asli yang berantakan, jalankan logika pembersihan lama
            sections = [[2,3,4,5,6], [7,8,9,10,11], [12,13,14,15,16], [17,18,19,20,21], 
                        [22,23,24,25,26], [27,28,29,30,31], [32,33,34,35,36], [37,38,39,40,41], 
                        [42,43,44,45,46], [47,48,49,50,51], [52,53,54,55,56], [57,58,59,60,61]]
            rekap = []
            for sec in sections:
                for _, row in df_file.iterrows():
                    if len(row) > max(sec) and pd.notna(row.iloc[sec[0]]):
                        rekap.append({
                            'Matkul': row.iloc[sec[0]], 
                            'Suka': str(row.iloc[sec[2]]), 
                            'Kendala': str(row.iloc[sec[3]]), 
                            'Umum': str(row.iloc[sec[1]])
                        })
            st.session_state.main_df = pd.DataFrame(rekap)

def get_summary():
    model, tfidf = joblib.load('model_nb_aisyah.pkl'), joblib.load('tfidf_aisyah.pkl')
    df = st.session_state.main_df
    summary = df.groupby('Matkul').agg(
        Jml_Suka=('Suka', lambda x: (x.str.strip() != "").sum()), 
        Jml_Kendala=('Kendala', lambda x: (x.str.strip() != "").sum()), 
        Teks_Umum=('Umum', lambda x: " ".join(x.astype(str)))
    ).reset_index()
    def judge(row):
        if row['Jml_Suka'] > row['Jml_Kendala']: return 'Positif'
        elif row['Jml_Kendala'] > row['Jml_Suka']: return 'Negatif'
        else:
            u = clean_text_fast(row['Teks_Umum'])
            return 'Positif' if model.predict(tfidf.transform([u]))[0] == 1 else 'Negatif'
    summary['Status_Umum'] = summary.apply(judge, axis=1)
    return summary

# --- 3. LANDING PAGE ---
if 'role_akses' not in st.session_state: 
    st.session_state.role_akses = None

if st.session_state.role_akses is None:
    # Deskripsi Umum Web
    st.markdown("<h1 style='text-align: center; margin-top: 30px;'>Selamat Datang di Portal Evaluasi</h1>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; padding: 30px; border-radius: 20px; margin-bottom: 30px; border-left: 15px ;'>
            <h5>Selamat datang di <b>Sistem Analisis Sentimen Evaluasi Mata Kuliah</b> Program Studi Informatika Universitas Adzkia.<br> 
            Web ini dirancang untuk memproses ulasan mahasiswa menggunakan teknologi <i>Text Mining</i> dengan algoritma Naive Bayes <br> 
            Hasil analisis ini membantu program studi dalam memantau kualitas pembelajaran secara transparan dan interaktif.</h5>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center; color: #ffffff;'>Silakan Login Untuk Mengakses Data</h3>", unsafe_allow_html=True)
    
    col_kiri, col_utama, col_kanan = st.columns([1, 1.5, 1])

    with col_utama: 
        tab_login, tab_register = st.tabs(["🔐 Masuk Sistem", "📝 Daftar Akun Baru"])

        with tab_login:
            st.write("Silakan masukkan akun untuk melanjutkan.")
            input_user = st.text_input("Username / NIM", placeholder="Masukan Username")
            input_pass = st.text_input("Password", type="password", placeholder="******")
            
            # Tombol otomatis mengikuti lebar kolom tengah yang sudah dirampingkan
            if st.button("Continue", type="primary", use_container_width=True):
                users = load_users()
                match = users[(users['username'] == input_user) & (users['password'] == input_pass)]
                
                if not match.empty:
                    st.session_state.role_akses = match.iloc[0]['role']
                    st.success(f"Berhasil masuk sebagai {st.session_state.role_akses}")
                    st.rerun()
                else:
                    st.error("Username atau Password salah.")

        with tab_register:
            st.write("Lengkapi data untuk membuat akun mahasiswa.")
            reg_name = st.text_input("Buat Username", placeholder="username")
            reg_pass = st.text_input("Buat Password", type="password")
            reg_confirm = st.text_input("Konfirmasi Password", type="password")
            
            agree = st.checkbox("Setuju")
            
            if st.button("Registrasi", use_container_width=True):
                if agree:
                    if reg_pass == reg_confirm and reg_name:
                        if save_user(reg_name, reg_pass):
                            st.success("Akun berhasil dibuat! Silakan pindah ke tab Masuk.")
                        else:
                            st.warning("Username tersebut sudah terdaftar.")
                    else:
                        st.error("Pastikan password cocok dan kolom terisi.")
                else:
                    st.warning("Anda harus menyetujui syarat.")
        
        st.markdown("</div>", unsafe_allow_html=True) # Tutup kotak transparan

# --- 4. DASHBOARD UTAMA ---

else:
    summary = get_summary()
    with st.sidebar:
        # Nama Akses (Admin / User)
        st.markdown(f"<h3 style='text-align:center; padding-top:20px; color:white;'>{st.session_state.role_akses}</h3>", unsafe_allow_html=True)
        st.write("") # Spasi
        
        # Garis pembatas awal
        st.markdown("<hr style='margin: 0 -20px; border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        
        # Daftar Menu
        nav = ["Beranda", "Analisis Sentimen", "Tentang"]
        if st.session_state.role_akses == "Admin": 
            nav.insert(2, "Data Master (Admin)")
        
        # Tampilkan navigasi tanpa label
        menu = st.radio("", nav, label_visibility="collapsed")
        
        if st.button("Keluar"): 
            st.session_state.role_akses = None
            st.rerun()
    if menu == "Beranda":
        st.title("Prodi Informatika Universitas Adzkia")
        
        st.markdown("""
        <div style='background-color:rgba(255,255,255,0.05); padding:20px; border-radius:15px;'>
            <p>Informatika Adzkia berfokus pada pengembangan teknologi yang inovatif dan berbasis karakter mulia. 
            Kami menyiapkan lulusan yang siap bersaing di industri teknologi global.</p>
        </div>
        """, unsafe_allow_html=True)


        st.divider()
        # Membuat dua kolom: kiri untuk Visi, kanan untuk Misi
        col_visi, col_misi = st.columns([1, 1.5], gap="large")

        with col_visi:
            st.markdown("### 🎯 Visi")
            st.markdown("""
                <div style="text-align: justify; color: white; line-height: 1.6;">
                Menjadi program studi yang unggul pada bidang Ilmu Komputer / Informatika 
                dan menghasilkan lulusan yang berkarakter, berprestasi, serta mampu 
                bersaing secara global.
                </div> """, unsafe_allow_html=True)
            

        with col_misi:
            st.markdown("### 🚀 Misi")
            misi_points = [
                "Menyelenggarakan pendidikan dan pembelajaran berkualitas untuk memajukan IPTEK dalam bidang Informatika dengan memperhatikan dan menerapkan nilai-nilai humaniora.",
                "Menyelenggarakan penelitian yang inovatif serta bermanfaat bagi masyarakat dan pengembangan IPTEK di bidang Informatika.",
                "Menyelenggarakan pengabdian kepada masyarakat yang berkualitas dan tepat guna pada bidang Informatika.",
                "Menerapkan tata kelola program studi Informatika yang bersih dan baik (*Clean and Good Governance*).",
                "Menerapkan dan mengembangkan nilai-nilai karakter mulia dan *rahmatan lil ‘alamin* dalam pelaksanaan Tridharma Perguruan Tinggi pada bidang Ilmu Komputer / Informatika."
            ]
            # Bungkus seluruh loop di dalam div justify
            st.markdown('<div style="text-align: justify; color: white;">', unsafe_allow_html=True)
            for i, point in enumerate(misi_points, 1):
                st.markdown(f"**{i}.** {point}")
            st.markdown('</div>', unsafe_allow_html=True)

    elif menu == "Analisis Sentimen":
        st.title("📊 Dashboard Analisis & Statistik")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Matkul", len(summary))
        col2.metric("Sentimen Positif", len(summary[summary['Status_Umum'] == 'Positif']))
        col3.metric("Sentimen Negatif", len(summary[summary['Status_Umum'] == 'Negatif']))
        
        st.divider()
        
        st.subheader("Persentase Kategori Mata Kuliah")
        fig_pie = px.pie(summary, names='Status_Umum', hole=0.4, color='Status_Umum', 
                         color_discrete_map={'Positif':'#90a955','Negatif':'#dd2d4a'})
        
        fig_pie.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    font_color="white"            
)

        
        st.plotly_chart(fig_pie, use_container_width=True)

        st.divider()

        st.subheader("📋 Daftar Seluruh Mata Kuliah")
        
        tab1, tab2 = st.tabs(["👍 Semua Matkul Positif", "👎 Semua Matkul Negatif"])
        
        with tab1:
            df_pos = summary[summary['Status_Umum'] == 'Positif'].sort_values('Jml_Suka', ascending=False)
            st.write(f"Ditemukan **{len(df_pos)}** mata kuliah dengan sentimen positif.")
            fig_all_pos = px.bar(df_pos, x='Jml_Suka', y='Matkul', orientation='h',
                                 color_discrete_sequence=['#90a955'], text_auto=True,
                                 height=max(400, len(df_pos)*30))
            fig_all_pos.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    font_color="white",
    xaxis=dict(showgrid=False), 
    yaxis=dict(showgrid=False)
)
            st.plotly_chart(fig_all_pos, use_container_width=True)
            
        with tab2:
            df_neg = summary[summary['Status_Umum'] == 'Negatif'].sort_values('Jml_Kendala', ascending=False)
            st.write(f"Ditemukan **{len(df_neg)}** mata kuliah dengan sentimen negatif.")
            fig_all_neg = px.bar(df_neg, x='Jml_Kendala', y='Matkul', orientation='h',
                                 color_discrete_sequence=['#dd2d4a'], text_auto=True,
                                 height=max(400, len(df_neg)*30))
            
            # 1. Membuat Grafik
            fig_all_neg = px.bar(df_neg, x='Jml_Kendala', y='Matkul', orientation='h',
                                 color_discrete_sequence=['#dd2d4a'], # Merah Coral agar menyala
                                 text_auto=True,
                                 height=max(400, len(df_neg)*30))
            
            # 2. MENGUBAH LATAR BELAKANG (Tambahkan Bagian Ini)
            fig_all_neg.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', # Transparan mengikuti background web
                plot_bgcolor='rgba(0,0,0,0)',  # Transparan agar tidak ada kotak hitam
                font_color="white",            # Warna teks matkul jadi putih
                xaxis=dict(showgrid=False),    # Hilangkan garis vertikal
                yaxis=dict(showgrid=False),    # Hilangkan garis horizontal
                margin=dict(l=20, r=20, t=20, b=20) # Mengatur jarak pinggir grafik
            )
            
            st.plotly_chart(fig_all_neg, use_container_width=True)

        st.divider()

        st.subheader("🔍 Input Ulasan Mata Kuliah")
        pilihan = st.selectbox("Pilih Mata Kuliah", sorted(summary['Matkul'].unique()))
        res = summary[summary['Matkul'] == pilihan].iloc[0]
        
        st.markdown(f"""<div style="background:white;padding:25px;border-radius:15px;border-left:10px solid {'#90a955' if res['Status_Umum']=='Positif' else '#dd2d4a'}; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    <h1 style="margin:0;color:{'#90a955' if res['Status_Umum']=='Positif' else '#dd2d4a'}">{res['Status_Umum']}</h1>
                    </div>""", unsafe_allow_html=True)
        
         # --- BAGIAN UPDATE: NOTIFIKASI & RESET KOLOM ---
        with st.expander(f"➕ Berikan Ulasan Baru untuk {pilihan}"):
            with st.form("input_form", clear_on_submit=True): # Kolom bersih setelah pencet Kirim
                s = st.text_input("Suka")
                k = st.text_input("Kendala")
                u = st.text_area("Umum")
                
                if st.form_submit_button("Kirim"):
                    if s.strip() == "" and k.strip() == "" and u.strip() == "":
                        st.warning("Mohon isi ulasan sebelum mengirim.")
                    else:
                        new_data = pd.DataFrame([{'Matkul': pilihan, 'Suka': s, 'Kendala': k, 'Umum': u}])
                        st.session_state.main_df = pd.concat([st.session_state.main_df, new_data], ignore_index=True)
                        st.success("✅ ULASAN TERKIRIM!")
  
    elif menu == "Data Master (Admin)":
        st.title("⚙️ Manajemen Data Master")
        
        # 1. Fitur Upload Berkas Baru
        up = st.file_uploader("Upload Excel/CSV", type=['xlsx', 'csv'], key="admin_up")
        if up:
            new_df = pd.read_excel(up) if up.name.endswith('.xlsx') else pd.read_csv(up)
            st.session_state.main_df = new_df
            # SIMPAN PERMANEN HASIL UPLOAD
            new_df.to_excel('evaluasi matkul.xlsx', index=False) 
            st.success("Update Berhasil & File Excel Diperbarui!")
            st.rerun()

        st.divider()

        # 2. Tabel Editor (Data diambil dari memori)
        edited_df = st.data_editor(st.session_state.main_df, num_rows="dynamic", use_container_width=True, key="master_edit")
        
        # 3. TOMBOL SIMPAN PERMANEN (WAJIB ADA)
        if st.button("💾 Simpan Perubahan", type="primary", use_container_width=True):
            # Update memori aplikasi
            st.session_state.main_df = edited_df 
            
            # TULIS ULANG KE FILE FISIK (Ini biar tidak hilang saat refresh)
            edited_df.to_excel('evaluasi matkul.xlsx', index=False) 
            
            st.success("✅ BERHASIL! Data sekarang sudah tersimpan permanen di file Excel.")
            st.balloons()
            st.rerun()

    elif menu == "Tentang":
        st.title("ℹ️ Tentang Sistem")
        st.divider()
        
        # 1. Ringkasan Sistem
        st.markdown("### 📊 Ringkasan Sistem")
        c1, c2, c3 = st.columns(3)
        c1.metric("Metode", "Naive Bayes")
        c2.metric("Dataset", f"{len(st.session_state.main_df)} Baris")
        c3.metric("Akurasi Model", "93,14%") 

        st.divider()
        
        # 2. Alur Kerja Sistem
        st.markdown("### 🛠️ Alur Kerja Sistem")
        
        # --- TAMBAH DETAIL ALUR ---
        with st.expander("🔍 Tahap 1: Preprocessing (Pembersihan Teks)"):
            st.write("""
            Pada tahap ini, ulasan mahasiswa dibersihkan:
            * **Case Folding**: Mengubah teks menjadi huruf kecil.
            * **Filtering**: Menghapus angka dan tanda baca.
            * **Tokenizing**: Mengubah kalimat menjadi per kata.        
            * **Stopword Removal**: Menghapus kata umum.
            * **Stemming**: Mengubah kata menjadi kata dasar.
            """)

        with st.expander("🔢 Tahap 2: Pembobotan TF-IDF"):
            st.write("""
            Data teks diubah menjadi bentuk angka (vektor) menggunakan metode **TF-IDF**. 
            Metode ini menghitung seberapa penting suatu kata dalam sebuah ulasan relatif terhadap seluruh ulasan yang ada.
            """)

        with st.expander("🤖 Tahap 3: Klasifikasi Naive Bayes"):
            st.write("""
            Algoritma **Naive Bayes** digunakan untuk menghitung probabilitas ulasan masuk ke kategori **Positif** atau **Negatif** berdasarkan pola kata yang telah dipelajari dari data latih.
            """)
        # ------------------------------------------

        st.divider()
        st.write("Aisyah Qurrata Ayun - Informatika Adzkia.")