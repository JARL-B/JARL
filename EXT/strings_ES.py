#: español

{
    'blacklisted' : ''':x: Este canal está en la blacklist :x:''',

    'admin_required' : 'Necesitas permisos de administrador para usar este comando.',

    'help' : '''Por favor visita https://jellywx.co.uk/help?lang=ES''',

    'help_raw' : [
['Comandos de recordatorios', {
'$del' : 'Elimina recordatorios e intervalos en tu servidor.',

'$remind [usuario/canal] <tiempo-para-recordatorio> <mensaje>' : 'coloca un recordatorio. El tiempo debe ponerse como [num][s/m/h/d], por ejemplo 10s para 10 segundos o 2s10m para 2 segundos 10 minutos. Un tiempo exacto puede ser colocado como `día`/`mes`/`año`-`hora`:`minuto`:`segundo`.',

'$interval [usuario/canal] <tiempo-para-recordatorio> <intervalo> <mensaje>' : 'coloca un intervalo, donde el `mensaje` se enviará cada cierto `intervalo` iniciando desde el `tiempo-para-recordatorio` dado. El tiempo se coloca como dice arriba. Ej. `$interval 0s 20m ¡Hola Mundo!` enviará `¡Hola Mundo!` a tu canal cada 20 minutos.',

'$todo' : 'comandos relacionado a la lista TO-DO (lista de tareas). Utiliza `$todo help` para más información.',

'$todos' : 'lo mismo que `$todo` pero para tareas a nivel de servidor.',

'$timezone' : 'configura la zona horaria del servidor, para facilitar los recordatorios basados en tiempo.'
}],

['Comandos de administración', {
'$autoclear [veces] [canales]' : 'activa/desactiva la limpieza automática de mensajes, donde los mensajes enviados al canal (por defecto el canal en el que estás) serán eliminados automáticamente luego de un tiempo (por defecto 10 segundos).',

'$clear <usuarios>' : 'elimina mensajes enviados por los usuarios mencionados.',

'$restrict [roles]' : 'añade/remueve permiso a ciertos roles mencionados para colocar recordatorios e intervalos.',

'$tag' : 'comando para alias. Utiliza `$tag help` para más información.',

'$blacklist [canal]' : 'bloquea o desbloquea un canal de enviar comandos.'
}],

['Otros comandos', {
'$donate' : 'muestra información sobre donaciones.',

'mbprefix <prefijo>' : 'cambia el prefijo "$". ¡Este comando no utiliza un prefijo!',

'$info' : 'obtén información sobre el bot.',

'$lang <nombre>' : 'cambia el idioma.',

'$clock' : 'obtén la hora actual.'}]
],

    'web_foot_title' : 'Información extra',
    'web_foot' : '¡No coloques los paréntesis al escribir un comando! Por ejemplo, `mbprefix !`, no `mbprefix <!>`',
    'web_foot2' : 'Por favor dirígete a nuestro servidor de Discord si necesitas más ayuda',

    'about' : {'Sobre el bot' : ['Creado por: Jude Southworth', 'Github: <a href=https://github.com/JellyWX>https://github.com/JellyWX</a>', 'Want a bot making? Please contact me on Discord.', 'Hosting provider: OVH']},

    'join' : 'Ingresa a nuestro servidor de Discord',
    'invite' : 'Invita el bot a tu servidor',

    'info' : '''
Prefijo por defecto: `$`
Prefijo seleccionado: `@{user} prefix $`
Ayuda: `{prefix}help`

**Bienvenido a RemindMe!**
Desarrollador: <@203532103185465344>
Un chico cool: <@174243954487853056>
Ícono: <@253202252821430272>
Encuéntrame en https://discord.gg/WQVaYmT y en https://github.com/JellyWX :)

Framework: `discord.py`
Proveedor de host: OVH

Mi otro bot (solo Patreon):
https://discordapp.com/oauth2/authorize?client_id=411224415863570434&scope=bot&permissions=35840

*Si tienes consultas sobre nuevas caracterísicas, por favor envíalas a nuestro servidor de Discord*
*Si tienes consultas sobre desarrollo de bot para tí y tu servidor, por favor envíame un mensaje directo*
''',

    'donate' : '''
¿Pensando en aportar una contribución mensual? Presiona abajo para mi Patreon y el servidor oficial del bot :D
https://www.patreon.com/jellywx

https://discord.gg/WQVaYmT

Aquí hay un poco más información:

Cuando donas, Patreon automáticamente te dará el rango en nuestro servidor de Discord, siempre y cuando hayas vinculado tu Patreon con Discord.
Con tu nuevo rango, podrás:
: usar comandos exclusivos como `interval`
: colocar más recordatorios (ilimitados)
: colocar recordatorios más largos (2000 caracteres)
: seleccionar más/largos tags

Para quienes estén en Patreon, muchas gracias :D Haces que este bot pueda sostenerse.

Ten en cuenta que debes estar conectado a nuestro servidor de Discord para recibir las recompenzas de Patreon.
''',

    'prefix' : {
        'no_argument' : '''
Por favor utiliza este comando como `mbprefix <prefijo>`
''',
        'success' : '''
Prefijo cambiado a {prefix}
''',

        'too_long' : '''Please select a prefix under 5 characters'''
    },

    'timezone' : {

        'no_argument' : '''
Uso:
    ```{prefix}timezone <nombre>```
Example:
    ```{prefix}timezone Europe/London```
Todas las zonas horarias: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
Zona horaria actual: {timezone}''',

        'no_timezone' : '''Zona horaria no reconocida. Una lista está disponible en https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568''',

        'success' : '''La zona horaria ha sido cambiada a {timezone}. Tu hora actual debería ser {time}'''
    },

    'restrict' : {

        'disabled' : '''Desactivados los permisos de recordatorios para el rol.''',

        'enabled' : '''Activados los permisos de recordatorios para el rol.''',

        'allowed' : '''Roles permitidos: {}'''
    },

    'clear' : {

        'no_argument' : '''Por favor menciona los usuarios de los que deseas eliminar los mensajes.'''

    },

    'remind' : {
        'no_argument' : '''
Uso:
    ```{prefix}remind [canal o usuario] <tiempo para/tiempo exacto> <mensaje>```
Ejemplo:
    ```{prefix}remind #general 10s Hola mundo```
    ```{prefix}remind 10:30 Son las 10:30```''',

        'invalid_tag' : '''No es posible encontrar la localización de tu tag.''',

        'invalid_time' : '''Asegúrate que la hora que colocaste es en el formato [num][s/m/h/d][num][s/m/h/d] etc. o `día/mes/año-hora:minuto:segundo`.''',

        'invalid_count' : '''¡Demasiados recordatorios en el canal especificado! Utiliza `{prefix}del` para eliminar algunos, o utiliza `{prefix}donate` para aumentar el límite (tier de $5).''',

        'invalid_chars' : '''¡Recordatorio demasiado largo! (máx. 150, usaste {}). Utiliza `{prefix}donate` para aumentar el límite a 1900 caracteres (tier de $5).''',

        'invalid_chars_2000' : '''Discord no permite colocar recordatorios con 2000+ caracteres. Lo siento,''',

        'no_perms' : '''Necesitas `Administrar Mensajes` tener un rol con el cual puedas colocar recordaorios a ese canal. Contacta al admnistrador de tu servidor y dile que utilice el comando `{prefix}restrict` para especificar roles permitidos.''',

        'success' : '''Nuevo recordatorio registrado para <{}{}> en {} segundos. Ya no puedes editarlo, así que eres libre de eliminarlo.'''
    },

    'interval' : {
        'no_argument' : '''
Uso:
    ```{prefix}interval [canal o usuario] <tiempo para/tiempo exacto> <intervalo> <mensaje>```
Ejemplo:
    ```{prefix}interval #general 9:30 1d ¡Buen día!```
    ```{prefix}interval 0s 10s Esto será muy irritante```''',

        'invalid_interval' : '''Asegúrate que la hora que colocaste es en el formato [num][s/m/h/d][num][s/m/h/d] etc. sin espacios, ej. 10s para 10 segundos o 10s12m15h1d for 10 segundos, 12 minutos, 15 horas y 1 día.''',

        '8_seconds' : '''Por favor asegúrate que tu intervalo es mayor a 8 segundos.''',

        'donor' : '''¡Necesitas ser un Patreon (dona 2$ o más) para acceder a este comando! Escribe `{prefix}donate` para más información.''',

        'success' : '''Nuevo intervalo registrado para <{}{}> en {} segundos . Ya no puedes editarlo, así que eres libre de eliminarlo.''',

        'removed' : '''Parece que no hay Patreons en tu servidor, por lo tanto el intervalo se ha eliminado.'''

    },

    'autoclear' : {
        'disable' : '''Autolimpieza desactivada en {}''',

        'enable' : '''Autolimpieza de {} segundos activada.''',
    },

    'del' : {
        'listing' : '''Listando recordatorios en este servidor... (puede haber un pequeño retraso, espera que el mensaje "Selecciona (1,2,3...)" aparezca).''',

        'listed' : '''Selecciona (1,2,3...) el recordaorio que quieres eliminar, o escribe cualquier otra cosa para cancelar.''',

        'count' : '''¡Se han eliminado {} recordatorios!'''
    },

    'todo' : {
        'server_only' : '''Por favor utiliza `{prefix}todo` para tu lista de tareas personal. `{prefix}todos` es para las tareas del servidor entero.''',

        'add' : '''*Pon `{prefix}{command} add <mensaje>` para añadir un ítem a tu TODO, o escribe `{prefix}{command} help` para más comandos*''',

        'too_long' : '''Disculpa, pero los ítems están limitados a 80 caracteres. Mantenlo conciso :)''',

        'too_long2' : '''Disculpa, pero la lista no puede excederse de los 800 caracteres. ¿Tal vez completar algunas tareas?''',

        'added' : '''¡Añadido \'{name}\' a la lista de tareas!''',

        'removed' : '''¡Eliminado \'{}\' de la lista de tareas!''',

        'error_value' : '''El ítem a remover ha de ser un número. Mira el número de las tareas usando `{prefix}{command}`''',

        'error_index' : '''No se pudo encontrar un ítem con ese número. ¿Estás en la lista correcta?''',

        'help' : '''Para usar comandos de la lista de tareas (TODO), pon `{prefix}{command} add <mensaje>`, `{prefix}{command} remove <número>`, `{prefix}{command} clear` y `{prefix}{command}` para añadir, remover, limpiar o mirar tu lista de tareas.''',

        'cleared' : '''¡Limpiada la lista de tareas!'''
    },

    'tags' : {

        'deleted' : '''Eliminado el tag {}''',

        'added' : '''Añadido el tag {}''',

        'invalid_count' : '''Lo siento, para usuarios normales hay un límite de 6 tags. Por favor elimina algunos o considera donar con `{prefix}donate` (tier de 5$).''',

        'invalid_chars' : '''Los tags están limitados a 80 caracteres. ¡Mantenlo conciso!''',

        'colon' : '''Por favor añade dos puntos para separar el nombre del tag con el cuerpo.''',

        'illegal' : '''Por favor no utilices palabras claves `add, new, remove, del` en el nombre de tus tags.''',

        'unfound' : '''No se pudo encontrar el tag con el nombre que has especificado.''',

        'help' : '''Utiliza `{prefix}tag add <nombre>: <mensaje>` para añadir nuevos tags. Utiliza `{prefix}tag remove <nombre>` para eliminar un tag. Utiliza `{prefix}tag <nombre>` para ver un tag. Utiliza `{prefix}tag` para ver todos los tags.'''
    },

    'blacklist' : {
        'removed_from' : '''Removidas las blacklists de los canales especificados.''',

        'added_from' : '''Añadido los canales especificados a la blacklist.''',

        'removed' : '''Removido el canal actual de la blacklist.''',

        'added' : '''Añadido el canal actual a la blacklist.'''

    },

    'lang' : {

        'invalid' : '''Idiomas:
{}''',

        'set' : '''Idioma cambiado a Español.''',
    },

    'clock' : {

        'time' : '''La hora actual es {}.''',
    }

}
