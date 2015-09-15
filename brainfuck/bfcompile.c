#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#define PATH_MAX_SIZE 256
//#define DEBUG

int main(int argc, char** argv)
{
	FILE *fin, *fout;
	char fnout[PATH_MAX_SIZE] = {0};
	char c;
	int indent_level=0, i;
	char cmd[PATH_MAX_SIZE] = "make ";

	if (argc < 2)
	{
		fprintf(stderr, "Usage: %s <file.bf>\n", argv[0]);
		exit(1);
	}

	fin = fopen(argv[1], "r");

	if (fin==NULL)
	{
		fprintf(stderr, "Cannot open input file '%s'\n", argv[1]);
		exit(2);
	}

#ifdef DEBUG
	printf("Input file '%s' opened\n", argv[1]);
#endif

	strncpy(fnout, argv[1], PATH_MAX_SIZE);
	strncat(fnout, "_run.c", PATH_MAX_SIZE);
	fout = fopen(fnout, "w");
	
	if (fout==NULL)
	{
		fprintf(stderr, "Cannot open output file '%s'\n", argv[1]);
		exit(2);
	}

#ifdef DEBUG
	printf("Ouput file '%s' opened\n", fnout);
#endif

	fputs("#include <stdio.h>\n", fout);
	fputs("#include <stdlib.h>\n\n", fout);
	fputs("int main() {\n\n", fout);
	fputs("\tchar cells[256] = {0};\n", fout);
	fputs("\tchar tmp;\n", fout);
	fputs("\tchar pnt=0;\n\n", fout);

	while((c=getc(fin))!=EOF)
	{
		if(c==']')
		{
			if(!indent_level)
				fputs("Unbalanced brackets !\n", stderr);
			indent_level--;
		}

		for(i=0; i<indent_level; i++)
			putc('\t', fout);

		switch(c)
		{
			case '+':
				fputs("\tcells[pnt]++;\n", fout);
				break;

			case '-':
				fputs("\tcells[pnt]--;\n", fout);
				break;

			case '>':
				fputs("\tpnt++;\n", fout);
				break;

			case '<':
				fputs("\tpnt--;\n", fout);
				break;

			case ',':
				fputs("\ttmp = getc(stdin); cells[pnt] = tmp==EOF ? 0 : tmp;\n", fout);
				break;

			case '.':
				fputs("\tputc(cells[pnt], stdout);\n", fout);
				break;

			case '[':
				fputs("\twhile (cells[pnt]) {\n", fout);
				indent_level++;
				break;

			case ']':
				fputs("\t}\n", fout);
				break;

			default:
				continue;
		}
	}

	fputs("\n\treturn EXIT_SUCCESS;\n", fout);
	fputs("}", fout);

	fclose(fin);
	fclose(fout);

	strncat(cmd, argv[1], PATH_MAX_SIZE);
	strncat(cmd, "_run", PATH_MAX_SIZE);

#ifdef DEBUG
	printf("Running '%s'\n", cmd);
#endif

	system(cmd);

#ifndef DEBUG
	bzero(cmd, PATH_MAX_SIZE);
	strncat(cmd, "rm ", PATH_MAX_SIZE);
	strncat(cmd, argv[1], PATH_MAX_SIZE);
	strncat(cmd, "_run.c", PATH_MAX_SIZE);

	system(cmd);
#endif

	return EXIT_SUCCESS;
}
