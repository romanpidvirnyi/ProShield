from typing import Any, Dict

import flet as ft


class StorageClassesDataTable(ft.UserControl):
    def __init__(self, page: ft.Page, data: list[Dict[str, Any]]):
        super().__init__()
        self.page = page
        self.data = data

    def get_data_rows(self):
        data_rows = []
        for item in self.data:
            data_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item["id"])),
                        ft.DataCell(ft.Text(item["description"])),
                        ft.DataCell(ft.Text(item["protection_class"])),
                        ft.DataCell(ft.Text(item["overpressure_air_blast_wave"])),
                        ft.DataCell(ft.Text(item["radiation_protection_level"])),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                tooltip="Редагувати",
                                on_click=lambda _: self.on_update_click(
                                    item["id"], item["name"]
                                ),
                                alignment=ft.alignment.center,
                            ),
                        ),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                tooltip="Видалити",
                                on_click=lambda _: self.on_delete_click("3"),
                                alignment=ft.alignment.center,
                            ),
                        ),
                    ]
                )
            )
        return data_rows

    def on_update_click(self, row_id: int, row_name: str):
        pass

    # Function to handle delete button click
    def on_delete_click(self, row_id):
        self.page.snack_bar = ft.SnackBar(ft.Text(f"Delete clicked for ID: {row_id}"))
        self.page.snack_bar.open()

    def build(self):
        return ft.Container(
            content=ft.DataTable(
                columns=[
                    ft.DataColumn(
                        ft.Container(
                            content=ft.Text("ID"),
                            alignment=ft.alignment.center,
                            padding=5,
                        )
                    ),
                    ft.DataColumn(
                        ft.Text(
                            "Розміщення сховищ, \nСПП із захисними \nвластивостями сховищ",
                            max_lines=5,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ),
                    ft.DataColumn(
                        ft.Text(
                            "Клас сховища, \nСПП із захисними \nвластивостями сховищ",
                            max_lines=5,
                            overflow=ft.TextOverflow.CLIP,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ),
                    ft.DataColumn(
                        ft.Container(
                            content=ft.Text(
                                "Надмірний тиск \nповітряної \nударної хвилі",
                                max_lines=5,
                                overflow=ft.TextOverflow.FADE,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            expand=True,
                        ),
                    ),
                    ft.DataColumn(
                        ft.Container(
                            content=ft.Text(
                                "Ступінь послаблення \nрадіаційного впливу \n(ступінь захисту)",
                                max_lines=5,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            expand=True,
                        )
                    ),
                    ft.DataColumn(
                        ft.Container(
                            content=ft.Text(""),
                            alignment=ft.alignment.center,
                        )
                    ),
                    ft.DataColumn(
                        ft.Container(
                            content=ft.Text(""),
                            alignment=ft.alignment.center,
                        ),
                    ),
                ],
                rows=self.get_data_rows(),
                expand=True,
                # bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                border_radius=5,
            ),
            width=self.page.window_width,
        )
