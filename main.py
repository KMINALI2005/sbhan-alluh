import flet as ft
import cv2
import numpy as np
from PIL import Image
import io

def main(page: ft.Page):
    page.title = "تحليل صور الأشعة السينية"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 50
    page.bgcolor = ft.colors.BLUE_GREY_900

    def analyze_xray(image):
        # تحويل الصورة إلى تدرجات الرمادي
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # تطبيق فلتر جاوس لتنعيم الصورة
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # استخدام طريقة Canny للكشف عن الحواف
        edges = cv2.Canny(blurred, 50, 150)
        
        # البحث عن الكونتورات في الصورة
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # رسم الكونتورات على الصورة الأصلية
        cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
        
        return image, len(contours)

    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            upload_button.disabled = True
            progress_ring.visible = True
            page.update()

            file_content = io.BytesIO(e.files[0].read())
            image = cv2.imdecode(np.frombuffer(file_content.read(), np.uint8), 1)
            
            analyzed_image, num_anomalies = analyze_xray(image)
            
            # تحويل الصورة المحللة إلى صيغة يمكن عرضها في Flet
            is_success, buffer = cv2.imencode(".png", analyzed_image)
            io_buf = io.BytesIO(buffer)
            
            result_image.src_base64 = Image.open(io_buf).tobytes()
            result_image.visible = True
            result_text.value = f"تم العثور على {num_anomalies} منطقة مشبوهة في الصورة."
            result_text.visible = True
            
            upload_button.disabled = False
            progress_ring.visible = False
            page.update()

    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    upload_button = ft.ElevatedButton(
        "اختر صورة الأشعة السينية",
        icon=ft.icons.UPLOAD_FILE,
        on_click=lambda _: file_picker.pick_files(allow_multiple=False),
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLUE_600,
            padding=20,
        )
    )

    progress_ring = ft.ProgressRing(visible=False)

    result_image = ft.Image(
        visible=False,
        fit=ft.ImageFit.CONTAIN,
        width=400,
        height=400,
    )

    result_text = ft.Text(
        visible=False,
        size=18,
        color=ft.colors.GREEN_400,
        weight=ft.FontWeight.BOLD,
    )

    page.add(
        ft.Column(
            [
                ft.Text("تحليل صور الأشعة السينية", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_200),
                ft.Text("قم برفع صورة الأشعة السينية لتحليلها وكشف المناطق المشبوهة.", size=16, color=ft.colors.GREY_400),
                ft.Row([upload_button, progress_ring], alignment=ft.MainAxisAlignment.CENTER),
                result_image,
                result_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
    )

ft.app(target=main)
