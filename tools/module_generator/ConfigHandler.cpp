/*
 * (c) Copyright 2015-2018 	OscillatorIMP Digital
 * Gwenhael Goavec-Merou <gwenhael.goavec-merou@trabucayre.com>
 */

#include <iostream>
#include <fstream>
#include <tinyxml2.h>

#include "XmlWrapper.hpp"
#include "ConfigHandler.hpp"
using namespace tinyxml2;
using namespace std;

ConfigHandler::ConfigHandler(string xmlFilename)
{
	try {
		xmlhandler = new XmlWrapper(xmlFilename, true);
	} catch (exception &exec) {
		xmlhandler = new XmlWrapper();
		xmlhandler->setFileName(xmlFilename);
		xmlhandler->setRoot("MGConfig");
		xmlhandler->writeFile();
	}
	suppressXml = true;
}

ConfigHandler::ConfigHandler(XmlWrapper *xmlWrapper)
{
	xmlhandler = xmlWrapper;
	suppressXml = false;
}

ConfigHandler::~ConfigHandler()
{
	if (suppressXml)
		delete xmlhandler;
}

string ConfigHandler::getText(string nodeName, string defaultValue="")
{
	XMLElement *node = xmlhandler->getNode(nodeName);
	if (!node) {
		node = xmlhandler->addNode(nodeName);
	}

	string content = xmlhandler->getText(node);
	if (""==content && defaultValue != "") {
		cerr << "node " << nodeName << " empty : use default value " << endl;
		xmlhandler->setText(node, defaultValue);
		content = defaultValue;
	}
	return content;
}

string ConfigHandler::getNfsInstallDir()
{
	return getText("nfsInstallDir");
}
string ConfigHandler::getDriverPath()
{
	return getText("driverPath", "/usr/local/modules");
}
string ConfigHandler::getAuthor()
{
	return getText("author", "toto <toto@toto.com>");
}
