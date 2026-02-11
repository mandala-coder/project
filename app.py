import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- РОЗРАХУНКОВИЙ БЛОК (Математика У-СІН) ---
def calculate_wuxing(birth_date):
    # Тут ваша логіка перетворення дати в 5 чисел
    # Наприклад, сума цифр року, місяця тощо.
    return [1.0, 1.2, 0.8, 1.5, 0.9] # Повертає сили 5 елементів

# --- ВІЗУАЛІЗАЦІЯ ---
def generate_systemic_mandala(wuxing_data, phase):
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(10,10))
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')

    t = np.linspace(0, 2*np.pi, 1000)
    
    # 1. Радар-граф стихій (Фундамент здоров'я)
    angles = np.linspace(0, 2*np.pi, 6)
    values = wuxing_data + [wuxing_data[0]] # Замикаємо лінію
    ax.plot(angles, values, color='gold', lw=3)
    ax.fill(angles, values, color='gold', alpha=0.2)

    # 2. Біоритми (Хвилі активності органів)
    for i, amp in enumerate(wuxing_data):
        wave = 2.5 + 0.3 * np.sin((i+1)*t + phase) * amp
        ax.plot(t, wave, alpha=0.4, lw=1)

    # 3. Фрактальна межа (самоподібність)
    # Використовуємо рекурсивні пелюстки
    N = 10 # Кількість сегментів
    r_border = 3.5 + 0.2 * np.cos(N * t) * np.sin(phase)
    ax.plot(t, r_border, color='white', lw=0.5)

    ax.set_ylim(0, 5)
    ax.set_axis_off()
    return fig

# --- STREAMLIT UI ---
# (Залишаємо ваші вкладки та слайдери, але додаємо вибір Концепції)
mode = st.radio("Оберіть модель", ["Математична мандала", "Система У-СІН (Здоров'я)"])

if mode == "Система У-СІН (Здоров'я)":
    # Виклик нової функції
    w_data = calculate_wuxing(d) # Передаємо день народження
    fig = generate_systemic_mandala(w_data, phase=0)
    st.pyplot(fig)
