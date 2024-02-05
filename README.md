# Definición proyecto

Mi proyecto será sobre emparejamientos de partidos de fútbol sala, 7 u 11.

Consiste en una app para poder reservar campos de fútbol que estén alrededor de un usuario.

Tenemos 2 variantes:
- Eventos privados: Si tienes el número de jugadores necesario para formar 2 equipos y lo que estás buscando es alquilar un campo, podrás reservarlo para un evento privado
- Eventos públicos: Si lo que necesitas es a más gente para jugar, creas un partido público con los amigos que seáis y otros usuarios podrán unirse al partido

Podrán también organizarse torneos en los cuales como requisito debes tener un equipo completo de fútbol.

También contamos con la opción de reservar pistas de fútbol habilitadas para realizar entrenamientos con tu equipo de fútbol.

Todo esto contará con perfiles de usuarios los cuales indicarán información del jugador como:
- Números de partidos jugados, ganados y perdidos
- Mediante estadística, se calculará el porcentaje de nivel del jugador con los resultados registrados de los partidos
- Posición preferida, equipos profesionales donde jugó, tiempo de experiencia, etc.

Se cuenta también con un apartado de posts en los cuales podrás compartir los resultados de partidos, crear alertas de partidos abiertos o contenido multimedia a gusto del usuario.

# Examen

- He comentado en las vistas y en los formularios EXAMEN y todo lo que he hecho es apartir de ahi hacia abajo. Está todo añadido al final

- He usado automatic-crud en la eliminación, el template es "appFutbol/promocion_confirm_delete.html"

- La vista "promociones_realizadas" es la lista de promociones

- La vista "promocion_create" es para crear

- La vista "promocion_avanzada" para busqueda avanzada

- La vista "promocion_editar" para actualizar

# Creación Aplicación Web Parte IV - CRUD

### Validaciones

#### Usuarios

- El email del usuario es único
- El nivel de un usuario no puede ser superior a 10.
- He usado el widget "forms.TextInput" para crear un placeholder

#### Partido

- Advertencia!! No puse el campo Estado queriendo ya que un partido, se sobreentiende que cuando se crea siempre estará disponible y nunca completo.
- hora: no puedes crear un partido con la hora antes de las 7:00
- tipo + estilo: No se pueden crear partidos de fútbol sala con la creación de partidos públicos.
- usuarios jugadores: si selecciono más jugadores del total de un estilo de juego (sala=10 jugadores en total, 7=14 jugadores o 11=22 jugadores), nos retorna error
- Uso el widget "forms.Select()" para sacar un desplegable de un campo TimeField() y poder seleccionar una hora. He creado una lista "horas_choices" para el deplegable del Select y en la validación paso los datos a objeto datetime para que compare bien las horas.

#### Recinto

- nombre: debe ser único
- teléfono: no puede tener menos de 9 carácteres

#### Resultado

- Si el creador del partido es el mismo que el usuario logueado aparecerá un botón para crear el resultado del partido.

# Creación Aplicación Web Parte V - Sesiones y Autenticación

### Usuario

- Mis usuarios son el dueño del recinto que podrá crear recintos y el cliente que usará la aplicación para crear partidos

#### Permisos
- Los usuarios "cliente" son los únicos que podrán hacer búsqueda avanzada de partidos, eliminar, editar y crear
- Los usuarios "dueñorecinto" son los únicos que pueden añadir, editar y borrar recintos.
- NOTA: no me deja añadir ni un recinto nuevo ni un partido, los cree con el superusuario en admin, sorry

# API REST I
En el index principal, las vistas que he manejado están:
- Consulta sencilla: Desplegable de "Partido" (Ver partidos_api)
- Consulta mejorada: Desplegable de "Partido" (Ver partidos_api_mejorada)
- Consulta mejorada con token oauth2 primera: Barra de navegación superior (Datos Usuarios)
- Consulta mejorada con token oauth2 segunda: Desplegable de "Recinto" (Ver recintos api)
- Consulta mejorada con token JWT: Barra de navegación superior (Lsta posts api)

# API REST II
NOTA: está hecho el fixtures para los dos tipos de usuarios con autenticaciones
En el index principal, las vistas que he manejado están:
- Búsqueda sencilla modelo principal y avanzada (no es el principal pero lo he hecho de ese): barra de búsqueda
- Búsqueda avanzada modelo principal: desplegable de "Recinto"
- Búsqueda avanzada partidos: desplegable de "Partidos"
- Búsqueda avanzada datos usuarios: desplegable "Datos Usuarios"