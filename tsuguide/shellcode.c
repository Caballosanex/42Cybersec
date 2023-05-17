#include <stdio.h>
#include <windows.h>

/*
 * Este código está hecho en ensamblador, en él cargamos las librerías stdio.h y windows.h.
 * Podemos ver dos partes en el código, en la primera parte estamos cargando la librería "msvcrt.dll" y en la segunda ejecutamos "calc.exe"
 * 
 * La segunda dirección de memoria se consigue usando el offset.c, al que le daremos como parametros la librería y la función que buscamos
 * La primera dirección es donde se localiza LoadLibrary en Windows XP SP3, se puede encontrar en internet o ejecutando offset.exe kernel32.dll LoadLibraryA
 * Al ejecutar el offset.exe (lo conseguimos haciendo el comando "cl" al offset.c) y darle los parametros "msvcrt.dll" system conseguiremos la segunda dirección de memoria, que es el offset necesario para ejecutar programas con la función system
 * Básicamente la primera parte carga la librería msvcrt.dll y la segunda ejecuta la calculadora, estos dos archivos están escritos en hexadecimal en las lineas de mov byte y el sub esp se utiliza para darles hueco a los bytes necesarios para escribirlo
 * el xor se utiliza en este caso para crear un valor 0 que se usará como fin de linea
 * */
int main()
{
	_asm
	{
		push ebp
		mov ebp,esp
		xor edi,edi
		push edi
		sub esp,0ch
		mov byte ptr [ebp-0bh],6dh
		mov byte ptr [ebp-0ah],73h
		mov byte ptr [ebp-09h],76h
		mov byte ptr [ebp-08h],63h
        mov byte ptr [ebp-07h],72h
        mov byte ptr [ebp-06h],74h
        mov byte ptr [ebp-05h],2Eh
        mov byte ptr [ebp-04h],64h
        mov byte ptr [ebp-03h],6ch
		mov byte ptr [ebp-02h],6ch
		lea eax,[ebp-0bh]
		push eax
		mov ebx,0x7c801d7b
		call ebx
		
		push ebp
		mov ebp,esp
		xor edi,edi
		push edi
		sub esp,08h
		mov byte ptr [ebp-09h],63h
		mov byte ptr [ebp-08h],61h
        mov byte ptr [ebp-07h],6Ch
        mov byte ptr [ebp-06h],63h
        mov byte ptr [ebp-05h],2Eh
        mov byte ptr [ebp-04h],65b
        mov byte ptr [ebp-03h],78h
		mov byte ptr [ebp-02h],65h
		lea eax,[ebp-09h]
		push eax
		mov ebx,0x77c293c7
		call ebx
	}

}
