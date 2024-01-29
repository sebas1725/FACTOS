import sqlite3
import flet as ft

def obtener_todos_los_productos():
    conn = sqlite3.connect("inve.db")
    cursor = conn.cursor()

    cursor.execute("SELECT codigo, nombre, precio_unidad, iva FROM inventario")
    productos = cursor.fetchall()

    conn.close()
    return productos

def obtener_datos_producto_por_codigo(codigo):
    conn = sqlite3.connect("inve.db")
    cursor = conn.cursor()

    cursor.execute("SELECT nombre, precio_unidad, iva FROM inventario WHERE codigo=?", (codigo,))
    producto = cursor.fetchone()

    conn.close()
    return producto



#!Crear la tabla
Data_table=ft.DataTable(
    width=1100,
    columns=[
        ft.DataColumn(ft.Text("ID"),),
        ft.DataColumn(ft.Text("Nombre")),
        ft.DataColumn(ft.Text("Precio Unidad")),
        ft.DataColumn(ft.Text("IVA")),
    ],
    rows=[
        
    ]
        
    )
    #!Agregar los productos a la tabla de la base de datos
max_productos = 0
productos_disponibles = obtener_todos_los_productos()
for producto in productos_disponibles:
    max_productos= max_productos +1
    codigo, nombre, precio_unidad, iva = producto
    #print(f"Código: {codigo}, Nombre: {nombre}, Precio: {precio_unidad}, IVA: {iva}%")
    Data_table.rows.append(ft.DataRow(
        cells=[
            ft.DataCell(ft.Text(codigo)),
            ft.DataCell(ft.Text(nombre)),
            ft.DataCell(ft.Text(precio_unidad)),
            ft.DataCell(ft.Text(iva)),
                
            ],
        ),)
    


