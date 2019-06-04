/*
 * (c) Copyright 2015-2018 	OscillatorIMP Digital
 * Gwenhael Goavec-Merou <gwenhael.goavec-merou@trabucayre.com>
 */

#include <tinyxml2.h>
#include <stdlib.h>
#include <iostream>
#include <sys/stat.h>

#include "XmlWrapper.hpp"
#include "DTSGenerator.hpp"
#include "DriverGenerator.hpp"
#include "AppGenerator.hpp"
#include "ConfigHandler.hpp"
#include "directoryHandler.hpp"
#include "common.h"
#include "display.hpp"
#include <errno.h>

using namespace tinyxml2;
using namespace std;


void printUsage(string appname)
{
	printError("missing xml name");
	printInfo("USAGE: " + appname + "[-dts] [-nodts] [-legacy] file.xml");
	printInfo("\tlegacy : (only with -nodts) use this option to flash FPGA with xdevcfg");
	printInfo("\t dts : (default option) generate a dts file instead of board driver");
	printInfo("\t -nodts : generate board driver instead of dts file");
}

int main(int argc, char **argv)
{
	bool legacy = false, use_dts = true;
	string xmlFile;
	string configName = string(getenv("HOME")) + "/.modulegenrc";

	ConfigHandler cfhandl(configName);

	if (argc < 2 || argc > 4) {
		printUsage(string(argv[0]));
		return EXIT_FAILURE;
	}

	if (argc == 2) {
		xmlFile = string(argv[1]);
	} else {
		xmlFile = string(argv[2]);
		if (!strcmp(argv[1], "-nodts")) {
			use_dts = false;
			if (!strcmp(argv[2], "-legacy")) {
				legacy = true;
				xmlFile = string(argv[3]);
			}
		} else if (!strcmp(argv[1], "-dts")) {
			use_dts = true;
		} else {
			printUsage(string(argv[0]));
			return EXIT_FAILURE;
		}
	}

	string fpga_driver_dir;
	try {
		fpga_driver_dir = string(getenv(DRIVER_DIR.c_str()));
	} catch (exception &exec) {
		printError("Erreur: env var " + DRIVER_DIR + " not defined");
		return EXIT_FAILURE;
	}

	string fpga_ip_dir;
	try {
		fpga_ip_dir = string(getenv(FPGA_IP_DIR.c_str()));
	} catch (exception &exec) {
		printError("Erreur: env var " + FPGA_IP_DIR + " not defined");
		return EXIT_FAILURE;
	}

	string board_name;
	try {
		board_name = string(getenv(BOARD_NAME.c_str()));
	} catch (exception &exec) {
		printError("Erreur: env var " + BOARD_NAME + " not defined");
		return EXIT_FAILURE;
	}

	XmlWrapper xmlWrapper;
	try {
		xmlWrapper.loadFile(xmlFile);
	} catch (exception &exec) {
		return EXIT_FAILURE;
	}

	XmlWrapper xmlDriverWrapper;
	try {
		xmlDriverWrapper.loadFile(fpga_driver_dir+"/driver.xml");
	} catch (exception &exec) {
		return EXIT_FAILURE;
	}

	XmlWrapper xmlFPGAIPWrapper;
	try {
		xmlFPGAIPWrapper.loadFile(fpga_ip_dir+"/ip.xml");
	} catch (exception &exec) {
		return EXIT_FAILURE;
	}

	DTSGenerator dtsGen(xmlWrapper, xmlDriverWrapper, xmlFPGAIPWrapper, board_name);
	DriverGenerator drvGen(&xmlWrapper, &xmlDriverWrapper, false);

	AppGenerator appGen(xmlWrapper, xmlDriverWrapper, xmlFPGAIPWrapper, legacy, board_name);

	string rootName(xmlWrapper.getRoot()->Attribute("name"));
	string appDir("app");

	string moduleDir("modules");

	/* Makefile generation */
	if (use_dts == false) {
		if (-1 == mkpath(moduleDir.c_str(), S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH)) {
			printError("Error creating directory " + moduleDir + "!");
			return EXIT_FAILURE;
		}
	}
	if (-1 == mkpath(appDir.c_str(), S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH)) {
		printError("Error creating directory " + appDir + "!");
		return EXIT_FAILURE;
	}

	if (use_dts == true) {
		char dtsName[128];
		sprintf(dtsName, "%s.dts", rootName.c_str());
		if (0 != dtsGen.generateDTS(appDir + "/"+dtsName))
			goto end;
	} else {
		char driverName[128];
		sprintf(driverName, "board_%s.c", rootName.c_str());
		if (0 != drvGen.generateBoardDriver(moduleDir+"/"+driverName, cfhandl.getAuthor()))
			goto end;
		if (0 != drvGen.generateMakefile(moduleDir+"/Makefile", cfhandl.getNfsInstallDir()))
			goto end;
	}

	cout << "etape 2" << endl;
	if (0 != appGen.generateMakefile(appDir+"/Makefile", cfhandl.getNfsInstallDir()))
		goto end;
	if (0 != appGen.generateScript(appDir+"/"+rootName+"_us.sh", "../../modules", use_dts))
		goto end;
	printInfo("Generation successfully");
end:
	std::cout << "end" << std::endl;
}
