#: romanian

{
    'blacklisted' : ''':x: Acest canal este pe lista neagra. :x:''',

    'admin_required' : 'Trebuie sa fi Administrator pentru a folosii aceasta comanda.',

    'help' : '''Viziteaza https://jellywx.co.uk/help?lang=RO''',

    'help_raw' : [
['Reminder Commands', {
'$del' : 'Sterge reaminitriile serverului.',
'$remind [user/channel] <time-to-reminder> <message>' : 'Setează o reamintire. Are timpul în format de [num][s/m/h/d], de exemplu 10s timp de 10 secunde sau 2s10m timp de 2 secunde 10 minute. O oră exactă poate fi dată ca `day`/`month`/`year`-`hour`:`minute`:`second`.',
'$interval [user/channel] <time-to-reminder> <interval> <message>' : 'Seteaza un interval unde `message` o sa fie trimis `interval` începand cu data `time-to-reminder`. Are timp in formatele de mai sus. Ex. `$interval 0s 20m Salutari Tuturor!` o sa trimita `Salutari Tuturor!` in canalul dvs la fiecare 20 de minute.',
'$todo' : 'Lista de activitati.Folositi `$todo help` pentru mai multe informatii.',
'$todos' : 'La fel ca si `$todo` dar pentru gestionarea sarcinilor la nivel de server.',
'$timezone' : 'Setați fusul orar al serverului dvs., pentru mementouri mai ușoare bazate pe date.'
}],

['Management Commands', {
'$autoclear [time/s] [channels]' : 'Activează / dezactivează autoștergerea, unde mesajele trimise canalului (canalul tău implicit) vor fi șterse automat după timp (implicit 10 secunde).',
'$clear <user mentions>' : 'Șterge mesajele făcute de un utilizator / utilizatori.',
'$restrict [role mentions]' : 'Adăugați / eliminați rolurile de la a li se permite să trimită mementouri și intervale de canale.',
'$tag' : 'Comenzi de aliniere. Folositi `$tag help` pentru mai multe informatii.',
'$blacklist [channel-name]' : 'Blocați sau deblocați un canal din trimiterea comenzilor.',
}],

['Other Commands', {
'$donate' : 'Vezi informatii despre donatii.',
'mbprefix <string>' : 'Modificati prefixul din $. Această comandă nu utilizează un prefix!',
'$info' : 'Primeste informatiile botului.',
'$lang <name>' : 'Schimbați limba.',
'$clock' : 'Vedeți cat este ora.'
}]
],

    'web_foot_title' : 'Extra Information',
    'web_foot' : 'Nu introduceți parantezele atunci când tastați comanda! De exemplu, "mbprefix!", Nu `mbprefix <!>`',
    'web_foot2' : 'Vă rugăm să vă alăturați serverului nostru discord dacă aveți nevoie de ajutor suplimentar',

    'about' : {'About' : ['Bot Created By: Jude Southworth', 'Github: <a href=https://github.com/JellyWX>https://github.com/JellyWX</a>', 'Want a bot making? Please contact me on Discord.', 'Hosting provider: OVH']},

    'join' : 'Join our Discord Server',
    'invite' : 'Invite the Bot',

    'info' : '''
Prefixul de baza: `$`
Resetati prefixul: `@{user} prefix $`
Ajutor: `{prefix}help`
**Bun venit la botul RemindMe!**
Developer: <@203532103185465344>
Baiatul de treaba care se pricepe si el: <@174243954487853056>
Icoana: <@253202252821430272>
Ma gasiti si pe https://discord.gg/WQVaYmT cat si pe https://github.com/JellyWX :)

Framework: `discord.py`
Hosting : OVH

Alti boti de ai mei (Patreon doar,):
https://discordapp.com/oauth2/authorize?client_id=411224415863570434&scope=bot&permissions=35840
* Dacă aveți întrebări despre noi caracteristici, vă rugăm să trimiteți la serverul de discordanță *
* Dacă aveți întrebări despre dezvoltarea bot pentru tine sau serverul dvs., vă rugăm sa mi dati un mesaj in privat *''',

    'donate' : '''
Va ganditi la contribuirea lunara? Mai jos aveti niste link-uri!
https://www.patreon.com/jellywx
https://discord.gg/WQVaYmT
Mai multe informatii aici:
Când dați, Patreon vă va clasifica automat pe serverul nostru de discuții, presupunând că ați conectat corect conturile dvs. Patreon și Discord!
Cu noul dvs. rang, veți putea:
: utilizați comenzi numai pentru administratori, cum ar fi `intervalul '
: setați mai multe mementouri (nelimitat)
: setați mementouri mai lungi (2000 caractere)
: setați mai multe / etichete mai lungi

Oricine este patron, vă mulțumesc: D Îl faceți pe bot să fie durabil

Rețineți că trebuie să fiți conectat la serverul Discord pentru a primi recompense Patreon.
''',

    'prefix' : {
        'no_argument' : '''
Utilizați această comandă ca `mbprefix <prefix>`
''',
        'success' : '''
Prefix schimbat in {prefix}
''',

        'too_long' : '''Please select a prefix under 5 characters'''
    },

    'timezone' : {

        'no_argument' : '''
Usage:
    ```{prefix}timezone <Name>```
Example:
    ```{prefix}timezone Europe/London```
All timezones: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
Current timezone: {timezone}''',

        'no_timezone' : '''Fusul orar nu este recunoscut. O listă este disponibilă la https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568''',

        'success' : '''Fusul orar a fost setat la {timezone}. Timpul dvs. curent ar trebui să fie {time}'''
    },

    'restrict' : {

        'disabled' : '''Permisiunile de reamintire a canalelor dezactivate pentru roluri.''',

        'enabled' : '''Permisiuni de memento pentru canale activate pentru roluri.''',

        'allowed' : '''Roluri cu acces: {}'''
    },

    'clear' : {

        'no_argument' : '''Menționați utilizatorii la care doriți să eliminați mesajele.'''

    },

    'remind' : {
        'no_argument' : '''
Usage:
    ```{prefix}remind [channel mention or user mention] <time to or time at> <message>```
Example:
    ```{prefix}remind #general 10s Hello world```
    ```{prefix}remind 10:30 It\'s now 10:30```''',

        'invalid_tag' : '''Nu s-a putut găsi o locație prin eticheta prezentă.''',

        'invalid_time' : '''Asigurați-vă că timpul furnizat este în formatul [num][s/m/h/d][num][s/m/h/d] etc. sau `day/month/year-hour:minute:second`.''',

        'invalid_count' : '''Prea multe mementouri în canalul specificat! Folositi `{prefix}del` pentru a șterge unele dintre ele sau pentru a le utiliza `{prefix}donate` pentru a vă crește maximul (nivelul de 5 $).''',

        'invalid_chars' : '''Mesajul de reamintire este prea lung! (maxim 150, tu ai folosit {}). Foloseste `{prefix}donate` Pentru a creste limita la 1900 caractere (nivelul de 5 $).''',

        'invalid_chars_2000' : '''Restricțiile discordante înseamnă că nu putem trimite mementouri de 2000 de caractere. Scuze.''',

        'no_perms' : '''Trebuie sa ai `Manage Messages` sau au un rol capabil de a trimite mementouri la acel canal. Vă rugăm să discutați cu administratorul serverului dvs. și spuneți-i să utilizeze `{prefix}restrict` comandă pentru a specifica rolurile permise.''',

        'success' : '''Un nou memento înregistrat pentru <{}{}> in {} secunde. Nu poți edita memento-ul acum, deci ai libertatea de a șterge mesajul.'''
    },

    'interval' : {
        'no_argument' : '''
Usage:
    ```{prefix}interval [channel mention or user mention] <time to or time at> <interval> <message>```
Example:
    ```{prefix}interval #general 9:30 1d Good morning!```
    ```{prefix}interval 0s 10s This will be really irritating```''',

        'invalid_interval' : '''Asigurați-vă că intervalul pe care l-ați furnizat este în formatul [num][s/m/h/d][num][s/m/h/d] etc. wfără spații, de ex. 10s pentru 10 secunde sau 10s12m15h1d timp de 10 secunde, 12 minute, 15 ore și 1 zi.''',

        '8_seconds' : '''Asigurați-vă că intervalul de timp este mai lung de 8 secunde.''',

        'donor' : '''Trebuie să fii Patron (care donează 2 $ sau mai mult) pentru a accesa această comandă! Scrie `{prefix}donate` pentru a afla mai multe''',

        'success' : '''Noul interval înregistrat pentru <{}{}> in {} secunde . Nu puteți edita memento-ul acum, deci aveți libertatea de a șterge mesajul.''',

        'removed' : '''Se pare că nu există patroni pe serverul dvs., așa că intervalul a fost eliminat.'''

    },

    'autoclear' : {
        'disable' : '''Auto stergerea dezactivata pentru {}''',

        'enable' : '''{} secunde pana auto stergerea se activeaza.''',
    },

    'del' : {
        'listing' : '''Înregistrați mementouri pe acest server ... (este posibil să existe o mică întârziere, așteptați mesajul "List (1,2,3 ...)").''',

        'listed' : '''Lista (1,2,3 ...) memento-urile pe care doriți să le ștergeți sau tastați altceva pentru a le anula.''',

        'count' : '''Am sers {} reamintirile!'''
    },

    'todo' : {
        'server_only' : '''Folositi `{prefix}todo` pentru lista dvs. de gestionare a sarcinilor `{prefix}todos` este doar pentru utilizarea serverului.''',

        'add' : '''*Folositi `{prefix}{command} adaugati <message>` pentru a adăuga un element la gestionarea sarcinilor, sau scrieti `{prefix}{command} help` pentru mai multe comenzi!*''',

        'too_long' : '''Ne pare rău, dar dimensiunile mesajelor de gestionare a sarcinilor sunt limitate la 80 de caractere. Păstrați-l concis :)''',

        'too_long2' : '''Ne pare rău, dar listele de gestionare a sarcinilor sunt limitate la 800 de caractere. Poate, ai făcut ceva?''',

        'added' : '''Adaugat \'{name}\' in lista de gestionare a sarcinilor!''',

        'removed' : '''Sters \'{}\' din lista de gestionare a sarcinilor!''',

        'error_value' : '''Elementul de îndepărtare trebuie să fie un număr. Vizualizați numerele listelor de gestionare a sarcinilor folosind `{prefix}{command}`''',

        'error_index' : '''Nu s-ar putea găsi elementul prin numărul respectiv. Sunteți în lista corectă a todo?''',

        'help' : '''Pentru a folosii lista de gestionare a sarcinilor, folositi `{prefix}{command} adaugati <message>`, `{prefix}{command} sterge <number>`, `{prefix}{command} clear` si `{prefix}{command}` pentru a adauga, sterge din lista, caflați sau vizualizați lista dvs. de mandate.''',

        'cleared' : '''Lista de gestionare a sarcinilor a fost stearsa.'''
    },

    'tags' : {

        'deleted' : '''Etichetă ștersă {}''',

        'added' : '''Etichetă adăugată {}''',

        'invalid_count' : '''Ne pare rău, dar pentru utilizatorii normali etichetele sunt limitate la 6. Vă rugăm să eliminați unele sau să luați în considerare donarea cu `{prefix}donate` (5$ tier).''',

        'invalid_chars' : '''Etichetele sunt limitate la 80 de caractere. Păstrați-l concis!''',

        'colon' : '''Adăugați un colon pentru a împărți numele etichetei din corp.''',

        'illegal' : '''Nu folosiți cuvinte cheie "adăugați, noi, eliminați" în numele etichetelor.''',

        'unfound' : '''Nu am putut găsi eticheta după numele pe care l-ați specificat.''',

        'help' : '''Utilizați `{prefix}tag add <name>: <message>` pentru a adăuga etichete noi. Utilizați "{prefix}tag remove <nume> pentru a șterge o etichetă. Utilizați `{prefix}tag <nume>` pentru a vedea o etichetă. Utilizați `{prefix}tag` pentru a lista toate etichetele'''
    },

    'blacklist' : {
        'removed_from' : '''Eliminați lista negra de pe canalele specificate.''',

        'added_from' : '''Adăugat canalele specificate pe lista neagră.''',

        'removed' : '''Eliminat canalul curent din lista neagră.''',

        'added' : '''Adăugat canalul actual la lista neagră.'''

    },

    'lang' : {

        'invalid' : '''Limbi:
{}''',

        'set' : '''Limba a fost setata in Română.''',
    },

    'clock' : {
        'time' : '''Ora este: {}.''',
    }

}
