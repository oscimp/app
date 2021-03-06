/*
 * (c) Copyright 2015-2018 	OscillatorIMP Digital
 * Gwenhael Goavec-Merou <gwenhael.goavec-merou@trabucayre.com>
 */

#include <iostream>
#include <fstream>
#include <tinyxml2.h>

#include "XmlWrapper.hpp"
#include "DTSGenerator.hpp"
#include "common.h"
#include "display.hpp"
using namespace tinyxml2;
using namespace std;

typedef list<XMLElement*>::iterator lelem;

DTSGenerator::DTSGenerator(string xmlFilename, string driverFilename, string FPGAIPFilename,
	string board_name):
	_xmlhandler(xmlFilename), _driverhandler(driverFilename), _FPGAIPhandler(FPGAIPFilename),
	_board_name(board_name), _tool("vivado")
{
	rootName = _xmlhandler.getRoot()->Attribute("name");
	drvList = _xmlhandler.getNodes("driver");
	ipList = _xmlhandler.getNodes("ip");
	try {
		string tool = _xmlhandler.getAttributeForElement(_xmlhandler.getRoot(), "tool", true);
		_tool = std::move(tool);
	} catch (const std::invalid_argument &e) {} // by default use "vivado"
}

DTSGenerator::DTSGenerator(XmlWrapper &xmlWrapper, XmlWrapper &driverWrapper, XmlWrapper &FPGAIPWrapper,
	string board_name):
	_xmlhandler(xmlWrapper), _driverhandler(driverWrapper), _FPGAIPhandler(FPGAIPWrapper),
	_board_name(board_name), _tool("vivado")
{
	rootName = _xmlhandler.getRoot()->Attribute("name");
	drvList = _xmlhandler.getNodes("driver");
	ipList = _xmlhandler.getNodes("ip");
	try {
		string tool = _xmlhandler.getAttributeForElement(_xmlhandler.getRoot(), "tool", true);
		_tool = std::move(tool);
	} catch (const std::invalid_argument &e) {} // by default use "vivado"
}

DTSGenerator::~DTSGenerator(){}

int DTSGenerator::generateNode(std::string drvName, XMLElement *child)
{
	XMLElement *elem;
	string driverName, childName, base_addr, addr_size, cut_addr;
	string compatible;

	elem = _driverhandler.getNodeWithAttributeValue("driver", "filename", drvName);
	if (elem == NULL) {
		printError("No driver with filename : " + drvName);
		return EXIT_FAILURE;
	}
	try {
		driverName = XmlWrapper::getAttributeForElement(elem, "name");
		compatible = XmlWrapper::getAttributeForElement(elem, "compatible");
	} catch (const std::exception &e) {
		printError("attribute problem with driver " + drvName
					+ " : " + e.what());
		return EXIT_FAILURE;
	}

	for (int i=0; child; child = child->NextSiblingElement(), i++) {
		try {
			childName = XmlWrapper::getAttributeForElement(child, "name");
			base_addr = XmlWrapper::getAttributeForElement(child, "base_addr");
			addr_size = XmlWrapper::getAttributeForElement(child, "addr_size");
		} catch (const std::exception &e) {
			printError("attribute problem for " + drvName +
						" subnode : " +e.what());
			return EXIT_FAILURE;
		}

		if (childName.empty()) {
			printError("Error: empty instance name");
			return EXIT_FAILURE;
		}

		if (base_addr.empty()) {
			printError("Error: missing base addr for " + childName);
			return EXIT_FAILURE;
		}

		if (addr_size.empty()) {
			printError("Error: missing addr size for " + childName);
			return EXIT_FAILURE;
		}

		cut_addr = base_addr.substr(2);
		outfile << "\t\t\t" << childName << ": " << childName << "@" << cut_addr << "{" << std::endl;
		outfile << "\t\t\t\tcompatible = \"" << compatible << "\";" << std::endl;
		outfile << "\t\t\t\treg = <" << base_addr << " "<< addr_size << ">;" << std::endl;
		outfile << "\t\t\t};" << std::endl;
		outfile << "" << std::endl;
	}
	return 0;
}

