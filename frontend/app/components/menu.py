import flet as ft


class MenuBar(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

    def build(self):
        menubar = ft.MenuBar(
            expand=True,
            style=ft.MenuStyle(
                alignment=ft.alignment.top_left,
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                mouse_cursor={
                    ft.ControlState.HOVERED: ft.MouseCursor.WAIT,
                    ft.ControlState.DEFAULT: ft.MouseCursor.ZOOM_OUT,
                },
            ),
            controls=[
                ft.IconButton(
                    icon=ft.Icons.LOCAL_FIRE_DEPARTMENT,
                    tooltip="Домашня сторінка",
                    on_click=lambda _: self.page.go("/"),
                ),
                ft.SubmenuButton(
                    leading=ft.Icon(ft.Icons.MENU_BOOK),
                    content=ft.Text("Додатки"),
                    controls=[
                        ft.MenuItemButton(
                            content=ft.Text(
                                "А.1 - Клас сховищ, СПП із захисними властивостями сховищ"
                            ),
                            leading=ft.Icon(ft.Icons.BOOK),
                            style=ft.ButtonStyle(
                                bgcolor={ft.ControlState.HOVERED: ft.Colors.GREEN_100}
                            ),
                            on_click=lambda _: self.page.go("/storage-classes"),
                        ),
                        ft.MenuItemButton(
                            content=ft.Text(
                                "Г.1 - Коефіцієнт послаблення дози гамма-випромінювання та нейтронів проникаючої радіації товщею матеріалів"
                            ),
                            leading=ft.Icon(ft.Icons.BOOK),
                            style=ft.ButtonStyle(
                                bgcolor={ft.ControlState.HOVERED: ft.Colors.GREEN_100}
                            ),
                            on_click=lambda _: self.page.go(
                                "/attenuation-coefficients"
                            ),
                        ),
                        ft.MenuItemButton(
                            content=ft.Text(
                                "Г.2 - Коефіцієнт, який враховує зниження дози проникаючої радіації у забудові"
                            ),
                            leading=ft.Icon(ft.Icons.BOOK),
                            style=ft.ButtonStyle(
                                bgcolor={ft.ControlState.HOVERED: ft.Colors.GREEN_100}
                            ),
                            on_click=lambda _: self.page.go(
                                "/location-condition-coefficients"
                            ),
                        ),
                        ft.MenuItemButton(
                            content=ft.Text(
                                "Г.3 - Коефіцієнт, який враховує послаблення радіації огороджувальними конструкціями"
                            ),
                            leading=ft.Icon(ft.Icons.BOOK),
                            style=ft.ButtonStyle(
                                bgcolor={ft.ControlState.HOVERED: ft.Colors.GREEN_100}
                            ),
                            on_click=lambda _: self.page.go("/buildings-coefficients"),
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("Матеріали"),
                            leading=ft.Icon(ft.Icons.BOOK),
                            style=ft.ButtonStyle(
                                bgcolor={ft.ControlState.HOVERED: ft.Colors.GREEN_100}
                            ),
                            on_click=lambda _: self.page.go("/materials"),
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("Характер забудови"),
                            leading=ft.Icon(ft.Icons.BOOK),
                            style=ft.ButtonStyle(
                                bgcolor={ft.ControlState.HOVERED: ft.Colors.GREEN_100}
                            ),
                            on_click=lambda _: self.page.go("/building-types"),
                        ),
                        ft.MenuItemButton(
                            content=ft.Text("Матеріали стін"),
                            leading=ft.Icon(ft.Icons.BOOK),
                            style=ft.ButtonStyle(
                                bgcolor={ft.ControlState.HOVERED: ft.Colors.GREEN_100}
                            ),
                            on_click=lambda _: self.page.go("/wall-materials"),
                        ),
                    ],
                ),
            ],
        )
        return ft.Container(
            content=menubar,
            height=50,
            width=self.page.window_width,
        )
