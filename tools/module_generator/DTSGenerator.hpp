/*
 * (c) Copyright 2015-2018 	OscillatorIMP Digital
 * Gwenhael Goavec-Merou <gwenhael.goavec-merou@trabucayre.com>
 */

#ifndef DTSGENERATOR_HPP
#define DTSGENERATOR_HPP

#include <iostream>
#include <fstream>
#include "XmlWrapper.hpp"

class DTSGenerator
{
	public:
		DTSGenerator(XmlWrapper &xmlWrapper, XmlWrapper &driverWrapper,
			XmlWrapper &xmlFPGAWrapper);
		DTSGenerator(std::string xmlFilename, std::string driverFilename,
			std::string FPGAIPFilename);
		~DTSGenerator();
		int generateDTS(std::string outfilename, std::string authorName);
	private:
		XmlWrapper _xmlhandler;
		XmlWrapper _driverhandler;
		XmlWrapper _FPGAIPhandler;
		std::ofstream outfile;
		std::string rootName;
		std::list<tinyxml2::XMLElement *> drvList;
		std::list<tinyxml2::XMLElement *> ipList;
		int generateNodes();
		int generateNode(std::string drvName, tinyxml2::XMLElement *child);
		int generateNewNodes();
};
#endif /* DTSGENERATOR_HPP */