int DTSGenerator::generateNewNodes()
{
	XMLElement *ip, /**drv,*/ *child, *elem;
	string driverName, childName, base_addr, addr_size, cut_addr;
	string compatible, drvName, ipName;

	for (lelem it = ipList.begin (); it != ipList.end (); ++it){
		ip = *it;
		/* search for ip name */
		try {
			ipName = XmlWrapper::getAttributeForElement(ip, "name");
		} catch (const exception &e) {
			printError("Node has no ip name attribute.");
			return EXIT_FAILURE;
		}
		/* search for corresponding node in fpga_ip/driver.xml */
		elem = _FPGAIPhandler.getNodeWithAttributeValue("ip", "name", ipName);
		if (elem == NULL) {
			printError("No IP with name : " + ipName);
			return EXIT_FAILURE;
		}
		try {
			drvName = XmlWrapper::getAttributeForElement(elem, "driver");
		} catch (const std::exception &e) {
			printError("attribute problem with IP " + drvName
						+ " : " + e.what());
			return EXIT_FAILURE;
		}

		child = ip->FirstChildElement("instance");
		generateNode(drvName, child);
	}
	return 0;
}

int DTSGenerator::generateNodes()
{
	XMLElement *drv, *child/*, *elem*/;
	string driverName, childName, base_addr, addr_size, cut_addr;
	string compatible, drvName;

	for (lelem it = drvList.begin (); it != drvList.end (); ++it){
		drv = *it;
		try {
			drvName = XmlWrapper::getAttributeForElement(drv, "name");
		} catch (const exception &e) {
			printError("Node has no driver name attribute.");
			return EXIT_FAILURE;
		}

		child = drv->FirstChildElement("board_driver");
		generateNode(drvName, child);
	}
	return 0;
}

int DTSGenerator::generateDTS(string outfilename)
{
	int ret = 0;
	string target_phandle;
	bool is_pluto = false;

	if (!_board_name.compare("plutosdr"))
		is_pluto = true;

	outfile.open(outfilename.c_str());

	outfile << "/dts-v1/;" << std::endl;
	outfile << "/plugin/;" << std::endl;
	outfile << "" << std::endl;
	outfile << "/ {" << std::endl;
	if (_tool == "quartus") {
		outfile << "\tcompatible = \"altr,socfpga-cyclone5\", \"altr,socfpga\";" << std::endl;
	} else {
		outfile << "\tcompatible = \"xlnx,zynq-7000\";" << std::endl;
	}
	outfile << "" << std::endl;
    outfile << "\tfragment0 {" << std::endl;
	if (_tool == "quartus") {
		outfile << "\t\ttarget = <&base_fpga_region>;" << std::endl;
	} else {
		outfile << "\t\ttarget = <&" << ((is_pluto) ? "fpga_axi" : "fpga_full") << ">;" << std::endl;
	}
    outfile << "\t\t__overlay__ {" << std::endl;
    outfile << "\t\t\t#address-cells = <1>;" << std::endl;
    outfile << "\t\t\t#size-cells = <1>;" << std::endl;
	outfile << "" << std::endl;
	if (_tool == "quartus") {
		outfile << "\t\t\tfirmware-name = \"" << rootName << ".rbf\";" << std::endl;
		outfile << "\t\t\tfpga-bridges = <&fpga_bridge0>, <&fpga_bridge1>;" << std::endl;
		outfile << "" << std::endl;
		outfile << "\t\t\tranges = <0x00000 0xff200000 0x100000>;" << std::endl;
		outfile << "" << std::endl;
	} else {
		if (!is_pluto) {
			outfile << "\t\t\tfirmware-name = \"" << rootName << "_wrapper.bit.bin\";" << std::endl;
			outfile << "" << std::endl;
		}
	}

	ret = generateNodes();
	ret |= generateNewNodes();
	if (ret != 0) {
		ret = -1;
		goto end;
	}

	outfile << "\t\t};" << std::endl;
	outfile << "\t};" << std::endl;
	outfile << "};" << std::endl;
end:
	outfile.close();
	return ret;
}
