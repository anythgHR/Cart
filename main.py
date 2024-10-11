from flet import *
import sqlite3

# إعداد قاعدة البيانات
conn = sqlite3.connect("items.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute(""" 
CREATE TABLE IF NOT EXISTS items (
    name TEXT PRIMARY KEY,
    checked BOOLEAN
)""")
conn.commit()

mark_down = """\
## [انقر هنا](https://www.mediafire.com/folder/mrhqqtxvepcwa/Cart+List) لتحميل برنامجنا من  MediaFire حصراً على الاندرويد (مجاناً)

"""

theme = "Light"

def main(page: Page):

    
    def route_change(route):

        if page.route == "/about":
            page.views.append(
                View(
                    "/about",
                    [
                        AppBar(
                            title=Text("فكرة التطبيق", size=30, color=colors.BLACK),
                            center_title=True,
                            bgcolor=colors.PINK_400,
                            actions=[
                                IconButton(icons.INFO)
                            ]
                            
                        ),
                        Column([
                        Text("مرحبا بكم في تطبيق قائمة التسوق!",size=26,color=colors.BLUE_800),
                        Text("هذا التطبيق يتيح لك إضافة عناصر إلى قائمة التسوق وإرسالها عبر WhatsApp للشخص الذي تحدد رقمه في خانه الرقم",size=20,color=colors.BLUE_800),
                        ],alignment=MainAxisAlignment.CENTER,rtl=True)
                        
                    ],
                )
            )    
        
        elif page.route == "/How_to_use":
            page.views.append(
                View(
                    "/How_to_use",
                    [
                        AppBar(
                            title=Text("طريقة الاستعمال", size=30, color=colors.BLACK),
                            center_title=True,
                            bgcolor=colors.PINK_400,
                            actions=[
                                IconButton(icons.INFO_OUTLINE)
                            ]
                            
                        ),
                        Column([
                        Text("يتألف البرنامج من اربع اشياء: \nحقلين لادخال المعلومات \n و زرين\nاول حقل وضع المنتج و هو المكان الذي تضع فيه الاغراض التي تريد شرائها (كل غرض بغرضه) و بعد وضع الغرض الذي تحتاجه تكبس على زر وضع المنتج بعدما تضع كل المنتجات الي تريدها(كل غرض بغرضه) ان كنت تريد ارسال بعض الاغراض الى شخص معين تضع رقمه في خانه ادخال رقم الهاتف و تضع علامة الصح على الاغراض التي تريد ارسالها .\nان احضرت منتج معين يمكنك الضغط على سلة المهملات كما يمكنك ايضا الضغط عليها ان لم تعد تريد المنتج",size=20,color=colors.BLUE_800),
                        ],alignment=MainAxisAlignment.CENTER,rtl=True)
                        
                    ],
                )
            )
        elif page.route == "/credits":
            page.views.append(
                View(
                    "/credits",
                    [
                        AppBar(
                            title=Text("الحقوق ", size=30, color=colors.BLACK),
                            center_title=True,
                            bgcolor=colors.PINK_400,
                            actions=[
                                IconButton(icons.INFO)
                            ]
                            
                        ),

                        Column([
                        Markdown(mark_down,
                                 on_tap_link=lambda e :page.launch_url(e.data)),
                        Text("\n\n\nكل الحقوق تعود الى  ZOY_Production ©",size=16,color=colors.BLUE_800),
                        ],alignment=MainAxisAlignment.CENTER,rtl=True,horizontal_alignment=CrossAxisAlignment.CENTER),
                        
                        
                    ],
                )
            )    

        page.update()
    page.scroll = 'auto'
    page.window.top = 10
    page.window.left = 960
    page.window.width = 390
    page.window.height = 740
    page.theme_mode = ThemeMode.LIGHT
    page.bgcolor = colors.GREEN_300
    shopping_list = Column()

    def change_color(e):
        global theme
        if theme == "Dark":
            page.theme_mode = ThemeMode.LIGHT
            theme = "Light"
            page.update()
        else:
            page.theme_mode = ThemeMode.DARK
            theme = "Dark"
            page.update()


    page.appbar = AppBar(
        title=Text("قائمة التسوق", size=30, color=colors.BLACK),
        bgcolor=colors.AMBER,
        center_title=True,
        leading=Icon(icons.HOME),
        actions=[
            IconButton(icons.WB_SUNNY_OUTLINED,on_click=lambda e :change_color(e)),
            PopupMenuButton(
                items=[
                    PopupMenuItem(text="فكرة التطبيق", on_click=lambda e: page.go("/about")),
                    PopupMenuItem(text="طريقة استعمال التطبيق", on_click=lambda e: page.go("/How_to_use")),
                    PopupMenuItem(text="حول", on_click=lambda e: page.go("/credits")),
                    PopupMenuItem(text=""),
                    PopupMenuItem(text="الخروج", on_click=lambda e: page.window_close()),
                ]
            )
        ]
    )


    item_name_send =""
    item_row_send = ""
    message_send = ""
    check_send = ""

    def load_items():
        cursor.execute('SELECT name, checked FROM items')
        items = cursor.fetchall()
        for item_name_load, check_load in items:
            # تحويل القيمة من 0/1 إلى True/False
            is_checked = bool(check_load)
            # if is_checked == False:
            add_item_to_list(item_name_load, is_checked)
    
    def check(item_name_check,checked_check):
        cursor.execute("UPDATE items SET checked=? WHERE name=?", (checked_check, item_name_check))
        conn.commit()

    def add_item_to_list(item_name_add_list, checked_add_list):
        global item_name_send,item_row_send,message_send,check_send
        checkbox = Checkbox(label=item_name_add_list, value=checked_add_list, on_change=lambda e: check(item_name_add_list, checkbox.value))
        item_row = Row(
            controls=[
                checkbox,
                IconButton(
                    icon=icons.DELETE,
                    on_click=lambda e: delete_item(item_row, item_name_add_list)
                )
            ],
            alignment=MainAxisAlignment.CENTER, rtl=True
        )
        # print(f"ro {item_row}")
        item_name_send = item_name_add_list
        item_row_send = item_row
        message_send = item_name_add_list
        check_send = checked_add_list
        x = item_name_add_list
        print(x)

        shopping_list.controls.append(item_row)
        page.update()

    def add(e):
        item = item_add.value
        if item:
            add_item_to_list(item, False)
            item_add.value = ""
            cursor.execute('INSERT OR REPLACE INTO items (name, checked) VALUES (?, ?)', (item, False))
            conn.commit()
            page.update()
   
    def send_message(e):
        global item_name_send , item_row_send, message_send,check_send
        phone_number_s = phone_number.value
        cursor.execute('SELECT name FROM items WHERE checked = 1')
        checked_items = cursor.fetchall()


        if checked_items and phone_number_s:
            print(phone_number_s)
            item_names = ', '.join(item[0] for item in checked_items)
            message = item_names      # Replace with your message
            whatsapp_url = f"https://wa.me/{phone_number_s}?text={message.replace(' ', '%20')}"
            page.launch_url(whatsapp_url)

            for item in checked_items:
                item_name = item[0]
                cursor.execute('DELETE FROM items WHERE name = ?', [item_name])
            conn.commit()

            shopping_list.controls.clear()  # مسح قائمة التسوق
            load_items()  # إعادة تحميل العناصر لتظهر الحالة الحالية
            page.update()

    def delete_item(item_row_delete, item_name_delete):
        shopping_list.controls.remove(item_row_delete)
        page.update()
        cursor.execute('DELETE FROM items WHERE name = ?', [item_name_delete,])
        conn.commit()

    item_add = TextField(label="وضع منتج", icon=icons.SHOPPING_CART, rtl=True)
    add_item = ElevatedButton("وضع المنتج", icon=icons.ADD_SHOPPING_CART_OUTLINED, width=400, on_click=add,bgcolor=colors.GREY_300,color=colors.BLACK)
    phone_number = TextField(label="ادخل رقم هاتف",icon=icons.PHONE,width=170)
    send_item = ElevatedButton(" ارسال المنتج", icon=icons.SEND, width=160, on_click=send_message,bgcolor=colors.GREY_300,color=colors.BLACK)

    Credits = Text("By_Zoy_Productions",size=18)
    page.add(
        Column(
            controls=[
                Credits,
                item_add,
                add_item,
                shopping_list,
                
                
            ],alignment=MainAxisAlignment.CENTER,horizontal_alignment=CrossAxisAlignment.CENTER
        ),
        Row([
                phone_number,
                send_item
        ],alignment=MainAxisAlignment.CENTER),
        
    )

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

    page.update()

    
app(main)

