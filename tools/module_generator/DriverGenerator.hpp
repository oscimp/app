/*
 * (c) Copyright 2015-2018 	OscillatorIMP Digital
 * Gwenhael Goavec-Merou <gwenhael.goavec-merou@trabucayre.com>
 */

#ifndef DRIVERGENERATOR_HPP
#define DRIVERGENERATOR_HPP

#include <iostream>
#include <fstream>
#include "XmlWrapper.hpp"

class DriverGenerator
{
	public:
		DriverGenerator(XmlWrapper *xmlWrapper, XmlWrapper *driverWrapper, bool ng=false);
		DriverGenerator(std::string xmlFilename, std::string driverFilename, bool ng=false);
		~DriverGenerator();
		int generateBoardDriver(std::string outfilename, std::string authorName);
		int generateMakefile(std::string outfilename, std::string installDir);
	private:
		XmlWrapper *xmlhandler;
		XmlWrapper *driverhandler;
		std::ofstream outfile;
		std::string rootName;
		bool suppressXml;
		bool _ng;
		std::list<tinyxml2::XMLElement *> drvList;
		std::list<tinyxml2::XMLElement *> boardDrv;

		int generateInclude();
		int generateMacro();
		int generateResource();
		int generatePlatformData();
		int generatePlatformDevice();
		int generateInitExit(string authorName);
};
#endif /* DRIVERGENERATOR_HPP */
