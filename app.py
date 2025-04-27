import streamlit as st
import json

st.set_page_config(page_title="📌 Proje Öneri Sistemi", page_icon="🚀")
st.title("✨ Proje Öneri Sistemi")

# JSON'dan projeleri yükle
try:
    with open("projects.json", "r", encoding="utf-8") as f:
        projects = json.load(f)
except FileNotFoundError:
    st.error("Projeler dosyası bulunamadı! Lütfen 'projects.json' dosyasını kontrol edin.")
    projects = []

# Eğer proje verisi yoksa uygulamayı durdur
if not projects:
    st.stop()

# Filtreleme seçenekleri
languages = sorted(set(p["language"] for p in projects))
difficulties = sorted(set(p["difficulty"] for p in projects))
databases = sorted(set(p["database"] for p in projects))
statuses = ["Hepsi", "Başlandı", "Tamamlandı", "Devam Ediyor"]
categories = ["Hepsi", "Web", "Mobil", "Veri Bilimi", "Yapay Zeka", "Oyun Geliştirme", "Blockchain"]

# Filtreler
st.sidebar.header("🔎 Filtreleme Seçenekleri")
language = st.sidebar.selectbox("Programlama Dili", ["Hepsi"] + languages)
difficulty = st.sidebar.selectbox("Zorluk Seviyesi", ["Hepsi"] + difficulties)
database = st.sidebar.selectbox("Veritabanı", ["Hepsi"] + databases)
status = st.sidebar.selectbox("Proje Durumu", statuses)
category = st.sidebar.selectbox("Proje Kategorisi", categories)
online_only = st.sidebar.checkbox("Sadece çevrimiçi projeleri göster")
search_term = st.sidebar.text_input("🔍 Başlık veya açıklamada ara")

# Filtreleme işlemi
filtered = []
for p in projects:
    if language != "Hepsi" and p["language"] != language:
        continue
    if difficulty != "Hepsi" and p["difficulty"] != difficulty:
        continue
    if database != "Hepsi" and p["database"] != database:
        continue
    if status != "Hepsi" and p["status"] != status:
        continue
    if category != "Hepsi" and p["category"] != category:
        continue
    if online_only and not p["online"]:
        continue
    if search_term and search_term.lower() not in (p["title"] + p["description"]).lower():
        continue
    filtered.append(p)

# Sonuçları göster
st.subheader(f"🔍 {len(filtered)} proje bulundu:")

if filtered:
    for proj in filtered:
        with st.container():
            st.markdown(f"### {proj['title']}")
            st.write(f"**Dil**: {proj['language']} | **Zorluk**: {proj['difficulty']} | **Kategori**: {proj['category']}")
            st.write(f"**Veritabanı**: {proj['database']} | **Durum**: {proj['status']} | {'🌐 Çevrimiçi' if proj['online'] else '💾 Çevrimdışı'}")
            st.write(f"**Açıklama**: {proj['description']}")
            st.markdown(f"[🔗 Projeye Git]({proj['link']})")
            st.markdown("---")
else:
    st.info("Filtrelere uygun proje bulunamadı. 😊")
