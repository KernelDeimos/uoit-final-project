#include <stdio.h>
#include "Python.h"

int main()
{
	PyObject* pInt;

	Py_Initialize();

	PyRun_SimpleString("print('This is Python in C')");

	Py_Finalize();

	printf("\n");
	return 0;
}
