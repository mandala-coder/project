import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import io
import time

# 1. НАЛАШТУВАННЯ СТОРІНКИ
st.set_page_config(page_title="Мандала У-СІН 2.0", layout="wide")

st.title("🎨 Системна мандала: Психоматриця та У-СІН")
st.write("### Глибока візуалізація біоритмів та енергетичного балансу")
st.markdown("---")

# 2. ПАНЕЛЬ КЕРУВАННЯ
st.sidebar.header("📋 Персональні дані")
with st.sidebar:
    # Блок 1: Колірна гама
    eye_choice = st.selectbox("Колір очей (Палітра)", options=[1, 2, 3, 4], 
                              format_func=lambda x: {1:"Блакитні (Winter)", 2:"Зелені (Summer)", 3:"Карі (Autumn)", 4:"Янтарні (Spring)"}[x])
    
    # Блок 2: Форма межі
    G = st.radio("Стать (Геометрія межі)", options=[1, -1], format_func=lambda x: "Чоловіча (Гостра)" if x == 1 else "Жіноча (М'яка)")
    
    st.markdown("---")
    d = st.number_input("День народження", 1, 31, 15)
    n = st.number_input("Місяць народження", 1, 12, 6)
    
    st.markdown("---")
    A = st.slider("Вік", 1, 100, 45)
    T = st.slider("Енергія (Товщина ліній)", 1, 10, 5)
    E = st.slider("Впевненість (Яскравість)", 1, 10, 8)
    
    run_anim = st.checkbox("🌀 Запустити 'Живе дихання'", value=True)

# 3. РОЗРАХУНОК СТИХІЙ У-СІН
def calculate_wuxing(day, month, energy_val):
    base = (day + month) % 5
    strengths = [1.2, 1.2, 1.2, 1.2, 1.2] # Базовий баланс
    for i in range(5):
        strengths[(base + i) % 5] += (energy_val / 8.0) * np.sin(i)
    return strengths

# 4. ГЕНЕРАТОР МАНДАЛИ
def generate_advanced_mandala(phase=0):
    w_data = calculate_wuxing(d, n, T)
    
    # Налаштування стилю
    selected_cmap = {1: cm.winter, 2: cm.summer, 3: cm.autumn, 4: cm.spring}.get(eye_choice, cm.plasma)
    line_thickness = 1.5 + (T / 2.0) # Залежність від енергії
    brightness = 0.4 + (E / 20.0)    # Залежність від впевненості
    
    fig = plt.figure(figsize=(10, 10), facecolor='black')
    ax = plt.subplot(111, projection='polar')
    ax.set_facecolor('black')
    
    t = np.linspace(0, 2 * np.pi, 1000)
    
    # --- 1. РАДАР-ГРАФ У-СІН (Центр) ---
    angles = np.linspace(0, 2 * np.pi, 6)
    values = w_data + [w_data[0]]
    ax.fill(angles, values, color=selected_cmap(0.8), alpha=0.3)
    ax.plot(angles, values, color=selected_cmap(0.9), lw=line_thickness*1.5, marker='o', markersize=8)

    # --- 2. БІОРИТМИ (Яскраві хвилі) ---
    for i, strength in enumerate(w_data):
        omega = (i + 1) * 0.5
        phi = phase + (i * np.pi / 3)
        r_wave = 2.2 + (0.4 * np.sin(omega * t + phi) * strength)
        ax.plot(t, np.full_like(t, r_wave), alpha=brightness, color=selected_cmap(i/5), lw=line_thickness * 0.7)

    # --- 3. СПІРАЛЬ РОЗВИТКУ (Золотий перетин) ---
    phi_const = (1 + 5**0.5) / 2
    b_growth = np.log(phi_const) / (np.pi / 2)
    indices = np.arange(1, A + 1)
    theta_fib = indices * 0.5 + phase * 0.05
    r_fib = 0.25 * np.exp(b_growth * theta_fib * 0.08)
    ax.scatter(theta_fib, r_fib, s=T*15, c=indices, cmap=selected_cmap, alpha=0.9, edgecolors='white', lw=0.5)

    # --- 4. МЕЖА (Залежність від статі G) ---
    # Чоловіча (G=1) -> p=0.5 (гостра), Жіноча (G=-1) -> p=1.5 (м'яка)
    p_shape = 0.5 if G == 1 else 1.5
    N_peaks = int(10 + T) # Кількість зубців залежить від енергії
    
    breath = 1.0 + 0.05 * np.sin(phase)
    r_border_base = 4.2
    crown = (np.abs(np.sin(N_peaks * t)))**p_shape
    r_border = r_border_base + (0.6 * crown * breath)
    
    ax.plot(t, r_border, color=selected_cmap(0.95), lw=line_thickness * 1.2, alpha=0.9)
    ax.fill(t, r_border, color=selected_cmap(0.5), alpha=0.1)

    ax.set_ylim(0, 5.5)
    ax.set_axis_off()
    return fig

# 5. ВІДОБРАЖЕННЯ
tab1, tab2 = st.tabs(["🚀 Генератор У-СІН", "📜 Математика"])

with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("#### Характеристики")
        
        # 1. Визначаємо назву стилю заздалегідь
        if G == 1:
            style_name = "Неоновий зигзаг"
        else:
            style_name = "М'яка хвиля"
            
        # 2. Тепер просто виводимо змінні без складних конструкцій всередині {}
        st.write(f"**Стиль:** {style_name}")
        st.write(f"**Колір:** Palette {eye_choice}")
        
        st.markdown("---")
        st.caption("Ця мандала синтезує ваші біоритми. Товщина ліній прямо пропорційна вашій життєвій енергії (T).")

    with col2:
        placeholder = st.empty()
        if run_anim:
            for i in range(150):
                fig = generate_advanced_mandala(phase=i * 0.1)
                placeholder.pyplot(fig)
                plt.close(fig)
                time.sleep(0.04)
        else:
            fig = generate_advanced_mandala(phase=0)
            placeholder.pyplot(fig)

with tab2:
    st.header("Математика системної мандали 2.0")
    st.write("Ми поєднали психоматрицю з класичною геометрією:")
    
    st.latex(r"r_{border} = R_{base} + A \cdot |\sin(N \cdot \theta)|^p")
    st.write(f"Де показник $p = {0.5 if G==1 else 1.5}$ (визначено статтю).")
    
    st.latex(r"y(t) = \text{Energy} \cdot \sin(\omega t + \phi)")
    st.write("Колірна гама базується на картах: Winter, Summer, Autumn, Spring.")
