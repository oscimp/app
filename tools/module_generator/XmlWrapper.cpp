/*
 * (c) Copyright 2015-2018 	OscillatorIMP Digital
 * Gwenhael Goavec-Merou <gwenhael.goavec-merou@trabucayre.com>
 */

#include <iostream>
#include <list>
#include <tinyxml2.h>
#include "XmlWrapper.hpp"
#include "display.hpp"

using namespace tinyxml2;
using namespace std;

XmlWrapper::XmlWrapper():
	xmlFileName(),
	needSave(false),
	xmlDoc() {}

XmlWrapper::XmlWrapper(const XmlWrapper &xmlWrapp):
	xmlFileName(xmlWrapp.xmlFileName),
	needSave(false),xmlDoc()
{
	xmlDoc.LoadFile(xmlFileName.c_str());
	xmlRoot = xmlDoc.FirstChildElement();
}

XmlWrapper::XmlWrapper(string filename, bool createIfFail)
	:xmlFileName(filename), needSave(false), xmlDoc()
{
	loadFile(filename, createIfFail);
}

XmlWrapper::~XmlWrapper()
{
	if (needSave)
		writeFile();
}

void XmlWrapper::loadFile(string filename, bool createIfFail)
{
	xmlFileName = filename;
	if (xmlDoc.LoadFile(filename.c_str()) != 0) {
		if (createIfFail==false) {
			printError("erreur de chargement #" + std::to_string((int)xmlDoc.ErrorID()) + " : " +
						xmlDoc.ErrorName());
			printError(xmlDoc.ErrorStr());
		}
		throw std::exception();
	}
	xmlRoot = xmlDoc.FirstChildElement();
}


XMLElement *XmlWrapper::getRoot()
{
	return xmlRoot;
}

void XmlWrapper::writeFile()
{
	if (xmlFileName == "")
		throw std::exception();
	
	xmlDoc.SaveFile(xmlFileName.c_str());
	needSave = false;
}

void XmlWrapper::setRoot(string nodeName)
{
	xmlRoot = xmlDoc.NewElement(nodeName.c_str());
	xmlDoc.InsertFirstChild(xmlRoot);
	needSave = true;
}

std::string XmlWrapper::getAttributeForElement(XMLElement *element,
		std::string attribute, bool useException) {
	if (element->Attribute(attribute.c_str()))
		return std::string(element->Attribute(attribute.c_str()));
	else {
		if (useException == true) {
		throw std::invalid_argument("Node as no attribute with name : " +
										std::string(attribute));

		} else
			return NULL;
	}
}

XMLElement *XmlWrapper::getNode(string nodename)
{
	return xmlRoot->FirstChildElement(nodename.c_str());
}

list<XMLElement*> XmlWrapper::getNodes(string nodename)
{
	return getNodes(nodename, xmlRoot);
}

XMLElement *XmlWrapper::addNode(std::string nodeName)
{
	XMLElement *newNode = xmlDoc.NewElement(nodeName.c_str());
	xmlRoot->InsertEndChild(newNode);
	needSave = true;
	return newNode;
}

void XmlWrapper::addAttribute(tinyxml2::XMLElement *node,
							std::string attributeName,
							std::string attributeValue)
{
	node->SetAttribute(attributeName.c_str(), attributeValue.c_str());
	needSave = true;
}

void XmlWrapper::setText(tinyxml2::XMLElement *node, std::string content)
{
	node->SetText(content.c_str());
	needSave = true;
}


list<XMLElement*> XmlWrapper::getNodes(string nodename, XMLElement *current)
{
	list<XMLElement*> listElem = list<XMLElement*>();
	
	XMLElement *elem = current->FirstChildElement(nodename.c_str());

	list<XMLElement *> t;
	/* nodes are found */
	if (elem) {
		while (elem) {
			listElem.push_back(elem);
			elem = elem->NextSiblingElement(); // iteration 
		}
		return listElem;
	}
	/* nodes not found: needs to do a deep search */
	XMLElement *node = xmlRoot->FirstChildElement();
	if (!node)
		return listElem;

	while (node) {
		t = getNodes(nodename, node);
		listElem.insert(listElem.end(), t.begin(), t.end());
		node = node->NextSiblingElement(); // iteration 
	}

	return listElem;
}

list<string> *XmlWrapper::getAttributeForNodes(string nodename, string attributename)
{
	list<string> *l = new list<string>();
	XMLElement *elem = xmlRoot->FirstChildElement(nodename.c_str());
	while (elem) {
		l->push_back(elem->Attribute(attributename.c_str()));
		elem = elem->NextSiblingElement(); // iteration 
	 }
	 cout << l->size() << endl;

	return l;
}

XMLElement *XmlWrapper::getNodeWithAttributeValue(string nodename, string attribute, string value)
{
	list<XMLElement *> baseList = getNodes(nodename);
	list<XMLElement *>::iterator it;
	XMLElement * elem;
	for (it = baseList.begin(); it != baseList.end (); ++it) {
		elem = *it;
		if (elem->Attribute(attribute.c_str()) == value)
			return elem;
	}
	return NULL;
}
