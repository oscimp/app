/*
 * (c) Copyright 2015-2018 	OscillatorIMP Digital
 * Gwenhael Goavec-Merou <gwenhael.goavec-merou@trabucayre.com>
 */

#ifndef DIRECTORY_HANDLER_H
#define DIRECTORY_HANDLER_H

int do_mkdir(const char *path, mode_t mode);
int mkpath(const char *path, mode_t mode);

#endif /*DIRECTORY_HANDLER_H*/
