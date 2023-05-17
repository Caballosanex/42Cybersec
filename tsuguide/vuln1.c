#include <stdio.h>
/*
 * Este programa es vulnerable a buffer overflow, ya que no comprueba la longitud del argumento dado y usa la función strcpy que no limita la longitud de caracteres copiados, con lo cual se puede hacer un overflow
*/
int	main (int argc, char **argv)
{
	char buffer[64];
	if (argc < 2)
	{
		printf("Introduzca un argumento al programa\n");
		return 0;
	}
	strcpy (buffer, argv[1]);
	return 0;
}
