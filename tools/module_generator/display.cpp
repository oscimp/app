/*
 * (c) Copyright 2015-2018 	OscillatorIMP Digital
 * Gwenhael Goavec-Merou <gwenhael.goavec-merou@trabucayre.com>
 */

#include <iostream>
#include "display.hpp"

#include <stdio.h>

#define KNRM  "\x1B[0m"
#define KRED  "\x1B[31m"
#define KGRN  "\x1B[32m"
#define KYEL  "\x1B[33m"
#define KBLU  "\x1B[34m"
#define KMAG  "\x1B[35m"
#define KCYN  "\x1B[36m"
#define KWHT  "\x1B[37m"


void printError(std::string err)
{
	printf("%s[ERROR] : %s\e[0m\n", KRED, err.c_str());
}

void printInfo(std::string info)
{
	printf("%s[INFO] : %s\e[0m\n", KBLU, info.c_str());
}
