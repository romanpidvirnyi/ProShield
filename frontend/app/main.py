import flet as ft
from app import components, services, views


def main(page: ft.Page):
    page.title = "Flet App Example"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = page.width

    # Add routes to handle navigation
    def route_change(route: str | ft.RouteChangeEvent):
        print("route_change")
        print(route)

        if isinstance(route, ft.RouteChangeEvent):
            route = route.route

        if route == "/":
            page.clean()
            page.add(views.HomeView(page))
        elif route == "/materials":
            page.clean()
            materials = services.get_materials()
            page.add(views.MaterialsView(page, materials))
        elif route == "/storage-classes":
            page.clean()
            starage_classes = services.get_starage_classes()
            page.add(views.StorageClassesView(page, starage_classes))
        elif route == "/attenuation-coefficients":
            page.clean()
            attenuation_coefficients = services.get_attenuation_coefficients()
            page.add(views.AttenuationCoefficientsView(page, attenuation_coefficients))
        elif route == "/building-types":
            page.clean()
            building_types = services.get_building_types()
            page.add(views.BuildingTypesView(page, building_types))
        elif route == "/location-condition-coefficients":
            page.clean()
            location_condition_coefficients = (
                services.get_location_condition_coefficients()
            )
            page.add(
                views.LocationConditionCoeficientView(
                    page, location_condition_coefficients
                )
            )
        elif route == "/wall-materials":
            page.clean()
            wall_materials = services.get_wall_materials()
            page.add(views.WallMaterialsView(page, wall_materials))
        elif route == "/buildings-coefficients":
            page.clean()
            buildings_coefficients = services.get_buildings_coefficients()
            page.add(views.BuildingCoeficientsView(page, buildings_coefficients))

    # Set up routing
    page.on_route_change = route_change

    route_change(page.route)


if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
