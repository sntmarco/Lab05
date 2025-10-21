import flet as ft
from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    txt_nuova_auto = ft.Text(value="Aggiungi nuova auto", size=20)
    marca = ft.TextField(label = "Marca")
    modello = ft.TextField(label = "Modello")
    anno = ft.TextField(label = "Anno")
    num_posti = ft.TextField(value="0", text_align="right", width=100)

    # Codice del contatore importato dalla documentazione di Flet
    def minus_click(e):
        num_posti.value = str(int(num_posti.value) - 1)
        page.update()

    def plus_click(e):
        num_posti.value = str(int(num_posti.value) + 1)
        page.update()
    page.update()

    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    def Aggiungi_auto(marca, modello, anno_int, num_posti_int):
        Autonoleggio.aggiungi_automobile(autonoleggio, marca, modello, anno_int, num_posti_int)
        print("Auto aggiunta con successo!")
        page.update()

    def aggiungi_automobile_click(e):
        # Validazione dei campi
        if not marca.value:
            marca.error_text = "Campo obbligatorio"
            alert.show_alert("❌ Inserisci la marca")
            page.update()
            return
        else:
            marca.error_text = None

        if not modello.value:
            modello.error_text = "Campo obbligatorio"
            alert.show_alert("❌ Inserisci il modello")
            page.update()
            return
        else:
            modello.error_text = None

        if not anno.value or not anno.value.isdigit() or len(anno.value) != 4:
            anno.error_text = "Inserisci un anno valido"
            alert.show_alert("❌ Inserisci un anno valido")
            page.update()
            return
        else:
            anno.error_text = None

        if not num_posti.value or not num_posti.value.isdigit() or int(num_posti.value) <= 0:
            num_posti.error_text = "Numero posti non valido"
            alert.show_alert("❌ Inserisci un numero valido di posti")
            page.update()
            return
        else:
            num_posti.error_text = None

        num_posti_int = int(num_posti.value)
        anno_int = int(anno.value)
        Aggiungi_auto(marca.value, modello.value, anno_int, num_posti_int)
        aggiorna_lista_auto()

        #Dopo aver aggiunto la nuova auto alla lista ripristina campi per inserimento
        marca.value = ""
        modello.value = ""
        anno.value = ""
        num_posti.value = "0"
        marca.error_text = None
        modello.error_text = None
        anno.error_text = None
        num_posti.error_text = None
        page.update()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    pulsante_conferma_auto = ft.ElevatedButton("Aggiungi", on_click=aggiungi_automobile_click)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),

        # Sezione 3
        txt_nuova_auto,
        ft.Row(spacing=30,
               controls=[marca, modello, anno, ft.IconButton(ft.Icons.REMOVE, on_click=minus_click),
                num_posti,
                ft.IconButton(ft.Icons.ADD, on_click=plus_click),],
               alignment=ft.MainAxisAlignment.CENTER),
        pulsante_conferma_auto,
        ft.Divider(),

        # Sezione 4
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)