import flet as ft

def main(page: ft.Page):

     #!Campos a llenar 
    
    Nombre_Usuario=ft.TextField(label="Nombre de Usuario",width=280,height=45)
    Apeliido_Usuaio=ft.TextField(label="Apellido de Usuario",width=280,height=45)
    Telefono=ft.TextField(label="Telefono",width=570,height=45)
    Cedula=ft.TextField(label="Cedula",width=570,height=45)
    Mail=ft.TextField(label="E-Mail",width=570,height=45)
    Direccion=ft.TextField(label="Direccio",width=570,height=45)
    
    greetings = ft.Column()
    #!Campos del login
    
    Login_Mail=ft.TextField(label="Usuario",width=380,height=50)
    Registrar = ft.Column()
    Login_Pasword=ft.TextField(label="Password",width=380,height=50,password=True,can_reveal_password=True)
    
    #!Campo para el Forget password
    Olvido_Contraseña=ft.TextField(label="Correo Electronico",width=500,height=80)

    #!Verificacion de campos
    def send_fac_data(a):
        if not Nombre_Usuario.value:
            Nombre_Usuario.error_text = "Please enter your name"
            page.update()
        else:

            name = Nombre_Usuario.value
            
            greetings = (ft.Text(f"Nombre: {Nombre_Usuario.value} {Apeliido_Usuaio.value}"))
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
                icon_content=ft.Icon(ft.icons.PERSON_OUTLINE),
                selected_icon_content=ft.Icon(ft.icons.PERSON_ROUNDED),
                label="Clientes",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.SETTINGS),
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
                                        Mail,Direccion,Cedula,Telefono,ft.ElevatedButton("Enviar datos", on_click=send_fac_data),
                                    ],
                                        )
                            ],
                            expand=True,height=800
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
                                
                    ft.VerticalDivider(width=1),
                    ft.Text(["pag 3"])
                ],
                    expand=True,height=800,alignment=ft.MainAxisAlignment.START
    )


    #!Tema y Titulo de la pagina
    page.theme_mode = ft.ThemeMode.LIGHT
   

    content = ft.Row([page_one_ui])
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
        
        if (e.ctrl == True and e.key == "1"):
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
                                src=f"https://i.ibb.co/HTt7LK3/Logo-Png.png",
                                width=450,
                                height=140  ,
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
        page.horizontal_alignment = "center",
        page.vertical_alignment = "center" , 
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
                                content,greetings,
                        
                            ],
                            alignment=(ft.MainAxisAlignment.START)
                        )
                    ]
                    
                    
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

ft.app(target=main)