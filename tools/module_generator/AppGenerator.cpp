/*
 * (c) Copyright 2015-2018 	OscillatorIMP Digital
 * Gwenhael Goavec-Merou <gwenhael.goavec-merou@trabucayre.com>
 */

#include <iostream>
#include <fstream>
#include <tinyxml2.h>
#include <sys/stat.h>

#include "XmlWrapper.hpp"
#include "AppGenerator.hpp"
#include "common.h"

using namespace tinyxml2;
using namespace std;

typedef list<XMLElement*>::iterator lelem;

AppGenerator::AppGenerator(string xmlFilename, string driverFilename, bool legacy)
{
	xmlhandler = new XmlWrapper(xmlFilename);
	driverhandler = new XmlWrapper(driverFilename);

	rootName = xmlhandler->getRoot()->Attribute("name");
	drvList = xmlhandler->getNodes("driver");
	suppressXml = true;
	_legacy = legacy;
}

AppGenerator::AppGenerator(XmlWrapper *xmlWrapper, XmlWrapper *driverWrapper, bool legacy)
{
	xmlhandler = xmlWrapper;
	driverhandler = driverWrapper;
	rootName = xmlhandler->getRoot()->Attribute("name");
	drvList = xmlhandler->getNodes("driver");
	boardDrv = xmlhandler->getNodes("board_driver");
	suppressXml = false;
	_legacy = legacy;
}

AppGenerator::~AppGenerator()
{
	if (suppressXml){
		delete xmlhandler;
		delete driverhandler;
	}
}

int AppGenerator::generateMakefile(string outfilename, string installDir)
{
	string boardName;

	outfile.open(outfilename.c_str());
	outfile << "BASE_NAME=" << rootName << endl;

	if (xmlhandler->getRoot()->Attribute("board")) {
		boardName = xmlhandler->getRoot()->Attribute("board");
		outfile << "BOARD_NAME=" << boardName << endl;
	}
	outfile << "include $(" << APP_DIR << ")/Makefile.inc" << endl;
	outfile.close();
	return 0;
}

int AppGenerator::generateScript(string outfilename, string driverPath, bool use_dts)
{
	string childName;
	XMLElement *elem;
	outfile.open(outfilename.c_str());
	string bitName(rootName + "_wrapper.bit");

	outfile << "CORE_MODULES_DIR=" << driverPath << endl;
	outfile << "" << std::endl;

	if (_legacy) {
		outfile << "cat ../bitstreams/" << bitName << " > /dev/xdevcfg" << endl;
	} else {
		outfile << "mkdir -p /lib/firmware" << std::endl;
		outfile << "cp ../bitstreams/" << bitName << ".bin /lib/firmware" << endl;
		if (!use_dts) {
			outfile << "echo \"" <<  bitName;
			outfile << ".bin\" > /sys/class/fpga_manager/fpga0/firmware "<< endl;
		} else {
			outfile << "DTB_DIR=/sys/kernel/config/device-tree/overlays/fpga"<< endl;
			outfile << "rmdir $DTB_DIR"<< endl;
			outfile << "mkdir $DTB_DIR"<< endl;
			outfile << "cat " << rootName << ".dtbo > $DTB_DIR/dtbo"<< endl;

		}
	}
	outfile << "" << std::endl;
	if (!use_dts)
		outfile << "insmod ../modules/board_" << rootName << ".ko" << endl;
	
	for (lelem it = drvList.begin (); it != drvList.end (); ++it){
		elem = driverhandler->getNodeWithAttributeValue("driver", "filename", (*it)->Attribute("name"));
		childName = elem->Attribute("filename");
		outfile << "insmod ${CORE_MODULES_DIR}/" << childName << "_core.ko" << endl;
	}
	outfile.close();
	chmod(outfilename.c_str(), S_IRWXU | S_IRWXG | S_IRWXO);

	return 0;
}
