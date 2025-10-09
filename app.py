import streamlit as st
import pandas as pd
import os
import json
import math
from io import BytesIO

STATE_FILE = "keyword_rotation_state.json"

# Marketplace domain eşlemesi
DOMAIN_MAP = {
    'DE': 'de',
    'FR': 'fr',
    'IT': 'it',
    'ES': 'es',
    'UK': 'co.uk',
    'IE': 'ie',
    'PL': 'pl',
    'SE': 'se',
    'TR': 'com.tr',
    'NL': 'nl',
    'BE': 'com.be'
}

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def process_file(file):
    df = pd.read_excel(file)
    required_cols = ['Marketplace', 'Class', 'Keywords']
    if not all(col in df.columns for col in required_cols):
        st.error(f"Excel dosyasında şu sütunlar olmalı: {required_cols}")
        return None

    state = load_state()
    result_rows = []

    for mp in df['Marketplace'].unique():
        mp_clean = str(mp).strip().upper()
        mp_df = df[df['Marketplace'].str.strip().str.upper() == mp_clean]
        domain = DOMAIN_MAP.get(mp_clean, 'com')

        for cls in mp_df['Class'].unique():
            cls_df = mp_df[mp_df['Class'] == cls]
            keywords_str = cls_df['Keywords'].values[0]
            keywords = [k.strip() for k in str(keywords_str).split(',') if k.strip()]
            if len(keywords) == 0:
                continue

            key = f"{mp_clean}_{cls}"
            start_idx = state.get(key, 0)
            total_keywords = len(keywords)

            group = []
            for i in range(4):
                idx = (start_idx + i) % total_keywords
                group.append(keywords[idx])

            state[key] = (start_idx + 4) % total_keywords
            rotation_number = math.floor(start_idx / 4) + 1

            links = []
            for kw in group:
                url = f"https://www.amazon.{domain}/s?k={kw.replace(' ', '+')}"
                links.append(f'=HYPERLINK("{url}","🔍 {kw}")')

            result_rows.append({
                'Marketplace': mp_clean,
                'Class': cls,
                'Rotation': rotation_number,
                'Keyword 1': links[0],
                'Keyword 2': links[1],
                'Keyword 3': links[2],
                'Keyword 4': links[3]
            })

    save_state(state)
    result_df = pd.DataFrame(result_rows)

    # Excel'e kaydet
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        result_df.to_excel(writer, index=False, sheet_name='Keywords')
        worksheet = writer.sheets['Keywords']
        worksheet.set_column('A:G', 30)
    output.seek(0)
    return output


# --- Streamlit UI ---
st.set_page_config(page_title="Keyword Rotasyonu - Linkli Excel", layout="centered")
st.title("🔁 Keyword Rotasyonu - Linkli Excel Oluşturucu")

uploaded_file = st.file_uploader("Keyword Excel dosyasını yükleyin (.xlsx veya .xls)", type=["xlsx", "xls"])

if uploaded_file:
    if st.button("4'lü Linkli Excel Oluştur"):
        result = process_file(uploaded_file)
        if result:
            st.success("✅ Excel dosyası başarıyla oluşturuldu!")
            st.download_button(
                label="📥 Dosyayı İndir",
                data=result,
                file_name="rotated_keywords_with_links.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
