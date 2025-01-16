import flet as ft


def main(page: ft.Page):
    # Create a DataTable with larger headers and scrolling
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(
                label=ft.Container(
                    content=ft.Text(
                        "First Column\n(Long Title)",
                        size=16,  # Font size for the header
                        weight="bold",  # Bold text
                        text_align="center",  # Center-align text
                    ),
                    height=50,  # Set the header height
                    padding=ft.Padding(5, 5, 5, 5),  # Add padding
                    alignment=ft.alignment.center,  # Center-align content
                )
            ),
            ft.DataColumn(
                label=ft.Container(
                    content=ft.Text(
                        "Second Column\n(Longer Title)",
                        size=16,
                        weight="bold",
                        text_align="center",
                    ),
                    height=50,
                    padding=ft.Padding(5, 5, 5, 5),
                    alignment=ft.alignment.center,
                )
            ),
            ft.DataColumn(
                label=ft.Container(
                    content=ft.Text(
                        "Third Column\n(Yet Another Long Title)",
                        size=16,
                        weight="bold",
                        text_align="center",
                    ),
                    height=50,
                    padding=ft.Padding(5, 5, 5, 5),
                    alignment=ft.alignment.center,
                )
            ),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(f"Row {i}, Col 1")),
                    ft.DataCell(ft.Text(f"Row {i}, Col 2")),
                    ft.DataCell(ft.Text(f"Row {i}, Col 3")),
                ]
            )
            for i in range(1, 51)  # Generate 50 rows for demonstration
        ],
    )

    # Use ListView to enable scrolling
    scrollable_table = ft.ListView(
        controls=[data_table],
        height=400,  # Set the height of the scrollable area
        auto_scroll=False,  # Disable auto-scroll to top/bottom
    )

    # Add the scrollable table to the page
    page.add(
        ft.Column([ft.Text("Data Table Example with Scrolling"), scrollable_table])
    )


# Run the app
ft.app(target=main, view=ft.AppView.WEB_BROWSER)
