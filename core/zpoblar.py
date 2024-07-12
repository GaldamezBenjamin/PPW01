import sqlite3
from django.contrib.auth.models import User, Permission
from django.db import connection
from datetime import date, timedelta
from random import randint
from core.models import Categoria, Producto, Carrito, Perfil, Boleta, DetalleBoleta, Bodega

def eliminar_tabla(nombre_tabla):
    conexion = sqlite3.connect('db.sqlite3')
    cursor = conexion.cursor()
    cursor.execute(f"DELETE FROM {nombre_tabla}")
    conexion.commit()
    conexion.close()

def exec_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)

def crear_usuario(username, tipo, nombre, apellido, correo, es_superusuario, 
    es_staff, rut, direccion, subscrito, imagen):

    try:
        print(f'Verificar si existe usuario {username}.')

        if User.objects.filter(username=username).exists():
            print(f'   Eliminar {username}')
            User.objects.get(username=username).delete()
            print(f'   Eliminado {username}')
        
        print(f'Iniciando creación de usuario {username}.')

        usuario = None
        if tipo == 'Superusuario':
            print('    Crear Superuser')
            usuario = User.objects.create_superuser(username=username, password='123')
        else:
            print('    Crear User')
            usuario = User.objects.create_user(username=username, password='123')

        if tipo == 'Administrador':
            print('    Es administrador')
            usuario.is_staff = es_staff
            
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.email = correo
        usuario.save()

        if tipo == 'Administrador':
            print(f'    Dar permisos a core y apirest')
            permisos = Permission.objects.filter(content_type__app_label__in=['core', 'apirest'])
            usuario.user_permissions.set(permisos)
            usuario.save()
 
        print(f'    Crear perfil: RUT {rut}, Subscrito {subscrito}, Imagen {imagen}')
        Perfil.objects.create(
            usuario=usuario, 
            tipo_usuario=tipo,
            rut=rut,
            direccion=direccion,
            subscrito=subscrito,
            imagen=imagen)
        print("    Creado correctamente")
    except Exception as err:
        print(f"    Error: {err}")

def eliminar_tablas():
    eliminar_tabla('auth_user_groups')
    eliminar_tabla('auth_user_user_permissions')
    eliminar_tabla('auth_group_permissions')
    eliminar_tabla('auth_group')
    eliminar_tabla('auth_permission')
    eliminar_tabla('django_admin_log')
    eliminar_tabla('django_content_type')
    #eliminar_tabla('django_migrations')
    eliminar_tabla('django_session')
    eliminar_tabla('Bodega')
    eliminar_tabla('DetalleBoleta')
    eliminar_tabla('Boleta')
    eliminar_tabla('Perfil')
    eliminar_tabla('Carrito')
    eliminar_tabla('Producto')
    eliminar_tabla('Categoria')
    #eliminar_tabla('authtoken_token')
    eliminar_tabla('auth_user')

def poblar_bd(test_user_email=''):
    eliminar_tablas()

# Usuarios Subscritos
    crear_usuario(
        username='jtorres',
        tipo='Cliente', 
        nombre='Juana', 
        apellido='Torres', 
        correo=test_user_email if test_user_email else 'jtorres@mail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='16427294-4',	
        direccion='Avenida Mapocho 7282, \nSantiago, \nChile', 
        subscrito=True, 
        imagen='perfiles/jtorres.jpg')

    crear_usuario(
        username='xmolina',
        tipo='Cliente', 
        nombre='Xavier', 
        apellido='Molina', 
        correo=test_user_email if test_user_email else 'xmolina@mail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='18584048-2', 
        direccion='Calle Las Araucarias 199, \nSantiago, \nChile', 
        subscrito=True, 
        imagen='perfiles/xmolina.jpg')

# Usuarios por defecto
    crear_usuario(
        username='mgarrido',
        tipo='Cliente', 
        nombre='María', 
        apellido='Garrido', 
        correo=test_user_email if test_user_email else 'mgarrido@mail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='11990999-7', 
        direccion='Avenida Las Torres 3498, \nSantiago, \nChile', 
        subscrito=False, 
        imagen='perfiles/mgarrido.jpg')

    crear_usuario(
        username='mrojas',
        tipo='Cliente', 
        nombre='María', 
        apellido='Rojas', 
        correo=test_user_email if test_user_email else 'mrojas@mail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='14821693-0', 
        direccion='Calle Salvador Gutiérrez 6716, \nSantiago, \nChile', 
        subscrito=False, 
        imagen='perfiles/mrojas.jpg')

