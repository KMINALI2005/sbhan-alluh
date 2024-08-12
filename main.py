import flet as ft
from datetime import datetime, date

def main(page: ft.Page):
    page.title = "حاسبة العمر"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ("#F0F8FF")

    def calculate_age(e):
        try:
            birth_date = date(int(year.value), int(month.value), int(day.value))
            today = date.today()
            age = today - birth_date
            
            years = age.days // 365
            months = (age.days % 365) // 30
            days = (age.days % 365) % 30
            seconds = age.days * 24 * 60 * 60

            result.value = f"عمرك هو: {years} سنة, {months} شهر, {days} يوم"
            seconds_result.value = f"عمرك بالثواني: {seconds} ثانية"
            result.update()
            seconds_result.update()
        except ValueError:
            result.value = "الرجاء إدخال تاريخ صالح"
            seconds_result.value = ""
            result.update()
            seconds_result.update()

    title = ft.Text("حاسبة العمر", size=32, weight=ft.FontWeight.BOLD)

    year = ft.Dropdown(
        label="السنة",
        options=[ft.dropdown.Option(y) for y in range(1900, datetime.now().year + 1)],
        width=100
    )
    month = ft.Dropdown(
        label="الشهر",
        options=[ft.dropdown.Option(m) for m in range(1, 13)],
        width=100
    )
    day = ft.Dropdown(
        label="اليوم",
        options=[ft.dropdown.Option(d) for d in range(1, 32)],
        width=100
    )

    calculate_button = ft.ElevatedButton("احسب العمر", on_click=calculate_age)
    result = ft.Text("", size=20, color="#333333")
    seconds_result = ft.Text("", size=16)

    page.add(
        ft.Column(
            [
                title,
                ft.Row([year, month, day], alignment=ft.MainAxisAlignment.CENTER),
                calculate_button,
                result,
                seconds_result
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
