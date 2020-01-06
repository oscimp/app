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

AppGenerator::AppGenerator(string xmlFilename, string driverFilename,
							string FPGAIPFilename, bool legacy, string board_name):
				_xmlhandler(xmlFilename), _driverhandler(driverFilename),
				_FPGAIPhandler(FPGAIPFilename), _board_name(board_name)
{
	rootName = _xmlhandler.getRoot()->Attribute("name");
	drvList = _xmlhandler.getNodes("driver");
	ipList = _xmlhandler.getNodes("ip");
	_legacy = legacy;
}

AppGenerator::AppGenerator(XmlWrapper &xmlWrapper, XmlWrapper &driverWrapper,
							XmlWrapper &xmlFPGAIPWrapper, bool legacy, string board_name):
				_xmlhandler(xmlWrapper), _driverhandler(driverWrapper),
				_FPGAIPhandler(xmlFPGAIPWrapper), _board_name(board_name)
{
	rootName = _xmlhandler.getRoot()->Attribute("name");
	drvList = _xmlhandler.getNodes("driver");
	ipList = _xmlhandler.getNodes("ip");
	boardDrv = _xmlhandler.getNodes("board_driver");
	_legacy = legacy;
}

AppGenerator::~AppGenerator() {}

int AppGenerator::generateMakefile(string outfilename, string installDir)
{
	string optName;
	string optValue;

	outfile.open(outfilename.c_str());
	outfile << "BASE_NAME=" << rootName << endl;

	/* check and add optional information in the Makefile */
	std::list<tinyxml2::XMLElement *> options_list = _xmlhandler.getNodes("option");
	for (lelem it = options_list.begin(); it != options_list.end(); ++it) {
		optName = (*it)->Attribute("name");
		optValue = (*it)->GetText();
		if (optName.find("FLAGS"))
			outfile << optName << "+=" << optValue << endl;
		else
			outfile << optName << "=" << optValue << endl;
	}

	XMLElement *elem;
	string ipName;
	string drvName;
	outfile << "CORE_MODULES_LIST = \\" << endl;
	for (lelem it = ipList.begin (); it != ipList.end (); ++it){
		ipName = XmlWrapper::getAttributeForElement(*it, "name");
		elem = _FPGAIPhandler.getNodeWithAttributeValue("ip", "name", ipName);
		drvName = XmlWrapper::getAttributeForElement(elem, "driver");
		elem = _driverhandler.getNodeWithAttributeValue("driver", "filename", drvName);
		outfile << "\t${" << DRIVER_DIR << "}/" << elem->Attribute("filename") << "_core/";
		outfile << elem->Attribute("filename") << "_core.ko";
		if (std::next(it) != ipList.end())
			outfile << " \\";
		outfile << endl;
	}
	for (lelem it = drvList.begin (); it != drvList.end (); ++it){
		drvName = XmlWrapper::getAttributeForElement(*it, "name");
		elem = _driverhandler.getNodeWithAttributeValue("driver", "filename", drvName);
		outfile << "\t${" << DRIVER_DIR << "}/" << elem->Attribute("filename") << "_core/";
		outfile << elem->Attribute("filename") << "_core.ko";
		if (std::next(it) != drvList.end())
			outfile << " \\";
		outfile << endl;
	}

	/* include app/Makefile.inc */
	outfile << "include $(" << APP_DIR << ")/Makefile.inc" << endl;
	outfile.close();
	return 0;
}

int AppGenerator::generateScript(string outfilename, string driverPath, bool use_dts)
{
	string childName;
	string drvName;
	string ipName;
	XMLElement *elem;
	outfile.open(outfilename.c_str());
	string bitName(rootName + "_wrapper.bit");

	outfile << "CORE_MODULES_DIR=" << driverPath << endl;
	outfile << "" << std::endl;

	if (_legacy) {
		outfile << "cat ../bitstreams/" << bitName << " > /dev/xdevcfg" << endl;
	} else {
		if (_board_name.compare("plutosdr") != 0) {
			outfile << "mkdir -p /lib/firmware" << std::endl;
			outfile << "cp ../bitstreams/" << bitName << ".bin /lib/firmware" << endl;
		}
		if (!use_dts) {
			outfile << "echo \"" <<  bitName;
			outfile << ".bin\" > /sys/class/fpga_manager/fpga0/firmware "<< endl;
		} else {
			outfile << "DTB_DIR=/sys/kernel/config/device-tree/overlays/fpga"<< endl;
			outfile << "if [ -d $DTB_DIR ]; then" << endl;
			outfile << "\trmdir $DTB_DIR"<< endl;
			outfile << "fi" << endl;
			outfile << "mkdir $DTB_DIR"<< endl;
			outfile << "cat " << rootName << ".dtbo > $DTB_DIR/dtbo"<< endl;
		}
	}
	outfile << "" << std::endl;
	if (!use_dts)
		outfile << "insmod ../modules/board_" << rootName << ".ko" << endl;
	
	/* based on driver structure */
	for (lelem it = drvList.begin (); it != drvList.end (); ++it){
		elem = _driverhandler.getNodeWithAttributeValue("driver", "filename", (*it)->Attribute("name"));
		outfile << "insmod ${CORE_MODULES_DIR}/" << elem->Attribute("filename")<< "_core.ko" << endl;
	}

	/* based on IP structure */
	for (lelem it = ipList.begin (); it != ipList.end (); ++it){
		ipName = XmlWrapper::getAttributeForElement(*it, "name");
		elem = _FPGAIPhandler.getNodeWithAttributeValue("ip", "name", ipName);
		drvName = XmlWrapper::getAttributeForElement(elem, "driver");
		elem = _driverhandler.getNodeWithAttributeValue("driver", "filename", drvName);
		outfile << "insmod ${CORE_MODULES_DIR}/" << elem->Attribute("filename") << "_core.ko" << endl;
	}
	outfile.close();
	chmod(outfilename.c_str(), S_IRWXU | S_IRWXG | S_IRWXO);

	return 0;
}
