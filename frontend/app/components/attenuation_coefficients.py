from typing import Any, Dict

import flet as ft


class AttenuationCoefficientsDataTable(ft.UserControl):
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
                        # ft.DataCell(ft.Text(item["material"]["name"])),
                        ft.DataCell(ft.Text(item["material_name"])),
                        ft.DataCell(ft.Text(item["material_thickness"])),
                        ft.DataCell(ft.Text(item["material_density"])),
                        ft.DataCell(ft.Text(item["neutron_dose_coefficient"])),
                        ft.DataCell(ft.Text(item["gamma_dose_coefficient"])),
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
        data_table = ft.DataTable(
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
                        "Матеріал",
                        max_lines=5,
                        overflow=ft.TextOverflow.ELLIPSIS,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ),
                ft.DataColumn(
                    ft.Text(
                        "Товщина \nшару матеріалу, \nсм",
                        max_lines=5,
                        overflow=ft.TextOverflow.CLIP,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ),
                ft.DataColumn(
                    ft.Container(
                        content=ft.Text(
                            "Щільність матеріалу, \nкг/м.куб.",
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
                            "Коефіцієнт послаблення \nдози \nгамма-випромінювання",
                            max_lines=5,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        expand=True,
                    )
                ),
                ft.DataColumn(
                    ft.Container(
                        content=ft.Text(
                            "Коефіцієнт послаблення \nдози \nнейтронів",
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
        )
        return ft.ListView(
            controls=[data_table],
            width=self.page.window_width,
            height=self.page.height - self.page.height * 0.1,
            auto_scroll=False,
        )
