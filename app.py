import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import time

# 1. КОНФІГУРАЦІЯ
st.set_page_config(page_title="Цифрова мандала особистості", layout="wide")
st.title("🎨 Цифрова мандала особистості")

# 2. КОНСТАНТИ У-СІН
ELEMENTS = ["Дерево", "Вогонь", "Земля", "Метал", "Вода"]
DESCRIPTIONS = {
    "Дерево": {"якості": "Ріст, гнучкість, креатив", "ризики": "Гнів, напруження печінки", "колір": "#2ecc71"},
    "Вогонь": {"якості": "Експресія, радість, харизма", "ризики": "Тривожність, серцево-судинна система", "колір": "#e74c3c"},
    "Земля": {"якості": "Стабільність, турбота, баланс", "ризики": "Зацикленість, травлення", "колір": "#f1c40f"},
    "Метал": {"якості": "Структура, воля, дисципліна", "ризики": "Смуток, дихальна система", "колір": "#ecf0f1"},
    "Вода": {"якості": "Мудрість, глибина, ресурс", "ризики": "Страхи, нирки та кістки", "колір": "#3498db"}
}

def get_wuxing_analysis(day, month):
    # Математичний розподіл сил (залишаємо вашу логіку)
    base_idx = (day + month) % 5
    values = [1.2] * 5
    values[base_idx] = 2.2  # Домінант
    values[(base_idx + 1) % 5] = 1.6  # Підтримка
    values[(base_idx + 3) % 5] = 0.8  # Дефіцит (цикл пригнічення)
    return values

# 3. ІНТЕРФЕЙС
with st.sidebar:
    st.header("📋 Персональні дані")
    eye_color = st.selectbox("Колір очей", [1, 2, 3, 4], 
                             format_func=lambda x: {1:"Блакитні", 2:"Зелені", 3:"Карі", 4:"Янтарні"}[x])
    G = st.radio("Стать", [1, -1], format_func=lambda x: "Чоловіча" if x == 1 else "Жіноча")
    st.markdown("---")
    d = st.number_input("День", 1, 31, 12)
    m = st.number_input("Місяць", 1, 12, 5)
    age = st.slider("Вік", 1, 100, 30)
    st.markdown("---")
    run_anim = st.checkbox("🌀 Жива мандала", value=True)

# 4. ГЕНЕРАТОР (Оптимізація розміру)
def generate_mandala(phase=0):
    w_values = get_wuxing_analysis(d, m)
    LW = 2.0  # Стала товщина ліній
    cmap = {1: cm.winter, 2: cm.summer, 3: cm.autumn, 4: cm.spring}[eye_color]
    
    # figsize=(8,8) робить графік компактнішим
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8), facecolor='black')
    ax.set_facecolor('black')
    
    t = np.linspace(0, 2 * np.pi, 500)

    # --- ЯДРО (5 СТИХІЙ) ---
    r_core = np.zeros_like(t)
    for i, val in enumerate(w_values):
        r_core += val * np.exp(-((t - i * 2 * np.pi / 5)**2) / 0.6)
    
    r_core = 0.5 + 1.2 * (r_core / np.max(r_core))
    ax.plot(t, r_core, color='white', lw=LW, alpha=0.9)
    ax.fill(t, r_core, color=cmap(0.5), alpha=0.2)

    # --- БІОРИТМИ ---
    for i in range(5):
        r_wave = 2.4 + 0.3 * np.sin((i+1)*t + phase)
        ax.plot(t, r_wave, color=cmap(i/5), lw=LW, alpha=0.5)

    # --- ДОСВІД (Спіраль Ферма) ---
    indices = np.arange(1, age + 1)
    theta_f = indices * 2.39996 + phase * 0.05
    r_f = 0.15 * np.sqrt(indices)
    ax.scatter(theta_f, r_f, s=40, color='white', edgecolors=cmap(0.3), alpha=0.7)

    # --- МЕЖА ---
    p = 0.6 if G == 1 else 1.4
    r_border = 4.0 + 0.3 * (np.abs(np.sin(10 * t)))**p
    ax.plot(t, r_border, color=cmap(0.9), lw=LW)

    # Масштабування, щоб мандала не виглядала порожньою
    ax.set_ylim(0, 5) 
    ax.set_axis_off()
    return fig

# 5. ВКЛАДКИ
tab1, tab2 = st.tabs(["✨ Візуалізація", "📐 Математичне обґрунтування"])

with tab1:
    col_img, col_info = st.columns([2, 1])
    
    w_vals = get_wuxing_analysis(d, m)
    dominant_idx = np.argmax(w_vals)
    weak_idx = np.argmin(w_vals)
    
    with col_img:
        placeholder = st.empty()
        if run_anim:
            for i in range(50):
                fig = generate_mandala(phase=i*0.1)
                placeholder.pyplot(fig)
                plt.close(fig)
        else:
            st.pyplot(generate_mandala())

    with col_info:
        st.subheader("📊 Діагностика У-СІН")
        
        # Переважна стихія
        st.success(f"**Домінанта: {ELEMENTS[dominant_idx]}**")
        st.write(f"*{DESCRIPTIONS[ELEMENTS[dominant_idx]]['якості']}*")
        
        # Дефіцит
        st.error(f"**Дефіцит: {ELEMENTS[weak_idx]}**")
        st.write(f"Нестача енергії {ELEMENTS[weak_idx]} може призводити до: {DESCRIPTIONS[ELEMENTS[weak_idx]]['ризики']}.")
        
        st.markdown("---")
        st.warning("**Прогноз ризиків:**")
        st.write(f"Зверніть увагу на {DESCRIPTIONS[ELEMENTS[dominant_idx]]['ризики']} через надмірну активність стихії.")

with tab2:
    st.header("Математичне обґрунтування")
    st.write("Мандала побудована на системі полярних координат, де кожен параметр життя трансформується у геометричний коефіцієнт.")
    
    st.latex(r"r(\theta)_{core} = \sum V_i e^{-\frac{(\theta-\theta_i)^2}{2\sigma^2}}")
    st.write("— Формула згладжування п'ятикутника У-СІН.")
    
    st.latex(r"r_{border} = R + A \cdot |\sin(N\theta)|^p")
    st.write(f"— Формула межі, де $p={0.6 if G==1 else 1.4}$ визначає тип енергії (Янь/Інь).")
