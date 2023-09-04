import time
import pyautogui
import tkinter as tk
from pynput import keyboard
from threading import Thread

search_active = True  # Variável para controlar o estado de busca
button = None  # Variável para armazenar o botão

def on_press(key):
    global search_active, button
    try:
        if key == keyboard.Key.ctrl_l and search_active:
            search_active = not search_active  # Inverte o estado de busca
            print("Busca pausada...")
            button.config(text="Desligado", bg="#FFC0C0")  # Altera o texto e a cor do botão para vermelho mais claro
    except AttributeError:
        pass

def encontrar_notificacao():
    while search_active:
        print("Procurando notificação...")
        notificacao = pyautogui.locateOnScreen('.\PrintClient3.png')
        if notificacao is not None:
            print("Notificação encontrada!")
            return notificacao
        time.sleep(2)  # Espera 2 segundos antes de verificar novamente

def clicar_notificacao():
    while True:  # Executa em loop infinito
        if search_active:
            notificacao = encontrar_notificacao()
            if notificacao is not None:
                centro_notificacao = pyautogui.center(notificacao)
                pyautogui.click(centro_notificacao)
                time.sleep(10)  # Espera 10 segundos após clicar na notificação

def toggle_search():
    global search_active, button
    search_active = not search_active  # Inverte o estado de busca
    if search_active:
        print("Busca ativada...")
        button.config(text="Ligado", bg="#C0FFC0")  # Altera o texto e a cor do botão para verde mais claro
    else:
        print("Busca pausada...")
        button.config(text="Desligado", bg="#FFC0C0")  # Altera o texto e a cor do botão para vermelho mais claro

def close_program():
    global search_active
    search_active = False  # Define a busca como inativa
    root.quit()  # Encerra o loop principal da interface gráfica

def start_gui():
    global button, root
    # Cria a interface gráfica
    root = tk.Tk()
    root.title("Controle de Busca")
    root.resizable(False, False)  # Impede a janela de ser redimensionada

    # Obtém as dimensões da tela
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calcula as coordenadas para posicionar a janela no centro
    window_width = 200  # Largura da janela
    window_height = 100  # Altura da janela
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Define a posição da janela
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Cria o botão
    button = tk.Button(root, text="Ligado", command=toggle_search, width=20, height=4, bg="#C0FFC0", font=("Arial", 14))
    button.pack(padx=10, pady=10)

    # Configura o listener para capturar eventos do teclado
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # Configura o evento para fechar a janela
    root.protocol("WM_DELETE_WINDOW", close_program)

    # Inicia o loop de eventos da interface gráfica
    root.mainloop()

# Cria uma thread para iniciar a interface gráfica
gui_thread = Thread(target=start_gui)
gui_thread.daemon = True
gui_thread.start()

# Chamando a função para clicar na notificação
clicar_notificacao()