import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import time

# 1. КОНФІГУРАЦІЯ ТА СТИЛЬ
st.set_page_config(page_title="Цифрова мандала особистості", layout="wide")
st.title("🎨 Цифрова мандала особистості")

# 2. МАТЕМАТИЧНА ЛОГІКА ТА ПАРАМЕТРИ
ELEMENTS = ["Дерево", "Вогонь", "Земля", "Метал", "Вода"]
DESCRIPTIONS = {
    "Дерево": {"якості": "Ріст, гнучкість, печінка", "ризики": "Гнів, напруження", "колір": "#2ecc71"},
    "Вогонь": {"якості": "Радість, активність, серце", "ризики": "Тривожність, безсоння", "колір": "#e74c3c"},
    "Земля": {"якості": "Стабільність, турбота, шлунок", "ризики": "Зацикленість, важкість", "колір": "#f1c40f"},
    "Метал": {"якості": "Дисципліна, структура, легені", "ризики": "Смуток, замкненість", "колір": "#ecf0f1"},
    "Вода": {"якості": "Мудрість, ресурс, нирки", "ризики": "Страхи, пасивність", "колір": "#3498db"}
}

def analyze_birth_date(day, month, year):
    # Математичне визначення сил стихій за датою народження
    base_idx = (day + month + year % 100) % 5
    strengths = [1.2] * 5
    strengths[base_idx] = 2.0       # Домінанта (Акцентна стихія)
    strengths[(base_idx + 1) % 5] = 1.6  # Підтримка (Цикл творення)
    strengths[(base_idx + 3) % 5] = 0.8  # Слабкість (Цикл пригнічення)
    return strengths, base_idx

# 3. SIDEBAR (ВХІДНІ ДАНІ)
with st.sidebar:
    st.header("📋 Параметри системи")
    d = st.number_input("День народження", 1, 31, 15)
    m = st.number_input("Місяць", 1, 12, 6)
    y = st.number_input("Рік", 1900, 2026, 1990)
    st.markdown("---")
    eye_color = st.selectbox("Колір очей", [1, 2, 3, 4], 
                             format_func=lambda x: {1:"Блакитні", 2:"Зелені", 3:"Карі", 4:"Янтарні"}[x])
    G = st.radio("Стать", [1, -1], format_func=lambda x: "Чоловіча" if x == 1 else "Жіноча")
    S = st.slider("Параметр Сон (S)", 1, 10, 7)
    run_anim = st.checkbox("🌀 Жива мандала", value=True)

# 4. ГЕНЕРАТОР (ОПТИМІЗОВАНИЙ РОЗМІР)
def generate_mandala(phase=0):
    strengths, dom_idx = analyze_birth_date(d, m, y)
    cmap = {1: cm.winter, 2: cm.summer, 3: cm.autumn, 4: cm.spring}[eye_color]
    LW = 2.0
    
    # figsize=(6, 6) робить мандалу компактною
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(6, 6), facecolor='black')
    ax.set_facecolor('black')
    
    t = np.linspace(0, 2 * np.pi, 500)

    # --- 1. КІЛЬЦЕ СНУ (ЯДРО) ---
    # r = R + A*sin(S*theta)
    r_sleep = 0.7 + 0.1 * np.sin(S * t + phase * 2.5)
    ax.plot(t, r_sleep, color='white', lw=1.2, ls='--', alpha=0.8)

    # --- 2. П'ЯТИКУТНИК У-СІН (КАРКАС) ---
    angles = np.linspace(0, 2 * np.pi, 6)
    r_pent = strengths + [strengths[0]]
    ax.plot(angles, r_pent, color='white', lw=LW, marker='o', markersize=6)
    ax.fill(angles, r_pent, color=cmap(0.5), alpha=0.3)

    # --- 3. БІОРИТМИ (ХВИЛІ) ---
    for i, amp in enumerate(strengths):
        omega = (i + 1) * 0.6
        phi = (d * np.pi / 31) + phase
        r_wave = 2.5 + 0.4 * np.sin(omega * t + phi)
        ax.plot(t, r_wave, color=cmap(i/5), lw=1.5, alpha=0.5)

    # --- 4. ЗАХИСНА МЕЖА ---
    p = 0.6 if G == 1 else 1.4
    r_border = 4.2 + 0.3 * (np.abs(np.sin(10 * t)))**p
    ax.plot(t, r_border, color=cmap(0.95), lw=LW)

    ax.set_ylim(0, 5)
    ax.set_axis_off()
    return fig

# 5. ВКЛАДКИ
tab1, tab2 = st.tabs(["✨ Візуалізація", "📐 Математичне обґрунтування"])

with tab1:
    col_img, col_diag = st.columns([1.5, 1])
    
    strengths, dom_idx = analyze_birth_date(d, m, y)
    weak_idx = np.argmin(strengths)
    
    with col_img:
        placeholder = st.empty()
        if run_anim:
            for i in range(50):
                fig = generate_mandala(phase=i*0.1)
                placeholder.pyplot(fig)
                plt.close(fig)
        else:
            st.pyplot(generate_mandala())
            
    with col_diag:
        st.subheader("📊 Аналіз У-СІН")
        st.success(f"**Переважає: {ELEMENTS[dom_idx]}**")
        st.caption(DESCRIPTIONS[ELEMENTS[dom_idx]]["якості"])
        
        st.error(f"**Недостатньо: {ELEMENTS[weak_idx]}**")
        st.caption(f"Ризики: {DESCRIPTIONS[ELEMENTS[weak_idx]]['ризики']}")
        
        st.markdown("---")
        st.info(f"**Дата народження:** {d:02d}.{m:02d}.{y}")
        st.write(f"Параметр Сон **S={S}** модулює внутрішню стійкість системи.")

with tab2:
    st.header("Математичне обґрунтування моделі")
    
    st.subheader("1. Параметризація дати народження")
    st.write("Сили п'яти стихій $V_i$ розраховуються на основі циклічного залишку дати народження:")
    st.latex(r"Index_{dom} = (Day + Month + Year_{2dg}) \pmod 5")
    
    st.subheader("2. Крива внутрішнього ядра (Сон)")
    st.write("Описує базовий біоритм відновлення як функцію радіуса від кута:")
    st.latex(r"r(\theta) = R_{core} + A \cdot \sin(S \cdot \theta + \phi)")
    st.write(f"— де $S = {S}$ (ваш параметр сну) визначає частоту осциляцій кільця.")
    

    st.subheader("3. Геометрія ядра (П'ятикутник)")
    st.write("Побудований у полярних координатах через 5 вершин, що відповідають стихіям У-СІН:")
    st.latex(r"\theta_k = \frac{2\pi k}{5}, \quad r_k = strengths[k]")
    

    st.subheader("4. Біоритмічні хвилі")
    st.write("Суперпозиція гармонік, фаза яких залежить від дня народження:")
    st.latex(r"r_i = R_w + 0.4 \sin(\omega_i t + \frac{Day \cdot \pi}{31})")
