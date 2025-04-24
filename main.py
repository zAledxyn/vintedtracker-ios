from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App

KV = '''
#:import MDLabel kivymd.uix.label.MDLabel
ScreenManager:
    MenuScreen:
    DashboardScreen:

<MenuScreen>:
    name: "menu"
    MDLabel:
        text: "VintedTracker (Kivy)"
        halign: "center"
    MDRaisedButton:
        text: "Dashboard öffnen"
        pos_hint: {"center_x": .5, "center_y": .4}
        on_release: app.root.current = "dash"

<DashboardScreen>:
    name: "dash"
    MDLabel:
        text: "Dashboard (noch leer – kommt in Etappe 2)"
        halign: "center"
    MDRaisedButton:
        text: "Zurück"
        pos_hint: {"center_x": .5, "center_y": .1}
        on_release: app.root.current = "menu"
'''

class MenuScreen(Screen):
    pass

class DashboardScreen(Screen):
    pass

class VintedApp(App):
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.05, 1)  # Dark mode
        return Builder.load_string(KV)

if __name__ == "__main__":
    VintedApp().run()
