import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.interpolate import make_interp_spline
import io
import time

# 1. КОНФІГУРАЦІЯ
st.set_page_config(page_title="Мандала У-СІН", layout="wide")

# 2. ЛОГІКА У-СІН (Послідовність Творення)
# Дерево -> Вогонь -> Земля -> Метал -> Вода
ELEMENTS = ["Дерево", "Вогонь", "Земля", "Метал", "Вода"]
ELEMENT_COLORS = ["#2ecc71", "#e74c3c", "#f1c40f", "#ecf0f1", "#3498db"]

def get_wuxing_data(day, month):
    # Математичний розподіл: кожен елемент отримує вагу на основі залишку від ділення
    base_idx = (day + month) % 5
    values = [1.0] * 5
    values[base_idx] = 1.8  # Акцентний елемент
    values[(base_idx + 1) % 5] = 1.4  # Підтримуючий елемент
    return values

# 3. ПАНЕЛЬ КЕРУВАННЯ
st.sidebar.header("📥 Вхідні дані")
with st.sidebar:
    eye_color = st.selectbox("Колір очей", [1, 2, 3, 4], 
                             format_func=lambda x: {1:"Блакитні", 2:"Зелені", 3:"Карі", 4:"Янтарні"}[x])
    G = st.radio("Стать", [1, -1], format_func=lambda x: "Чоловіча" if x == 1 else "Жіноча")
    st.markdown("---")
    d = st.number_input("День", 1, 31, 12)
    m = st.number_input("Місяць", 1, 12, 5)
    age = st.slider("Вік", 1, 100, 30)
    st.markdown("---")
    run_anim = st.checkbox("🌀 Жива мандала", value=True)

# 4. ГЕНЕРАТОР
def generate_mandala(phase=0):
    w_values = get_wuxing_data(d, m)
    
    # Налаштування стилю (однакова товщина для всіх ліній)
    LW = 2.0 
    cmap = {1: cm.winter, 2: cm.summer, 3: cm.autumn, 4: cm.spring}[eye_color]
    
    fig = plt.figure(figsize=(10, 10), facecolor='black')
    ax = plt.subplot(111, projection='polar')
    ax.set_facecolor('black')
    
    # --- 1. ПЛАВНИЙ П'ЯТИКУТНИК (Ядро У-СІН) ---
    # Використовуємо інтерполяцію для згладжування кутів
    angles = np.linspace(0, 2*np.pi, 6)
    r_vals = w_values + [w_values[0]]
    
    # Створюємо плавну криву через вершини
    smooth_angles = np.linspace(0, 2*np.pi, 200)
    # Проста синусоїдальна інтерполяція для м'якості
    r_smooth = np.interp(smooth_angles, angles, r_vals) 
    # Додаткове згладжування для ефекту "пелюстки"
    r_mandala = r_smooth + 0.1 * np.sin(5 * smooth_angles) 
    
    ax.plot(smooth_angles, r_mandala, color='white', lw=LW, alpha=0.8)
    ax.fill(smooth_angles, r_mandala, color=cmap(0.5), alpha=0.2)

    # --- 2. БІОРИТМИ (Хвилі життя) ---
    t = np.linspace(0, 2*np.pi, 500)
    for i, val in enumerate(w_values):
        # Кожна стихія — окрема гармоніка
        r_wave = 2.5 + 0.3 * np.sin((i+1)*t + phase)
        ax.plot(t, r_wave, color=cmap(i/5), lw=LW, alpha=0.6)

    # --- 3. СПІРАЛЬ ФЕРМА (Досвід) ---
    indices = np.arange(1, age + 1)
    phi_gold = 2.39996 # Золотий кут
    theta_f = indices * phi_gold + phase * 0.05
    r_f = 0.15 * np.sqrt(indices)
    ax.scatter(theta_f, r_f, s=50, color='white', edgecolors=cmap(0.3), alpha=0.8)

    # --- 4. МЕЖА (Стать) ---
    p = 0.6 if G == 1 else 1.4
    N = 12
    r_border = 4.0 + 0.4 * (np.abs(np.sin(N * t)))**p
    ax.plot(t, r_border, color=cmap(0.9), lw=LW)

    ax.set_ylim(0, 5)
    ax.set_axis_off()
    return fig

# 5. ВІДОБРАЖЕННЯ ТА МАТЕМАТИЧНЕ ОБҐРУНТУВАННЯ
tab1, tab2 = st.tabs(["✨ Мандала", "📐 Математичне обґрунтування"])

with tab1:
    placeholder = st.empty()
    if run_anim:
        for i in range(100):
            fig = generate_mandala(phase=i*0.1)
            placeholder.pyplot(fig)
            plt.close(fig)
            time.sleep(0.05)
    else:
        st.pyplot(generate_mandala())

with tab2:
    st.header("Математична модель особистості")
    
    # Таблиця У-СІН
    st.subheader("1. Послідовність У-СІН")
    st.table({
        "Стихія": ELEMENTS,
        "Логіка": ["Народження, ріст", "Активність, пік", "Стабільність, баланс", "Стиснення, досвід", "Спокій, ресурс"],
        "Математичний індекс": [0, 1, 2, 3, 4]
    })

    st.subheader("2. Аналіз кривих")
    
    st.markdown("""
    | Елемент | Формула | Вхідні дані |
    | :--- | :--- | :--- |
    | **Ядро (Згладжений п'ятикутник)** | $r(\theta) = f_{spline}(w_i)$ | День + Місяць народження |
    | **Біоритми (Синусоїди)** | $r = R + A \cdot \sin(\omega t + \phi)$ | Послідовність стихій |
    | **Поле досвіду (Спіраль Ферма)** | $r = c\sqrt{k}, \theta = k \cdot \psi$ | Вік ($A$) |
    | **Захисний контур (Епіциклоїда)** | $r = R + |\sin(N\theta)|^p$ | Стать ($G$) |
    """)

    st.latex(r"r_{total} = \sum_{i=1}^{5} \text{Element}_i + \text{Gender\_Shape}(G)")
    st.write("**Геометричний сенс:**")
    st.write("- **Згладжування:** Використано лінійну інтерполяцію значень У-СІН з накладанням високої гармоніки для м'якості.")
    st.write("- **Стать ($G$):** Показник степеня $p$ змінює кривизну межі: гострі вершини для чоловічої енергії ($p < 1$) та закруглені для жіночої ($p > 1$).")
