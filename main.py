import flet as ft
import math

def main(page: ft.Page):
    page.title = "آلة حاسبة متقدمة"
    page.window_width = 300
    page.window_height = 500
    page.window_resizable = False
    page.theme_mode = "dark"

    result = ft.TextField(value="0", text_align="right", width=280, read_only=True)
    
    def button_clicked(e):
        data = e.control.data
        if data == "C":
            result.value = "0"
        elif data == "=":
            try:
                result.value = str(eval(result.value))
            except:
                result.value = "خطأ"
        elif data == "√":
            try:
                result.value = str(math.sqrt(float(result.value)))
            except:
                result.value = "خطأ"
        elif data == "^2":
            try:
                result.value = str(math.pow(float(result.value), 2))
            except:
                result.value = "خطأ"
        else:
            if result.value == "0":
                result.value = data
            else:
                result.value += data
        page.update()

    buttons = [
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["0", ".", "C", "+"],
        ["√", "^2", "="]
    ]

    def create_button(label):
        return ft.ElevatedButton(
            text=label,
            data=label,
            width=65,
            height=65,
            on_click=button_clicked,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
            )
        )

    button_rows = []
    for row in buttons:
        button_row = ft.Row(
            controls=[create_button(button) for button in row],
            alignment=ft.MainAxisAlignment.CENTER
        )
        button_rows.append(button_row)

    page.add(
        ft.Container(
            content=ft.Column(
                controls=[result] + button_rows,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            margin=10
        )
    )

ft.app(target=main)
