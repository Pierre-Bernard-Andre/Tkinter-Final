import tkinter as tk
from tkinter import Label, Button, filedialog, Menu, messagebox
import speedtest
import threading
import sys

# Deklare variab st nan nivo global
st = speedtest.Speedtest()

# Fonksyon pou kòmanse tès la
def start_speedtest():
    # Fonksyon pou ekzekite tès la nan yon tretman paralèl
    def run_speedtest():
        while not stop_test:
            # Kòd tès la
            download_speed = st.download() / 10**6  # Nan megabit/s
            upload_speed = st.upload() / 10**6  # Nan megabit/s
            
            # Afiche rezilta yo nan etikèt la nan tan reyèl
            result_label.config(text=f"Vitès Download: {download_speed:.2f} Mbps\nVitès Upload: {upload_speed:.2f} Mbps")
            
            # Kòmanse yon tèt-an-tèt nan tès yo
            st.get_best_server()
    
    global stop_test
    stop_test = False
    
    # Kreye yon tretman paralèl pou tès la
    speedtest_thread = threading.Thread(target=run_speedtest)
    speedtest_thread.start()

# Fonksyon pou sispann tès la
def stop_speedtest():
    global stop_test
    stop_test = True
    result_label.config(text="Tès vitès rezo sispann.")

# Fonksyon pou ekspòte rezilta tès yo nan yon fichye
def export_results():
    # Kreye yon bo fenèt pou chwazi kote pou sovgade fichye a
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    
    if file_path:
        # Ouvri fichye a pou ekri rezilta tès yo
        with open(file_path, "w") as file:
            download_speed = st.download() / 10**6  # Nan megabit/s
            upload_speed = st.upload() / 10**6  # Nan megabit/s
            
            file.write(f"Vitès Download: {download_speed:.2f} Mbps\nVitès Upload: {upload_speed:.2f} Mbps")

# Fonksyon pou kite aplikasyon an
def quit_app():
    sys.exit()

# Fonksyon pou afiche dokimantasyon
def show_documentation():
    documentation = """
    Aplikasyon Tès Vitès Rezo

    1. Klike sou bouton "Demare Tès" pou kòmanse tès vitès rezo a.
    2. Pou sispann tès la, klike sou bouton "Kanpe Tès."
    3. Pou ekspòte rezilta tès yo nan yon fichye, klike sou bouton "Ekspòte Rezilta."
    4. Klike sou "Kite" nan meni an pou kite aplikasyon an.

    Aplikasyon sa a pèmèt ou tès vitès download ak upload nan rezo a nan tan reyèl.
    """
    messagebox.showinfo("Dokimantasyon", documentation)

# Kreye fenèt Tkinter
root = tk.Tk()
root.title("Aplikasyon Tès Vitès Rezo")

# Kreye yon meni pou dokimantasyon
menu = Menu(root)
root.config(menu=menu)
documentation_menu = Menu(menu)
menu.add_cascade(label="Dokimantasyon", menu=documentation_menu)
documentation_menu.add_command(label="Vizyèlize Dokimantasyon", command=show_documentation)

# Kreye yon bouton "Ekspòte Rezilta" nan meni an
menu.add_command(label="Ekspòte Rezilta", command=export_results)

# Kreye yon meni andènye nan meni an pou bouton "Kite"
sub_menu = Menu(menu)
menu.add_cascade(label="Kite", menu=sub_menu)
sub_menu.add_command(label="Kite Aplikasyon", command=quit_app)

# Kreye yon etikèt pou afiche rezilta tès yo nan tan reyèl
result_label = Label(root, text="", padx=20, pady=10)
result_label.pack()

# Kreye bouton pou demare tès la
start_button = Button(root, text="Demare Tès", command=start_speedtest)
start_button.pack()

# Kreye bouton pou sispann tès la
stop_button = Button(root, text="Kanpe Tès", command=stop_speedtest)
stop_button.pack()

# Retire limite a nan fenèt la pou li pran tout ekran
root.attributes("-fullscreen", True)

# Lanse aplikasyon an
root.mainloop()
