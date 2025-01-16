import flet as ft


class Content(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

    def build(self):
        return ft.Container(
            content=ft.Column([], spacing=10),
            bgcolor="black",
            expand=True,
            padding=10,
        )
