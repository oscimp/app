/*
 * (c) Copyright 2015-2018 	OscillatorIMP Digital
 * Gwenhael Goavec-Merou <gwenhael.goavec-merou@trabucayre.com>
 */

#ifndef CONFIGHANDLER_HPP
#define CONFIGHANDLER_HPP

#include <iostream>
#include <fstream>
#include "XmlWrapper.hpp"

class ConfigHandler
{
	public:
		ConfigHandler(XmlWrapper *xmlWrapper);
		ConfigHandler(std::string xmlFilename);
		~ConfigHandler();
		std::string getAuthor();
		std::string getDriverPath();
		std::string getNfsInstallDir();
	private:
		std::string getText(std::string NodeName,
			std::string defaultValue);
		void generateEmptyConfig();
		XmlWrapper *xmlhandler;
		bool suppressXml;
};
#endif /* CONFIGHANDLER_HPP */
