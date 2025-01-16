import flet as ft
from app import components


class HomeView(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

    def build(self):
        return ft.Column(
            controls=[components.MenuBar(self.page)],
            expand=True,
        )