class Task(ft.UserControl):
    
    def __init__(self, task_name, task_delete):
        super().__init__()
        self.task_name = task_name
        self.task_delete = task_delete

    def build(self):

        
        self.display_task = ft.Text(self.task_name)
        producto = obtener_datos_producto_por_codigo(self.display_task.value)
        nombre, precio, iva = producto   
        print(f"Nombre: {nombre}, Precio: {precio}, IVA: {iva}%")    
        print(self.display_task.value)
            
                

        self.display_view = ft.Row(
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.display_task,ft.Container(content=ft.Text(nombre), margin=1,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.GREEN,
                    width=80,
                    height=25,
                    border_radius=5,
                    ),
                ft.Container(content=ft.Text(precio), margin=1,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.GREEN,
                    width=55,
                    height=25,
                    border_radius=5,
                    ),
                ft.Container(content=ft.Text(iva), margin=1,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.GREEN,
                    width=35,
                    height=25,
                    border_radius=5,
                    ),
                ft.Row(
                    spacing=0,
                    controls=[
                        
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip="Eliminar",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        
        return ft.Column(controls=[self.display_view])
        self.update()

    def delete_clicked(self, e):
        self.task_delete(self)


class TodoApp(ft.UserControl):
    def build(self):
        

        self.new_task = ft.TextField(hint_text="Escriba el id del producto", expand=True)

        
        self.tasks = ft.Column()
        
        # application's root control (i.e. "view") containing all other controls
        return ft.Column(
            width=300,
            controls=[
                ft.Row(
                    controls=[
                        self.new_task,
                        ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked),
                    ],
                ),
                self.tasks,
            ],
        )

    def add_clicked(self, e):
        print(f"{self.new_task.value} {max_productos}")
        if int(self.new_task.value) <= 0 or int(self.new_task.value) > max_productos:
            self.new_task.error_text = "No se encuentra en la base de datos"
            self.update()
        else:
            task = Task(self.new_task.value, self.task_delete)
            self.tasks.controls.append(task)
            self.new_task.error_text = ""
            self.update()
            

        

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()
def check_item_clicked(e):
    e.control.checked = not e.control.checked



def main(page: ft.Page):
    
    
     #!Campos a llenar 
    
    Nombre_Usuario=ft.TextField(label="Nombre de Usuario",width=280,height=45)
    Apeliido_Usuaio=ft.TextField(label="Apellido de Usuario",width=280,height=45)
    Numero_de_celular=ft.TextField(label="Numero de celular",width=570,height=65,max_length=10)
    Cedula=ft.TextField(label="Cedula",width=570,height=65,max_length=10)
    Mail=ft.TextField(label="Correo electronico",width=570,height=45)
    Direccion=ft.TextField(label="Direccion",width=570,height=45)
    
    greetings = ft.Column()
    #!Campos del login
    
    Login_Mail=ft.TextField(label="Usuario",width=380,height=50)
    Registrar = ft.Column()
    Login_Pasword=ft.TextField(label="Password",width=380,height=50,password=True,can_reveal_password=True)
    
    #!Campo para el Forget password
    Olvido_Contraseña=ft.TextField(label="Correo Electronico",width=500,height=80)

    

    #!Verificacion de campos para agregar datos del cliente
    def send_fac_data(a):
        if not Nombre_Usuario.value:
            Nombre_Usuario.error_text = "Please enter your name"
            page.update()
        else:
            page.update()

    
            
    def theme(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode=ft.ThemeMode.LIGHT
        else:
            page.theme_mode=ft.ThemeMode.DARK
        page.update()

    
    Usuario=ft.Card(
        width=1280,
        height=525,
        content=ft.Container(

            border_radius=6,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            #ft.Divider(height=10),
                        ]
                    ),
                    ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                        controls=[
                    
                            ft.ElevatedButton(
                                "Pick files",
                                icon=ft.icons.UPLOAD_FILE,
                            )
                        ],
                    ),
                ],
            ),
        ),
    ) 
    
    rail = ft.NavigationRail(

        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        # extended=True,
        min_width=100,
        min_extended_width=400,
        
        
        leading=ft.FloatingActionButton(icon=ft.icons.CREATE, text="Add"),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.HOME_OUTLINED, selected_icon=ft.icons.HOME, label="Menu principal"
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.SETTINGS_OUTLINED),
                selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                label="Clientes",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.INVENTORY_2_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.INVENTORY_2),
                label_content=ft.Text("Inventario"),
            ),
        ],
        on_change=lambda e: change_index(e.control.selected_index),
    )

    page_one_ui = ft.Row(
                            [
                                rail,
                                
                                ft.VerticalDivider(width=1),
                                
                                ft.Column(
                                    [
                                        
                                        ft.Text("Datos de Usuario",size=40),
                                        ft.Row(controls=[Nombre_Usuario,Apeliido_Usuaio]),
                                        Mail,Direccion,Cedula,Numero_de_celular,ft.ElevatedButton("Enviar datos", on_click=send_fac_data),
                                        
                                    ],#
                                        ),
                                ft.VerticalDivider(width=1),
                                ft.Column(
                                    [
                                        
                                        ft.Text("Agrega productos!"),TodoApp(),
                                        
                                    ],scroll=ft.ScrollMode.ADAPTIVE, alignment=ft.MainAxisAlignment.START , height=600, width=500
                                        ),
                                
                            ],
                            expand=True,height=800 ,alignment=ft.MainAxisAlignment.START
                        )
                    
    
    page_two_ui = ft.Row(
        
                [
                    rail,
                                
                    ft.VerticalDivider(width=1),
                    Usuario
                ],
                    expand=True,height=800
                        )

    

    page_three_ui = ft.Row(
        [
                    rail,
                    ft.Column([Data_table],scroll=ft.ScrollMode.ADAPTIVE,height=680),
                                
                    ft.VerticalDivider(width=1),
                    
                    
                ],
                    expand=True,height=800,alignment=ft.MainAxisAlignment.START,
    )


    #!Tema y Titulo de la pagina
    page.theme_mode = ft.ThemeMode.DARK
   

    content = ft.Row([page_one_ui],vertical_alignment=ft.MainAxisAlignment.START)
    def change_index(e):
        index = e
        

        if index == 0:
            print(str(index))
            content.controls.pop()
            rail.selected_index = 0
            content.controls.append(page_one_ui)
            page.update()

        if index == 1:
            print(str(index))
            content.controls.pop()
            rail.selected_index = 1
            content.controls.append(page_two_ui)
            page.update()
            
        if index == 2:
            print(str(index))
            content.controls.pop()
            rail.selected_index = 2
            content.controls.append(page_three_ui)


            page.update()
        
        page.update()


    

    def on_keyboard(e: ft.KeyboardEvent):
        
        print(
                    f"Key: {e.key}, Control: {e.ctrl}"
                )
        if e.ctrl == True and e.key == "1":
            
            change_index(0)
            
            

        if e.ctrl == True and e.key == "2":
            
            change_index(1)
            

        if e.ctrl == True and e.key == "3":
            
            change_index(2)
            
        
        page.update()
    page.on_keyboard_event = on_keyboard


    #!Funcion para cerrar el programa
    def Close(end):
        page.window_destroy()
        page.update()

    #! Funcion para Cambiar tema
    


    def Sing(a):
        Registrar.controls.append(ft.Column([ft.TextField(label="E-Mail",width=380,height=45)]))
        page.update()

    Login_Card=ft.Card(           
        width=408,
        height=612,
        elevation=15,

        content=ft.Container(

            border_radius=6,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Divider(height=20, color="transparent"),
                    ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                        controls=[
                            ft.Image(
                                src=f"banner.png",
                                width=500,
                                height=180,
                                fit=ft.ImageFit.CONTAIN,
                            ),
                            ft.Text("Sign In Facturador", size=22, weight="bold"),
                            ft.Text(
                                "Concento de Facturador",
                                size=13,
                                weight="bold",
                            ),

                            ft.Divider(height=25, color="transparent"),
                            Login_Mail,
                            ft.Divider(height=1, color="transparent"),
                            Registrar,
                            ft.Divider(height=1, color="transparent"),
                            Login_Pasword,
                            ft.Divider(height=1, color="transparent"),
                        ],
                    ),
                    ft.Row(
                        width=320,
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.TextButton(
                                content=ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text(value="Olvido la CotraseÃ±a?", size=10),
                                        ],
                                    )
                                ),
                                on_click=lambda _: page.go("/Forgot_Password")    
                            )
                        ],
                    ),
                    ft.Divider(height=3, color="transparent"),
                    ft.ElevatedButton("Entrar", on_click=lambda _: page.go("/Home"),width=120,height=40),
                    #ft.Divider(height=35, color="transparent"),
                    ft.ElevatedButton("Sing-in", on_click=Sing,width=120,height=40),
                ],
            ),
        ),
    )
    #!Card del forgot password
    Forgot_password=ft.Card(
        width=600,
        height=400,
        content=ft.Container(

            border_radius=6,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            ft.TextButton(
                                "Volver a Login", icon="ARROW_BACK",
                                on_click=lambda _: page.go("/")    
                                
                            ),
                            ft.Divider(height=10),
                        ]
                    ),
                    ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                        controls=[
                            ft.Text("Recupera tu cuenta",size=45),
                            ft.Divider(height=20,color="transparent"),
                            ft.Text("Introduce tu correo electrónico",size=20),
                            ft.Divider(height=25,color="transparent"),
                            Olvido_Contraseña,ft.Divider(height=9,color="transparent"),
                            ft.ElevatedButton("Buscar Cuenta",width=150,height=50),
                            
                        ],
                    ),
                ],
            ),
        ),
    )
    page.appbar = ft.AppBar(         
        leading_width=40,
        title=ft.Text("FACTURADOR"),
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(
                ft.icons.WB_SUNNY_OUTLINED,
                selected_icon=ft.icons.BOOKMARK,
                tooltip=("Modo Oscuro"),
                on_click=theme,
            ),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        text=("Cerrar sesión"),
                        icon=ft.icons.MANAGE_ACCOUNTS,
                        on_click=lambda _: page.go("/"),
                    ),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        icon=ft.icons.EXIT_TO_APP,
                        text=("Salir"),
                        on_click=Close,
                    ),
                ]
            ),
        ],
    )

    #!Card del Usuario
    
    
    
            



    def route_change(e):
        page.window_maximized = True
        #page.horizontal_alignment = "center",
        page.vertical_alignment = "START" , 
        
        page.views.clear()
        if page.route == "/":
            page.views.append(
            #!Login
            ft.View(
                "/",
                [   
                    ft.Row(
                        [
                            Login_Card,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                ]
            )
            )
        #!Home
        elif page.route == "/Home":
            
            
            page.views.append(
                ft.View(
                    "/Home",
                    [
                        
                        page.appbar,
                        
                        ft.Column(
                            [
                                content,
                        
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                    ],vertical_alignment=ft.MainAxisAlignment.START,#scroll=ft.ScrollMode.ADAPTIVE
                    
                    
                )
                
            )
        elif page.route=="/Forgot_Password":
            page.views.append(
            #!Login
            ft.View(
                "/Forgot_Password",
                [   
                    ft.Row(
                        [   
                            ft.Column(
                                [
                                    ft.Divider(height=120),
                                    Forgot_password,
                                ],
                                alignment=(ft.MainAxisAlignment.CENTER)
                            )
                        ],
                        alignment=(ft.MainAxisAlignment.CENTER)
                    )
                ]
            )
            )
    page.on_route_change = route_change
    page.go(page.route)
    page.update

ft.app(target=main)