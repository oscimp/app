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
		DTSGenerator(XmlWrapper &xmlWrapper, XmlWrapper &driverWrapper);
		DTSGenerator(std::string xmlFilename, std::string driverFilename);
		~DTSGenerator();
		int generateDTS(std::string outfilename, std::string authorName);
	private:
		XmlWrapper _xmlhandler;
		XmlWrapper _driverhandler;
		std::ofstream outfile;
		std::string rootName;
		std::list<tinyxml2::XMLElement *> drvList;
		int generateNodes();
};
#endif /* DTSGENERATOR_HPP */
