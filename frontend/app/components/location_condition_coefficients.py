from typing import Any, Dict

import flet as ft


class LocationConditionCoeficientDataTable(ft.UserControl):
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
                        ft.DataCell(ft.Text(item["building_type_name"])),
                        ft.DataCell(ft.Text(item["building_height_from"])),
                        ft.DataCell(ft.Text(item["building_height_to"])),
                        ft.DataCell(ft.Text(item["building_density"])),
                        ft.DataCell(ft.Text(item["coefficient"])),
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
                        )
                    ),
                    ft.DataColumn(ft.Container(content=ft.Text("Характер забудови"))),
                    ft.DataColumn(
                        ft.Container(content=ft.Text("Висота будинків \n(від), м"))
                    ),
                    ft.DataColumn(
                        ft.Container(content=ft.Text("Висота будинків \n(до), м"))
                    ),
                    ft.DataColumn(
                        ft.Container(content=ft.Text("Щільність\nзабудови, %"))
                    ),
                    ft.DataColumn(ft.Container(content=ft.Text("Коефіцієнт"))),
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
