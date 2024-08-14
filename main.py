import flet as ft
from flet import (
    Page,
    Text,
    TextField,
    ElevatedButton,
    Column,
    Row,
    DataTable,
    DataColumn,
    DataRow,
    DataCell,
    ProgressRing,
)
import requests
from collections import Counter
import re
import asyncio

NAME = []

def main(page: Page):
    page.title = "تطبيق البحث عن معلومات الأرقام"
    page.theme_mode = "dark"
    page.rtl = True  # تفعيل الاتجاه من اليمين إلى اليسار للغة العربية

    # العناصر الرئيسية للواجهة
    title = Text("تطبيق البحث عن معلومات الأرقام", size=24, weight="bold")
    author = Text("تم التصميم بواسطة: kmein iraqi", size=16, italic=True)
    number_input = TextField(label="أدخل رقم الهاتف", hint_text="مثال: 964 5055555555")
    search_button = ElevatedButton("بحث", on_click=lambda _: search_number(number_input.value))
    progress_ring = ProgressRing(visible=False)
    result_text = Text()
    result_table = DataTable(
        columns=[
            DataColumn(Text("الرقم")),
            DataColumn(Text("الاسم")),
        ],
        rows=[],
    )

    # دالة البحث
    async def search_number(number):
        global NAME
        NAME = []
        result_table.rows.clear()
        result_text.value = ""
        progress_ring.visible = True
        search_button.disabled = True
        page.update()
        
        if '+' in number:
            number = number.replace('+', '')
        
        try:
            code, num = number.split(' ')
        except ValueError:
            result_text.value = "خطأ: رقم غير صالح. المثال الصحيح: 964 5055555555"
            progress_ring.visible = False
            search_button.disabled = False
            page.update()
            return

        # تنفيذ عمليات البحث
        await asyncio.gather(
            Search_1(num, code),
            Search_2(code, num, code),
            Search_3(code, num, code),
            Search_4(code, num, code)
        )

        # عرض النتائج
        if len(NAME) == 0:
            result_text.value = f"لم يتم العثور على معلومات للرقم [ +{code}{num} ]"
        else:
            result_text.value = f"معلومات الرقم [ +{code}{num} ]"
            for id, name in enumerate(NAME, 1):
                result_table.rows.append(
                    DataRow(cells=[
                        DataCell(Text(str(id))),
                        DataCell(Text(name)),
                    ])
                )
            
            # إضافة معلومات إضافية
            most_common = Counter(str(NAME).replace("'", '').replace(',', '').split()).most_common(4)
            additional_info = "\n\nالأسماء الأكثر شيوعًا في القائمة هي:\n"
            for name, count in most_common:
                additional_info += f"- {name}: تكرر {count} مرات\n"
            result_text.value += additional_info

        progress_ring.visible = False
        search_button.disabled = False
        page.update()

    # دوال البحث
    async def Search_1(number, code):
        country = None
        country_codes = {
            '20': 'EG', '98': 'IR', '212': 'MA', '213': 'DZ', '216': 'TN',
            '249': 'SD', '252': 'SO', '961': 'LB', '962': 'JO', '963': 'SY',
            '964': 'IQ', '965': 'KW', '966': 'SA', '967': 'YE', '968': 'OM',
            '970': 'PS', '971': 'AE', '972': 'ISR', '973': 'BH', '974': 'QA'
        }
        
        country = country_codes.get(code)
        if country is None:
            return
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; RMX1821) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4660.11 Mobile Safari/537.36'
        }
        
        try:
            r = await asyncio.to_thread(
                requests.get,
                f'http://caller-id.saedhamdan.com/index.php/UserManagement/search_number?number={number}&country_code={country}',
                headers=headers
            )
            r.raise_for_status()
            data = r.json()
            
            if 'result' in data and data['result']:
                name = data['result'][0]['name']
                if name:
                    NAME.append(name)
        except Exception as e:
            print(f"Search_1 Error: {e}")

    async def Search_2(country, number, code):
        try:
            rq = await asyncio.to_thread(
                requests.get,
                f'http://146.148.112.105/caller/index.php/UserManagement/search_number?number={number}&country_code={country}'
            )
            rq.raise_for_status()
            data = rq.json()
            
            if 'result' in data and data['result']:
                for item in data['result']:
                    NAME.append(item['name'])
        except Exception as e:
            print(f"Search_2 Error: {e}")

    async def Search_3(country, number, code):
        headers = {
            'Authorization': 'Basic YWEyNTAyOnp1enVBaGgy',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G977N Build/LMY49I)',
            'Host': 'devappteamcall.site',
            'Connection': 'close',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        try:
            r = await asyncio.to_thread(
                requests.post,
                f'https://devappteamcall.site/data/search_name?country={country}&phoneNumber={number}',
                headers=headers
            )
            r.raise_for_status()
            data = r.json()
            
            if 'errorDesc' not in data or data['errorDesc'] != 'no data found':
                for name in re.findall('"Name":"(.*?)"', str(data)):
                    NAME.append(name)
        except Exception as e:
            print(f"Search_3 Error: {e}")

    async def Search_4(country, number, code):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            'User-Agent': 'نمبربوك الخليج 1/3.3 CFNetwork/1240.0.4 Darwin/20.5.0'.encode('UTF-8'),
            'Accept-Encoding': 'gzip, deflate',
            'Host': '86.48.0.204:919',
            'Accept': '*/*',
            'Accept-Language': 'ar',
            'Authorization': 'Basic aW9zYWRtaW46cGFzc3BvcmQ=',
            'token': 'pcfgv64567ko1',
        }
        
        try:
            r = await asyncio.to_thread(
                requests.post,
                'http://86.48.0.204:919/main',
                data={'number': str(code + number)},
                headers=headers
            )
            r.raise_for_status()
            data = r.json()
            
            if 'name' in data:
                NAME.append(data['name'])
        except Exception as e:
            print(f"Search_4 Error: {e}")

    # إضافة العناصر إلى الصفحة
    page.add(
        Column([
            title,
            author,
            Row([number_input, search_button, progress_ring]),
            result_text,
            result_table,
        ])
    )

    # تعيين وظيفة البحث كدالة غير متزامنة
    search_button.on_click = lambda _: page.launch_async(search_number(number_input.value))

ft.app(target=main)