# Staff
    crear_usuario(
        username='egutierrez',
        tipo='Administrador', 
        nombre='Esperanza', 
        apellido='Gutierrez', 
        correo=test_user_email if test_user_email else 'egutierrez@mail.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='13248948-0', 
        direccion='Pasaje Manquehue Norte 1238 Vitacura, \nSantiago, \nChile', 
        subscrito=False, 
        imagen='perfiles/egutierrez.jpg')
    
    crear_usuario(
        username='alozano',
        tipo='Administrador', 
        nombre='Axel', 
        apellido='Lozano', 
        correo=test_user_email if test_user_email else 'alozano@mail.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='13057339-7', 
        direccion='Avenida Pedro De Valdivia 521 - B, \nSantiago, \nChile', 
        subscrito=False, 
        imagen='perfiles/alozano.jpg')

# Superusuario
    crear_usuario(
        username='super',
        tipo='Superusuario',
        nombre='Ivan',
        apellido='Vidal',
        correo=test_user_email if test_user_email else 'ividal@mail.com',
        es_superusuario=True,
        es_staff=True,
        rut='14725738-2',
        direccion='Calle Germán Ebbinghauss 0258, \nSantiago, \nChile',
        subscrito=False,
        imagen='perfiles/ividal.jpg')
    
    categorias_data = [
        { 'id': 1, 'nombre': 'Acción/Aventura'},
        { 'id': 2, 'nombre': 'Shooter'},
        { 'id': 3, 'nombre': 'RPG'},
        { 'id': 4, 'nombre': 'Estrategia'},
        { 'id': 5, 'nombre': 'Puzzle'},
        { 'id': 6, 'nombre': 'Simulación'},
        { 'id': 7, 'nombre': 'Carreras'},
    ]

    print('Crear categorías')
    for categoria in categorias_data:
        Categoria.objects.create(**categoria)
    print('Categorías creadas correctamente')

    productos_data = [
        # Categoría "Acción/Aventura" (7 juegos)
        {
            'id': 1,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'ELDEN RING',
            'descripcion': 'Un juego de rol y acción desarrollado por FromSoftware, conocido por su mundo abierto expansivo y colaborativo creado junto a George R.R. Martin. Combina combate desafiante y exploración profunda en un mundo de fantasía oscura.',
            'precio': 34990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 25,
            'imagen': 'productos/000001.jpg'
        },
        {
            'id': 2,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Red Dead Redemption 2',
            'descripcion': 'Una épica aventura en el Salvaje Oeste desarrollada por Rockstar Games. Sigue a Arthur Morgan y su pandilla mientras luchan por sobrevivir en un mundo en transformación a finales del siglo XIX.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 25,
            'imagen': 'productos/000002.jpg'

        },
        {
            'id': 3,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Grand Theft Auto V',
            'descripcion': 'Un juego de mundo abierto de Rockstar Games que sigue las historias entrelazadas de tres criminales en la ciudad ficticia de Los Santos. Ofrece una experiencia inmersiva con misiones variadas, actividades y multijugador en línea.',
            'precio': 29990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 25,
            'imagen': 'productos/000003.jpg'

        },
        {
            'id': 4,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Marvel\'s Spider-Man: Miles Morales',
            'descripcion': 'Sigue la historia de Miles Morales mientras aprende a ser Spider-Man en un mundo lleno de peligros. Desarrollado por Insomniac Games, ofrece una narrativa emocionante y combate dinámico en un entorno urbano detallado.',
            'precio': 34990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 25,
            'imagen': 'productos/000004.jpg'
        },
        {
            'id': 5,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Watch Dogs: Legion',
            'descripcion': 'Un juego de acción y aventura en mundo abierto donde puedes reclutar y jugar como cualquier ciudadano de Londres para luchar contra un régimen autoritario. Ofrece mecánicas innovadoras y una ciudad futurista detallada.',
            'precio': 44990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000005.jpg'
        },
        {
            'id': 6,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Watch_Dogs 2',
            'descripcion': 'Sigue a Marcus Holloway mientras hackea su camino a través de San Francisco para combatir la corrupción. Con un enfoque en el hackeo y la exploración de un mundo abierto, ofrece una experiencia rica y dinámica.',
            'precio': 34990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000006.jpg'

        },
        {
            'id': 7,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'DRAGON BALL Z: KAKAROT',
            'descripcion': 'Revive la historia de Goku en este RPG de acción que cubre todos los arcos principales de Dragon Ball Z. Ofrece combates intensos, exploración y momentos icónicos de la serie.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 25,
            'imagen': 'productos/000007.jpg'
        },

        # Categoría "Shooter" (5 Juegos)
        {
            'id': 8,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Atomic Heart',
            'descripcion': 'Un juego de acción en primera persona ambientado en una realidad alternativa de la Unión Soviética. Combina elementos de ciencia ficción con combate intenso y una narrativa intrigante.',
            'precio': 43990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000008.jpg'
        },
        {
            'id': 9,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Far Cry 6',
            'descripcion': 'Ambientado en la isla ficticia de Yara, sigue la lucha de los guerrilleros contra un dictador opresivo. Ofrece un mundo abierto vibrante y lleno de acción, con una historia profunda y personajes memorables.',
            'precio': 41500,
            'descuento_subscriptor': 5,
            'descuento_oferta': 25,
            'imagen': 'productos/000009.jpg'
        },
        {
            'id': 10,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'DOOM Eternal',
            'descripcion': 'Un shooter en primera persona frenético y brutal, donde el jugador combate hordas de demonios en diversos entornos infernales. Ofrece una acción intensa y mecánicas de juego rápidas.',
            'precio': 26990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 25,
            'imagen': 'productos/000010.jpg'
        },
        {
            'id': 11,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Ghostrunner 2',
            'descripcion': 'Un juego de acción en primera persona que combina parkour y combate con espadas en un entorno cyberpunk. La secuela amplía las mecánicas de su predecesor con nuevos desafíos y enemigos.',
            'precio': 29990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000011.jpg'
        },
        {
            'id': 12,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Tom Clancy\'s Rainbow Six Siege',
            'descripcion': 'Un shooter táctico en primera persona que enfatiza la cooperación en equipo y la estrategia. Los jugadores asumen roles de operadores de élite en escenarios de rescate y enfrentamientos.',
            'precio': 15990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 25,
            'imagen': 'productos/000012.jpg'
        },
        
        # Categoría "RPG" (3 Juegos)
        {
            'id': 13,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'The Witcher 3: Wild Hunt',
            'descripcion': 'Un RPG de mundo abierto donde juegas como Geralt de Rivia, un cazador de monstruos, en una búsqueda épica. Ofrece una narrativa rica, un mundo expansivo y decisiones significativas.',
            'precio': 19990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 25,
            'imagen': 'productos/000013.jpg'
        },
        {
            'id': 14,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Diablo IV',
            'descripcion': 'Un RPG de acción con una oscura y gótica atmósfera, donde los jugadores luchan contra hordas de demonios y exploran un vasto mundo. Ofrece combate visceral, personalización de personajes y una historia épica.',
            'precio': 44990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 25,
            'imagen': 'productos/000014.jpg'
        },
        {
            'id': 15,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Baldur\'s Gate 3',
            'descripcion': 'Un RPG basado en Dungeons & Dragons que combina narrativa profunda con combate táctico por turnos. Ofrece exploración, toma de decisiones y desarrollo de personajes en un mundo de fantasía.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000015.jpg'
        },

        # Categoría "Estrategia" (5 Juegos)
        {
            'id': 16,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Marvel\'s Midnight Suns',
            'descripcion': 'Un RPG táctico donde los jugadores lideran un equipo de superhéroes para enfrentar una amenaza sobrenatural. Combina estrategia, combate por turnos y una historia inmersiva.',
            'precio': 49990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000016.jpg'
        },
        {
            'id': 17,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Balatro',
            'descripcion': 'El roguelike de póquer. Balatro es un creador de mazos hipnotizante donde juegas manos de póquer ilegal, descubres comodines que cambian tu juego y activas combinaciones hilarantes y llenas de adrenalina.',
            'precio': 7990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000017.jpg'
        },
        {
            'id': 18,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Age of Empires 4',
            'descripcion': 'Un juego de estrategia en tiempo real que permite a los jugadores construir y expandir imperios a lo largo de la historia. Ofrece campañas históricas detalladas y multijugador competitivo.',
            'precio': 19990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000018.jpg'
        },
        {
            'id': 19,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Aliens: Dark Descent',
            'descripcion': 'Lánzate a la fascinante aventura de Aliens: Dark Descent, un juego de acción en escuadrón de un solo jugador dentro de la franquicia Alien. Lidera a tus soldados a detener un nuevo tipo de invasión terrorífica de xenomorfos en Moon Lethe.',
            'precio': 26990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000019.jpg'
        },
        {
            'id': 20,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Wasteland 3',
            'descripcion': 'Un RPG táctico post-apocalíptico que sigue a un grupo de Rangers en su lucha por sobrevivir en un Colorado helado. Ofrece decisiones significativas, combate estratégico y una historia envolvente.',
            'precio': 18500,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000020.jpg'
        },

        # Categoría "Puzzle" (3 Juegos)
        {
            'id': 21,
            'categoria': Categoria.objects.get(id=5),
            'nombre': 'COCOON',
            'descripcion': 'Jeppe Carlsen, el diseñador de jugabilidad principal que dio vida a LIMBO e INSIDE, presenta ahora COCOON, un juego que te llevará de aventuras a través de mundos dentro de mundos.',
            'precio': 12500,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000021.jpg'
        },
        {
            'id': 22,
            'categoria': Categoria.objects.get(id=5),
            'nombre': 'Superliminal',
            'descripcion': 'Un juego de puzzles en primera persona que desafía la percepción y la perspectiva. Los jugadores resuelven acertijos manipulando el entorno y las ilusiones ópticas.',
            'precio': 7500,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000022.jpg'
        },
        {
            'id': 23,
            'categoria': Categoria.objects.get(id=5),
            'nombre': 'The Talos Principle 2',
            'descripcion': 'La secuela del aclamado juego de puzzles filosófico, donde los jugadores resuelven desafíos mientras exploran temas profundos sobre la existencia y la humanidad.',
            'precio': 15500,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000023.jpg'
        },

        # Categoría "Simulación" (5 Juegos)
        {
            'id': 24,
            'categoria': Categoria.objects.get(id=6),
            'nombre': 'Stardew Valley',
            'descripcion': 'Un simulador de vida y agricultura donde los jugadores cultivan su propia granja, interactúan con los aldeanos y exploran cuevas. Ofrece una experiencia relajante y adictiva.',
            'precio': 7500,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000024.jpg'
        },
        {
            'id': 25,
            'categoria': Categoria.objects.get(id=6),
            'nombre': 'Farming Simulator 22',
            'descripcion': 'Un simulador realista de agricultura que permite a los jugadores gestionar sus propias granjas, cultivar cosechas y criar animales. Ofrece una experiencia detallada y auténtica.',
            'precio': 19990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000025.jpg'
        },
        {
            'id': 26,
            'categoria': Categoria.objects.get(id=6),
            'nombre': 'ACE COMBAT 7: SKIES UNKNOWN',
            'descripcion': 'Un simulador de vuelo de combate que ofrece misiones emocionantes y gráficos impresionantes. Los jugadores pilotan aviones en combates aéreos intensos.',
            'precio': 45990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000026.jpg'
        },
        {
            'id': 27,
            'categoria': Categoria.objects.get(id=6),
            'nombre': 'MADiSON',
            'descripcion': 'MADiSON es un videojuego de terror psicológico que ofrece una experiencia inmersiva y terrorífica. Con la ayuda de una cámara instantánea, une el mundo de los vivos con el de los muertos, toma fotografías y agitalas para revelarlas. Resuelve puzles, explora tus alrededores y trata de sobrevivir.',
            'precio': 14500,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000027.jpg'
        },
        {
            'id': 28,
            'categoria': Categoria.objects.get(id=6),
            'nombre': 'Untitled Goose Game',
            'descripcion': 'Un juego de puzzles y sigilo donde los jugadores controlan a un ganso travieso que causa caos en un pueblo inglés. Ofrece humor y creatividad en sus desafíos.',
            'precio': 9990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000028.jpg'
        },

        # Categoría "Carreras" (2 Juegos)
        {
            'id': 29,
            'categoria': Categoria.objects.get(id=7),
            'nombre': 'Forza Horizon 4',
            'descripcion': 'Un juego de carreras de mundo abierto ambientado en una recreación de Gran Bretaña. Ofrece una variedad de vehículos, eventos dinámicos y un entorno detallado.',
            'precio': 49990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000029.jpg'
        },
        {
            'id': 30,
            'categoria': Categoria.objects.get(id=7),
            'nombre': 'Assetto Corsa Competizione',
            'descripcion': 'Un simulador de carreras que ofrece una experiencia realista y precisa de la conducción. Focalizado en las competiciones de GT3, destaca por su física y gráficos avanzados.',
            'precio': 35990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000030.jpg'
        },
    ]

    print('Crear productos')
    for producto in productos_data:
        Producto.objects.create(**producto)
    print('Productos creados correctamente')

    print('Crear carritos')
    for rut in ['16427294-4', '11990999-7']:
        cliente = Perfil.objects.get(rut=rut)
        for cantidad_productos in range(1, randint(9, 13)):
            producto = Producto.objects.get(pk=randint(1, 24))
            if cliente.subscrito:
                descuento_subscriptor = producto.descuento_subscriptor
            else:
                descuento_subscriptor = 0
            descuento_oferta = producto.descuento_oferta
            descuento_total = descuento_subscriptor + descuento_oferta
            descuentos = int(round(producto.precio * descuento_total / 100))
            precio_a_pagar = producto.precio - descuentos
            Carrito.objects.create(
                cliente=cliente,
                producto=producto,
                precio=producto.precio,
                descuento_subscriptor=descuento_subscriptor,
                descuento_oferta=descuento_oferta,
                descuento_total=descuento_total,
                descuentos=descuentos,
                precio_a_pagar=precio_a_pagar
            )
    print('Carritos creados correctamente')

    print('Crear boletas')
    nro_boleta = 0
    perfiles_cliente = Perfil.objects.filter(tipo_usuario='Cliente')
    for cliente in perfiles_cliente:
        estado_index = -1
        for cant_boletas in range(1, randint(6, 21)):
            nro_boleta += 1
            estado_index += 1
            if estado_index > 3:
                estado_index = 0
            estado = Boleta.ESTADO_CHOICES[estado_index][1]
            fecha_venta = date(2024, randint(1, 5), randint(1, 28))
            fecha_despacho = fecha_venta + timedelta(days=randint(0, 3))
            fecha_entrega = fecha_despacho + timedelta(days=randint(0, 3))
            if estado == 'Anulado':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Vendido':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Despachado':
                fecha_entrega = None
            boleta = Boleta.objects.create(
                nro_boleta=nro_boleta, 
                cliente=cliente,
                monto_sin_iva=0,
                iva=0,
                total_a_pagar=0,
                fecha_venta=fecha_venta,
                fecha_despacho=fecha_despacho,
                fecha_entrega=fecha_entrega,
                estado=estado)
            detalle_boleta = []
            total_a_pagar = 0
            for cant_productos in range(1, randint(4, 6)):
                producto_id = randint(1, 10)
                producto = Producto.objects.get(id=producto_id)
                precio = producto.precio
                descuento_subscriptor = 0
                if cliente.subscrito:
                    descuento_subscriptor = producto.descuento_subscriptor
                descuento_oferta = producto.descuento_oferta
                descuento_total = descuento_subscriptor + descuento_oferta
                descuentos = int(round(precio * descuento_total / 100))
                precio_a_pagar = precio - descuentos
                bodega = Bodega.objects.create(producto=producto)
                DetalleBoleta.objects.create(
                    boleta=boleta,
                    bodega=bodega,
                    precio=precio,
                    descuento_subscriptor=descuento_subscriptor,
                    descuento_oferta=descuento_oferta,
                    descuento_total=descuento_total,
                    descuentos=descuentos,
                    precio_a_pagar=precio_a_pagar)
                total_a_pagar += precio_a_pagar
            monto_sin_iva = int(round(total_a_pagar / 1.19))
            iva = total_a_pagar - monto_sin_iva
            boleta.monto_sin_iva = monto_sin_iva
            boleta.iva = iva
            boleta.total_a_pagar = total_a_pagar
            boleta.fecha_venta = fecha_venta
            boleta.fecha_despacho = fecha_despacho
            boleta.fecha_entrega = fecha_entrega
            boleta.estado = estado
            boleta.save()
            print(f'    Creada boleta Nro={nro_boleta} Cliente={cliente.usuario.first_name} {cliente.usuario.last_name}')
    print('Boletas creadas correctamente')

    print('Agregar productos a bodega')
    for producto_id in range(1, 24):
        producto = Producto.objects.get(id=producto_id)
        cantidad = 0
        for cantidad in range(1, randint(2, 46)):
            Bodega.objects.create(producto=producto)
        print(f'    Agregados {cantidad} "{producto.nombre}" a la bodega')
    print('Productos agregados a bodega')

