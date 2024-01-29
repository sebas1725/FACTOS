import sqlite3
import flet as ft
import datetime


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
    
class Counter(ft.UserControl):
    def __init__(self, initial_count):
        super().__init__()
        self.counter = initial_count

    def build(self):
        text = ft.Text(str(f"{self.counter}%"))
        def add_click(e):
            self.counter += 1
            text.value = str(f"{self.counter}%")
            self.update()
        def del_click(e):
            self.counter -= 1
            text.value = str(f"{self.counter}%")
            self.update()

        return ft.Row([ft.Text("Modifique el porcentaje de IVA"),ft.IconButton(icon=ft.icons.REMOVE, on_click=del_click),text,ft.IconButton(icon=ft.icons.ADD, on_click=add_click),])


class Task(ft.UserControl):
    
    def __init__(self, task_name, task_delete):
        super().__init__()
        self.task_name = task_name
        self.task_delete = task_delete

    def build(self):

        
        self.display_task = ft.Text(self.task_name, scale=1.5)
        producto = obtener_datos_producto_por_codigo(self.display_task.value)
        nombre, precio, iva = producto   
        print(f"Nombre: {nombre}, Precio: {precio}, IVA: {iva}%")    
        print(self.display_task.value)
            
                

        self.display_view = ft.Row(
            alignment=ft.alignment.top_center,
            vertical_alignment=ft.MainAxisAlignment.START,
            controls=[
                #self.display_task,
                ft.Container(content=ft.Text(nombre, color=ft.colors.WHITE), margin=1,
                    alignment=ft.alignment.center,
                    bgcolor="#16807E",
                    width=180,
                    height=25,
                    border_radius=5,
                    ),
                ft.Container(content=ft.Text(precio,color=ft.colors.WHITE,text_align=ft.alignment.center), margin=1,
                    alignment=ft.alignment.center,
                    bgcolor="#16807E",
                    width=70,
                    height=25,
                    border_radius=5,
                    ),
                ft.Container(content=ft.Text(iva,color=ft.colors.WHITE), margin=1,
                    alignment=ft.alignment.center,
                    bgcolor="#16807E",
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
        

        self.new_task = ft.TextField(hint_text="Escriba el id del producto",width=40 ,expand=True)

        
        self.tasks = ft.Column()

        delete_all_button = ft.FloatingActionButton("Eliminar Todos los productos", on_click=self.delete_all_clicked, width=250)
        
        # application's root control (i.e. "view") containing all other controls
        return ft.Column(
            width=360,
            controls=[
                ft.Row(
                    controls=[
                        self.new_task,
                        ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked),
                    ],
                ),
                self.tasks,
                delete_all_button, 
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

    def delete_all_clicked(self, e):
        self.tasks.controls = []  # Eliminar todas las tareas
        self.update()

def check_item_clicked(e):
    e.control.checked = not e.control.checked



def main(page: ft.Page):
    

    def on_dialog_result(e: ft.FilePickerResultEvent):
        print("Selected files:", e.files)
        print("Selected file or directory:", e.path)

    file_picker = ft.FilePicker(on_result=on_dialog_result)
    #!Tema y Titulo de la pagina
    page.theme_mode = ft.ThemeMode.DARK

    page.window_maximized = True

    page.theme = ft.Theme(color_scheme_seed="Teal",use_material3=True)
    #page.theme = ft.ColorScheme(primary=ft.colors.TEAL, on_primary=ft.colors.TEAL)

    #! Elegir fecha
    def change_date(e):
        print(f"Date picker changed, value is {date_picker.value}")
        page.update

    def date_picker_dismissed(e):
        print(f"Date picker dismissed, value is {date_picker.value}")
        page.update

    date_picker = ft.DatePicker(
        on_change=change_date,
        on_dismiss=date_picker_dismissed,
        first_date=datetime.datetime(2020, 1, 1),
        last_date=datetime.datetime(2100, 10, 1),
    )

    page.overlay.append(date_picker)
    
    date_button = ft.ElevatedButton(
        "Escoger fecha",
        icon=ft.icons.CALENDAR_MONTH,bgcolor= ft.colors.TEAL_400, color=ft.colors.WHITE,
        on_click=lambda _: date_picker.pick_date() ,
    )

    
    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()
    print(selected_files.value)

    page.overlay.append(pick_files_dialog)

    #!Campos a llenar 
    
    Nombre_Cliente_Factura = ft.TextField(label="Nombres", width=280, height=60, hint_text="Ejemplo Joel Sebastian")
    Apellidos_Cliente_Factura = ft.TextField(label="Apellidos", width=280, height=60, hint_text="Ejemplo Morales Jativa")
    Numero_de_celular_factura = ft.TextField(label="Numero de celular", width=570, height=81, max_length=10, hint_text="Ejemplo: 0995566789")
    Cedula_Factura = ft.TextField(label="Cedula o RUC", width=570, height=81, max_length=13, hint_text="Ejemplo: 1234567890")
    Mail_Factura = ft.TextField(label="Correo electronico", width=570, height=60, hint_text="Ejemplo: correo@ejemplo.com")
    Direccion_Factura = ft.TextField(label="Direccion", width=570, height=60, hint_text="Ejemplo: Calle 123, Ciudad")

    Nombre_Cliente_Clientes = ft.TextField(label="Nombres", width=280, height=60, hint_text="Ejemplo Joel Sebastian")
    Apellidos_Cliente_Clientes = ft.TextField(label="Apellidos", width=280, height=60, hint_text="Ejemplo Morales Jativa")
    Numero_de_celular_Clientes = ft.TextField(label="Numero de celular", width=570, height=81, max_length=10, hint_text="Ejemplo: 0995566789")
    Cedula_CLientes = ft.TextField(label="Cedula o RUC", width=570, height=81, max_length=13, hint_text="Ejemplo: 1234567890")
    Mail_Clientes = ft.TextField(label="Correo electronico", width=570, height=60, hint_text="Ejemplo: correo@ejemplo.com")
    Direccion_Clientes = ft.TextField(label="Direccion_Factura", width=570, height=60, hint_text="Ejemplo: Calle 123, Ciudad")

    Nombre_Emisor = ft.TextField(label="Nombre del emisor", width=280, height=45, hint_text="Ejemplo Joel Sebastian")
    Apellidos_Emisor = ft.TextField(label="Apellido del emisor", width=280, height=45, hint_text="Ejemplo Morales Jativa")
    Numero_de_celular_Emisor = ft.TextField(label="Numero de celular", width=570, height=66, max_length=10, hint_text="Ejemplo: 0995566789")
    Cedula_Emisor = ft.TextField(label="Cedula o RUC", width=570, height=66, max_length=13, hint_text="Ejemplo: 1234567890")
    Mail_Emisor = ft.TextField(label="Correo electronico", width=570, height=45, hint_text="Ejemplo: correo@ejemplo.com")
    Direccion_M_Emisor = ft.TextField(label="Direccion Matriz", width=570, height=45, hint_text="Ejemplo: Calle 123, Ciudad")
    Direccion_E_Emisor = ft.TextField(label="Direccion Establecimineto", width=570, height=45, hint_text="Ejemplo: Calle 123, Ciudad")
    Codigo_Establecimiento = ft.TextField(label="Escriba el Codigo del establecimiento", width=250, height=45, hint_text="001")
    Cod_p_omision = ft.TextField(label="Escriba el Codigo del establecimiento", width=250, height=66, hint_text="001")
    Oblig_cont = ft.Checkbox(label="Obligado a llevar contabilidad")
    Rimpe = ft.Checkbox(label="Contribuyente RIMPE")
    Logo = ft.FilePicker()


    #!Campos para Datos del Usuario
    Nombre_Usuario=ft.Text("  ",size=50)

    Primer_Nombre=ft.Text("  ",size=20)
    Segundo_Nombre=ft.Text("  ",size=20)
    Primer_Apellido=ft.Text("  ",size=20)
    Segundo_Apellido=ft.Text("  ",size=20)
    Cedula_Usuario=ft.Text("  ",size=20)
    Numero_Empleado=ft.Text("  ",size=20)
    Sede=ft.Text("  ",size=20)
    page.update()

    #!campos para editar
    Text_Primer_Nombre=ft.TextField(label="Primer Nombre",height=40,width=200)
    text_segundo_nombre=ft.TextField(label="Segundo Nombre",height=40,width=200)
    text_primer_apellido=ft.TextField(label="Primer Apellido",height=40,width=200)
    text_segundo_apellido=ft.TextField(label="Segundo Apellido",height=40,width=200)
    N_celula_empleado=ft.TextField(label="Ingresa tu numero de cedula",height=60,width=420,max_length=10)
    N__empleado=ft.TextField(label="Ingresa tu numero de Empleado",height=40,width=420)
    Lugar_sede=ft.TextField(label="Nombre de Sede",height=40,width=420)
    #!Campos del login
    
    Login_Mail_Factura=ft.TextField(label="Usuario",width=380,height=50)
    Registrar = ft.Column()
    Login_Pasword=ft.TextField(label="Password",width=380,height=50,password=True,can_reveal_password=True)
    
    #!Validar entrada

    
        
    
    '''fail_log = ft.AlertDialog(
        title=ft.Text("Usuario o contraseña incorrecta",color=ft.colors.RED), on_dismiss=lambda e: print("Dialog dismissed!")
            )'''
    
    def open_error_log():
            
            #page.dialog = fail_log
            #fail_log.open = True
            page.snack_bar = ft.SnackBar(ft.Text(f"Usuario o contraseña incorrecta",bgcolor=ft.colors.RED,color=ft.colors.WHITE),bgcolor=ft.colors.RED)
            page.snack_bar.open = True
            page.update()

    def validar_entrada(e):
        if Login_Mail_Factura.value == "admin" and Login_Pasword.value == "admin":
            page.go("/Home")

        else:
            open_error_log()

        
        
        


    
    #!Campo para el Forget password
    clave_recu=ft.TextField(label="Respuesta:",width=380,height=50)

    

    #!Verificacion de campos para agregar datos del cliente
    def send_fac_data(a):
        Nombre_Cliente_Factura.error_text = ""
        Apellidos_Cliente_Factura.error_text = ""
        Numero_de_celular_factura.error_text = ""
        Cedula_Factura.error_text = ""
        Mail_Factura.error_text = ""
        Direccion_Factura.error_text = ""


        if not Nombre_Cliente_Factura.value:
            Nombre_Cliente_Factura.error_text = "Ingrese los nombres"
        if not Apellidos_Cliente_Factura.value:
            Apellidos_Cliente_Factura.error_text = "Ingresa los apellidos"
        if not Numero_de_celular_factura.value:
            Numero_de_celular_factura.error_text = "Ingresa el Numero de telefono celular"
        if not Cedula_Factura.value:
            Cedula_Factura.error_text = "Ingresa la Cedula_Factura"
        if not Mail_Factura.value:
            Mail_Factura.error_text = "Ingresa el correo electronico"
        if not Direccion_Factura.value:
            Direccion_Factura.error_text = "Ingresa la dirección"

            page.update()
        else:
            
            page.update()

    def close_dlg_borrar_prod(e):
        dlg_borrar_items.open = False
        page.update()

    dlg =  ft.AlertDialog( title=ft.Text("Se ha generado el PDF y XML correctamente"),actions=[ft.Image("pdf.png"),ft.Image("xml.png")])
    

    def send_Client_data(a):
        page.dialog = dlg
        dlg.open = True
        page.update()

    dlg_borrar_items = ft.AlertDialog(
            modal=True,
            title=ft.Text("Borrar campos"),
            content=ft.Text("¿Está seguro de borrar todos los proctos en la lista"),
            actions=[
                ft.ElevatedButton("Si", bgcolor=ft.colors.RED,color=ft.colors.WHITE ,on_click=close_dlg_borrar_prod),
                ft.ElevatedButton("No", bgcolor=ft.colors.BLUE_GREY_300,color=ft.colors.WHITE ,on_click=close_dlg_borrar_prod),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Todos los productos han sido eliminados!"),
        )

    def open_dlg_borrar_items(e):
        page.dialog = dlg_borrar_items
        dlg_borrar_items.open = True
        page.update()

     #! Funcion para Cambiar tema        
    def theme(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode=ft.ThemeMode.LIGHT
        else:
            page.theme_mode=ft.ThemeMode.DARK
        page.update()

    
    rail = ft.NavigationRail(
        width=150,
        height=700,
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        #extended=True,
        min_width=130,
        min_extended_width=100,
        #bgcolor= ft.colors.GREEN_200,
        
    
        leading=(ft.Image("banner.png",width=100)),
        group_alignment=-1,
        destinations=[
    
            ft.NavigationRailDestination(
                icon=ft.icons.HOME_OUTLINED, selected_icon=ft.icons.HOME, label="Menu principal",padding=13
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.PERSON_ADD_ALT),
                selected_icon_content=ft.Icon(ft.icons.PERSON_ADD_ALT_SHARP),
                label="Clientes",padding=15
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.INVENTORY_2_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.INVENTORY_2),
                label_content=ft.Text("Inventario"),padding=13
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                label_content=ft.Text("Ajustes"),padding=13
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.PERSON_2_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.PERSON_2),
                label_content=ft.Text("Ususario"),padding=13
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.LOGOUT_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.LOGOUT),
                label_content=ft.Text("Salir"),padding=13
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
                
                                        
                                        ft.Text("Datos del cliente",size=20,),
                                        ft.Row(controls=[Nombre_Cliente_Factura,Apellidos_Cliente_Factura]),
                                        Mail_Factura,Direccion_Factura,Cedula_Factura,Numero_de_celular_factura,
                                        date_button,
                                        ft.Divider(color=ft.colors.TRANSPARENT,height=5),
                                        ft.Row(controls=[ft.ElevatedButton("Limpiar campos",on_click=open_dlg_borrar_items,bgcolor="RED", color=ft.colors.WHITE),ft.ElevatedButton("Consumidor final",bgcolor=ft.colors.BLUE_300,color=ft.colors.WHITE, on_click=send_Client_data), ft.ElevatedButton("Enviar datos", on_click=send_fac_data,bgcolor=ft.colors.GREEN,color=ft.colors.WHITE)],alignment=ft.MainAxisAlignment.SPACE_AROUND,width=565),
                                    
                                    ],alignment=ft.MainAxisAlignment.START
                                        ),
                                ft.VerticalDivider(width=1),
                                ft.Container(width=page.window_width, height=800, alignment=ft.alignment.top_left ,content=ft.Column(
                                    [
                                        
                                        ft.Text("Agrega productos!"),
                                        ft.Row(controls=[TodoApp()],width=380),
                                        
                                        
                                    ],scroll=ft.ScrollMode.ADAPTIVE, alignment=ft.MainAxisAlignment.START,height=700
                                        )),
                                
                                
                            ], expand=True,height=800,alignment=ft.MainAxisAlignment.START,vertical_alignment=ft.CrossAxisAlignment.START
                        )
                    
    
    page_two_ui = ft.Row(
        
                [
                    rail, 
                    ft.VerticalDivider(width=1),
                    ft.Column(
                            [
                
                                        ft.Text("Datos del cliente",size=20,),
                                        ft.Row(controls=[Nombre_Cliente_Clientes,Apellidos_Cliente_Clientes]),
                                        Mail_Clientes,Direccion_Clientes,Cedula_CLientes,Numero_de_celular_Clientes,
                                        ft.Divider(color=ft.colors.TRANSPARENT,height=5),
                                        ft.Row(controls=[ft.FilledButton("Agregar Cliente", on_click=send_Client_data)],alignment=ft.MainAxisAlignment.SPACE_AROUND,width=565),
                                    
                                    ],)
                    
                ], expand=True,height=800,alignment=ft.MainAxisAlignment.START,vertical_alignment=ft.CrossAxisAlignment.START
                    
                        )

    

    page_three_ui = ft.Row(
        [
                    rail,
                    
                    ft.Column([ft.Row([ft.TextField(label="Codigo del producto"),ft.TextField(label="Nombre del producto"),ft.ElevatedButton("Buscar", icon=ft.icons.SEARCH,color=ft.colors.WHITE,bgcolor=ft.colors.GREEN),ft.ElevatedButton("Recargar base de datos", bgcolor=ft.colors.CYAN_900,color=ft.colors.WHITE)]),
                    ft.Container(border=ft.border.all(),content=ft.Column([Data_table],scroll=ft.ScrollMode.ADAPTIVE,height=650),height=600, alignment=ft.alignment.top_center),
                    
                              ]),
                      
                    ft.VerticalDivider(width=1),
                    ft.Column([
                        ft.Divider(height=50),
                        ft.Row(controls=[], alignment=ft.MainAxisAlignment.END)
                        ],alignment=ft.MainAxisAlignment.START,)
                    
                    
                ], expand=True,height=800,alignment=ft.MainAxisAlignment.START,vertical_alignment=ft.CrossAxisAlignment.START
    )

    page_four_ui = ft.Row([

                    rail,
                    ft.VerticalDivider(width=1),
                    ft.Column([ft.Text(
                            "Ajustes",
                            size=50,
                            #color=ft.colors.WHITE,
                            #bgcolor=ft.colors.ORANGE_800,
                            weight=ft.FontWeight.NORMAL,
                            text_align=ft.alignment.center,
                                    ), ft.Row([ft.Column([
                                                            ft.Row(controls=[Nombre_Emisor,Apellidos_Emisor]),Cedula_Emisor,Numero_de_celular_Emisor,Mail_Emisor
                                                            ,Direccion_M_Emisor,Direccion_E_Emisor,Oblig_cont,Rimpe,Logo,Counter(12),
                                                            ],
                                                            
                                                        ),
                                             ft.Column([ ft.ElevatedButton(
                                                                                            "Elige un archivo para el logo de la empresa",
                                                                                            icon=ft.icons.UPLOAD_FILE,
                                                                                            on_click=lambda _: pick_files_dialog.pick_files(
                                                                                                allow_multiple=True
                                                                                            ),
                                                                                        ),],alignment=ft.MainAxisAlignment.START)])
                    
                    
                    ],horizontal_alignment=ft.alignment.center,alignment= ft.MainAxisAlignment.START)
                    
    ], expand=True,height=800,alignment=ft.MainAxisAlignment.START,vertical_alignment=ft.CrossAxisAlignment.START
    )

    #!editar Usuario
    def Controles_editar_usuario(a):
        Primer_Nombre.value=Text_Primer_Nombre.value
        Segundo_Nombre.value=text_segundo_nombre.value
        Primer_Apellido.value=text_primer_apellido.value
        Segundo_Apellido.value=text_segundo_apellido.value
        Cedula_Usuario.value=N_celula_empleado.value
        Numero_Empleado.value=N__empleado.value
        Sede.value=Lugar_sede.value

        Editar_Usuario.open = False
        page.dialog = Mensaje_confirmar_datos
        Mensaje_confirmar_datos.open = True
        page.update()


    def open_Editar_Usuario(e):
        page.dialog =Editar_Usuario
        Editar_Usuario.open = True
        page.update()

    def close_dlg_editar_usuario(e):
        Editar_Usuario.open = False
        page.update()

    def close_dlg_mensaje_confirmar(e):
        Mensaje_confirmar_datos.open = False
        page.update()

    Editar_Usuario = ft.AlertDialog(
        modal=True,
        title=ft.Text("Editar datos"),
        content=ft.Text("Ingresa tus datos                               ",size=25),
        actions=[
            ft.Column(
                [
                    ft.Divider(),
                    ft.Text("Nombres:",size=20),
                    ft.Row(
                        [
                            Text_Primer_Nombre,text_segundo_nombre
                        ]
                    ),
                    ft.Text("Apellidos:",size=20),
                    ft.Row(
                        [
                            text_primer_apellido,text_segundo_apellido
                        ]
                    ),
                    ft.Divider(),
                    ft.Text("Ingrese sus identificadores:",size=20),
                    N_celula_empleado,N__empleado,Lugar_sede,
                    ft.Divider(),
                    ft.Row(
                        [
                            ft.FilledButton(
                                text="Cancelar",
                                on_click=close_dlg_editar_usuario,  
                            ),
                            ft.FilledButton(
                                text="Editar",
                                on_click=Controles_editar_usuario,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    
                ]
            ),
            
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )
    page.update()

    
    Mensaje_confirmar_datos = ft.AlertDialog(
        modal=True,
        title=ft.Text("Datos editados correctamente!"),
        actions=[
            ft.FilledButton("Volver al menu", on_click=close_dlg_mensaje_confirmar),
        ],
        on_dismiss=lambda e: print("Dialog dismissed!"),
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )
    page.update()


    page_five_ui = ft.Row([

        rail,
        ft.VerticalDivider(width=1),
        ft.Container(
            content=ft.Card(
        width=1100,
        height=700,
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
                            
                            ft.Row(
                                [
                                    ft.ElevatedButton(
                                        "Cambiar imagen",
                                        icon=ft.icons.ADD_PHOTO_ALTERNATE_OUTLINED,
                                        on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=True),
                                    ),
                                    ft.ElevatedButton(
                                        "Editar credenciales",
                                        icon=ft.icons.EDIT,
                                        on_click=open_Editar_Usuario,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),

                            #!usuario y files
                            Nombre_Usuario,
                            #!Card de los Datos
                            ft.Container(
                                width=500,
                                height=280,
                                border_radius=20,
                                shadow=ft.BoxShadow(
                                    spread_radius=1,
                                    blur_radius=15,
                                    offset=ft.Offset(0, 0),
                                    blur_style=ft.ShadowBlurStyle.SOLID,
                                ),
                                content=ft.Container(
                                    border_radius=6,
                                    content=ft.Column(
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            ft.Row(
                                                [
                                                    ft.VerticalDivider(width=50),
                                                    ft.Column(
                                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                        controls=[
                                                            ft.Row(
                                                                [
                                                                    ft.Column(
                                                                        [
                                                                            ft.Text("Nombre:",size=20,),
                                                                            ft.Text("Segundo Nombre:",size=20),
                                                                            ft.Text("Primer Apellido:",size=20),
                                                                            ft.Text("Segundo Apellido:",size=20),
                                                                            ft.Text("Cedula:",size=20),
                                                                            ft.Text("N. de empleado",size=20),
                                                                            ft.Text("Sede:",size=20),
                                                                        ]
                                                                    ),
                                                                    ft.VerticalDivider(width=50),
                                                                    ft.Column(
                                                                        [
                                                                            Primer_Nombre,Segundo_Nombre,Primer_Apellido,Segundo_Apellido,
                                                                            Cedula_Usuario,Numero_Empleado,Sede,
                                                                        ]
                                                                    ),
                                                                ]
                                                            )
                                                        ],
                                                    ),
                                                ]
                                            )
                                        ],
                                    ),
                                ),
                            )
                        ],
                    ),
                ],
            ),
        ),
    )
        ),




    ], expand=True,height=800,alignment=ft.MainAxisAlignment.START,vertical_alignment=ft.CrossAxisAlignment.START)       
   

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
            page.update

        if index == 3:
            print(str(index))
            content.controls.pop()
            rail.selected_index = 3
            content.controls.append(page_four_ui)
            page.update

        if index == 4:
            print(str(index))
            content.controls.pop()
            rail.selected_index = 4
            content.controls.append(page_five_ui)
            page.update

        if index == 5:
            Close(e)
            page.update()
        
        page.update()


    

    def on_keyboard(e: ft.KeyboardEvent):
        
        print(f"Key: {e.key}, Control: {e.ctrl}")
        if e.ctrl == True and e.key == "1":
            
            change_index(0)
            
        if e.ctrl == True and e.key == "2":
            
            change_index(1)

        if e.ctrl == True and e.key == "3":
            change_index(2)

        if e.ctrl == True and e.key == "4":
            change_index(3)

        if e.ctrl == True and e.key =="N" :
            theme(e)
            
        
        page.update()
    page.on_keyboard_event = on_keyboard


    #!Funcion para cerrar el programa
    def Close(end):
        page.window_destroy()
        page.update()



    Login_Card=ft.Container(
        image_src="bg.jpg",
        width=page.window_width,
        height=page.window_height,
        expand=True,
        
        
        content=ft.Row(controls=[ft.Card(           
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
                                            border_radius=100
                                        ),
                                        ft.Text("Entrar al facturador", size=22, weight="bold"),
                                        ft.Text(
                                            "TIRANDO FACTOS DESDE 2023",
                                            size=13,
                                            weight="bold",
                                        ),

                                        ft.Divider(height=25, color="transparent"),
                                        Login_Mail_Factura,
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
                                                        ft.Text(value="Olvido la Cotraseña?", size=10),
                                                    ],
                                                )
                                            ),
                                            on_click=lambda _: page.go("/Forgot_Password")    
                                        )
                                    ],
                                ),
                                ft.Divider(height=3, color="transparent"),
                                ft.ElevatedButton("Entrar",bgcolor=ft.colors.GREEN,color=ft.colors.WHITE ,on_click=validar_entrada,width=120,height=40),
                                #ft.Divider(height=35, color="transparent"),
                                #ft.ElevatedButton("Sing-in", on_click=Sing,width=120,height=40),
                            ],
                        ),
                    ),
                ), ft.Column(width=90)], alignment=ft.MainAxisAlignment.END, vertical_alignment= ft.alignment.bottom_center, spacing=100)
    )
    #!Card del forgot password
    Forgot_password=ft.Card(
        width=600,
        height=485,
        content=ft.Container(

            border_radius=6,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            ft.TextButton(
                                "Volver al inicio", icon="ARROW_BACK",
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
                            ft.Text("Escribe tu nombre de usuario",size=20),
                            Login_Mail_Factura,
                            ft.Divider(height=25,color="transparent"),
                            ft.Text("¿Cuál fue el nombre de su primera mascota?",size=20),
                            clave_recu,
                            ft.Divider(height=9,color="transparent"),
                            ft.ElevatedButton("Recuperar cuenta",bgcolor=ft.colors.GREEN,color=ft.colors.WHITE,width=180,height=50),
                            
                        ],
                    ),
                ],
            ),
        ),
    )
    page.appbar = ft.AppBar(         
        leading_width=100,
        title=ft.Text("FACTOS",size=50, weight="bold"),
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
                tooltip="Menu",
                items=[
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        text=("Cerrar sesión"),
                        icon=ft.icons.MANAGE_ACCOUNTS,
                        on_click=lambda _: page.go("/"),
                    ),
                    
                ]
            ),
        ],
    )

  

    def route_change(e):
        
        page.vertical_alignment = "START" , 
        
        page.views.clear()
        if page.route == "/":
            #page.views.append(ft.Container(image_src=))
            page.views.append(
            #!Login
            ft.View(
                "/",
                [   
                    
                    ft.Row(
                        [
                            
                            Login_Card,
                        ],
                        alignment=ft.alignment.top_right,vertical_alignment="center"
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
                    ],vertical_alignment=ft.MainAxisAlignment.CENTER,#scroll=ft.ScrollMode.ADAPTIVE
                    
                    
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