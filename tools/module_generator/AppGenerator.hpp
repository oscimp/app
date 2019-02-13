/*
 * (c) Copyright 2015-2018 	OscillatorIMP Digital
 * Gwenhael Goavec-Merou <gwenhael.goavec-merou@trabucayre.com>
 */

#ifndef APPGENERATOR_HPP
#define APPGENERATOR_HPP

#include <iostream>
#include <fstream>
#include "XmlWrapper.hpp"

class AppGenerator
{
	public:
		AppGenerator(XmlWrapper &xmlWrapper, XmlWrapper &driverWrapper,
			XmlWrapper &xmlFPGAWrapper, bool legacy);
		AppGenerator(std::string xmlFilename, std::string driverFilename,
			std::string FPGAIPFilename, bool legacy);
		~AppGenerator();
		int generateMakefile(std::string outfilename, std::string installDir);
		int generateScript(std::string outfilename, std::string driverPath, bool use_dts);
	private:
		XmlWrapper _xmlhandler;
		XmlWrapper _driverhandler;
		XmlWrapper _FPGAIPhandler;
		std::ofstream outfile;
		std::string rootName;
		bool _legacy;
		std::list<tinyxml2::XMLElement *> drvList;
		std::list<tinyxml2::XMLElement *> ipList;
		std::list<tinyxml2::XMLElement *> boardDrv;
};
#endif /* APPGENERATOR_HPP */
