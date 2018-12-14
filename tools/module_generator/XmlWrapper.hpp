/*
 * (c) Copyright 2015-2018 	OscillatorIMP Digital
 * Gwenhael Goavec-Merou <gwenhael.goavec-merou@trabucayre.com>
 */

#ifndef XMLWRAPPER_HPP
#define XMLWRAPPER_HPP

#include <iostream>
#include <list>
#include <tinyxml2.h>
using namespace std;

class XmlWrapper
{
	private:
		std::string xmlFileName;
	public:
		XmlWrapper();
		XmlWrapper(const XmlWrapper &xmlWrapp);
		XmlWrapper(std::string, bool createIfFail=false);
		~XmlWrapper();
		void loadFile(string filename, bool createIfFail = false);
		void writeFile();
		inline std::string getFileName() {return xmlFileName;}
		inline void setFileName(std::string filename) {xmlFileName = filename;}
		static std::string getAttributeForElement(tinyxml2::XMLElement *element,
				std::string attribute, bool useException = true);
		tinyxml2::XMLDocument *getXMLDoc() {return &xmlDoc;}
		tinyxml2::XMLElement *getRoot();
		void setRoot(std::string nodeName);
		tinyxml2::XMLElement *addNode(std::string nodeName);
		void addAttribute(tinyxml2::XMLElement *node, std::string attributeName,
							std::string attributeValue);
		void setText(tinyxml2::XMLElement *node, std::string content);
		inline std::string getText(tinyxml2::XMLElement *node){
			const char *content = node->GetText();
			if (!content)
				return "";
			else
				return string(node->GetText());
			}

		tinyxml2::XMLElement *getNode(std::string nodename);
		std::list<tinyxml2::XMLElement *> getNodes(std::string nodename);
		std::list<tinyxml2::XMLElement *> getNodes(std::string nodename,
										tinyxml2::XMLElement *current);
		std::list<std::string> *getAttributeForNodes(std::string nodename,
										std::string attributename);

		tinyxml2::XMLElement *getNodeWithAttributeValue(std::string nodename,
										std::string attribute, std::string value);
	private:
		bool needSave;
		tinyxml2::XMLDocument xmlDoc;
		tinyxml2::XMLElement *xmlRoot;
};
#endif /* XMLWRAPPER_HPP */
