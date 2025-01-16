import flet as ft
from app import components


class AttenuationCoefficientsView(ft.UserControl):
    def __init__(self, page: ft.Page, data: list):
        super().__init__()
        self.page = page
        self.data = data

    def build(self):
        return ft.Column(
            controls=[
                components.MenuBar(self.page),
                components.AttenuationCoefficientsDataTable(self.page, self.data),
            ],
            expand=True,
        )