/*
 * (c) Copyright 2015-2018 	OscillatorIMP Digital
 * Gwenhael Goavec-Merou <gwenhael.goavec-merou@trabucayre.com>
 */

#include <iostream>
#include <fstream>
#include <tinyxml2.h>

#include "XmlWrapper.hpp"
#include "DriverGenerator.hpp"
#include "common.h"
#include "display.hpp"
using namespace tinyxml2;
using namespace std;

typedef list<XMLElement*>::iterator lelem;

DriverGenerator::DriverGenerator(string xmlFilename, string driverFilename, bool ng)
{
	xmlhandler = new XmlWrapper(xmlFilename);
	driverhandler = new XmlWrapper(driverFilename);
	rootName = xmlhandler->getRoot()->Attribute("name");
	drvList = xmlhandler->getNodes("driver");
	boardDrv = xmlhandler->getNodes("board_driver");
	suppressXml = true;
	_ng = ng;
}

DriverGenerator::DriverGenerator(XmlWrapper *xmlWrapper, XmlWrapper *driverWrapper, bool ng)
{
	xmlhandler = xmlWrapper;
	driverhandler = driverWrapper;
	rootName = xmlhandler->getRoot()->Attribute("name");
	drvList = xmlhandler->getNodes("driver");
	boardDrv = xmlhandler->getNodes("board_driver");
	suppressXml = false;
	_ng = ng;
}

DriverGenerator::~DriverGenerator()
{
	if (suppressXml) {
		delete xmlhandler;
		delete driverhandler;
	}
}

int DriverGenerator::generateInclude()
{
	int ret = 0;
	list<string>::iterator it;
	list<string> *includelist = xmlhandler->getAttributeForNodes("driver", "name");
	XMLElement *elem;
	string drivername;

    outfile << "#include <linux/version.h>\n";
	outfile << "#include <linux/init.h>\n";
	outfile << "#include <linux/module.h>\n";
	outfile << "#include <linux/platform_device.h>\n\n";
	for (it = includelist->begin (); it != includelist->end (); ++it) {
		elem = driverhandler->getNodeWithAttributeValue("driver", "filename", *it);
		if (!elem) {
			printError (*it + " not found in " + driverhandler->getFileName());
			ret = -1;
			goto end;
		}
		drivername = elem->Attribute("filename");
		outfile << "#include <" << drivername << "_core/" << drivername << "_config.h>" << std::endl;
	}

	outfile << "\n";
end:
	delete includelist;
	return ret;
}

int DriverGenerator::generateMacro()
{
	outfile << "#define " << rootName << "_defglob(_instname, _addr, _addr_size, _platname, _drvname, _id) \\\n";
	outfile << "\tstatic struct resource _instname##_resources[] = { \\\n";
	outfile << "\t\t{ \\\n";
	outfile << "\t\t\t.start = _addr, \\\n";
	outfile << "\t\t\t.end   = _addr + _addr_size, \\\n";
	outfile << "\t\t\t.flags = IORESOURCE_MEM, \\\n";
	outfile << "\t\t}, \\\n";
	outfile << "\t};\\\n";
	outfile << "\\\n";
	outfile << "static struct _platname plat_##_instname##_data = { \\\n";
	outfile << "\t.name       = #_instname,\\\n";
	outfile << "\t.num        = _id, \\\n";
	outfile << "\t.idnum      = _id, \\\n";
	outfile << "}; \\\n";

	outfile << "static struct platform_device plat_##_instname##_device = { \\\n";
	outfile << "\t.name = #_drvname, \\\n";
	outfile << "\t.id = _id, \\\n";
	outfile << "\t.dev    = { \\\n";
	outfile << "\t\t.release    = plat_" << rootName << "_release, \\\n";
	outfile << "\t\t.platform_data  = &plat_##_instname##_data,\\\n";
	outfile << "\t},\\\n";
	outfile << "\t.num_resources      = ARRAY_SIZE(_instname##_resources),\\\n";
	outfile << "\t.resource       = _instname##_resources,\\\n";
	outfile << "};\\\n";
	outfile << "\n";
	outfile << endl;


	return 0;
}

int DriverGenerator::generateResource()
{
	XMLElement *child;

	for (lelem it = boardDrv.begin (); it != boardDrv.end (); ++it){
		child = *it;
		outfile << "static struct resource " << child->Attribute("name");
		outfile << "_resources[] = {\n";
		outfile << "\t{\n";
		outfile << "\t\t.start = ";
		outfile << child->Attribute("base_addr") << ",\n";
		outfile << "\t\t.end   = " << child->Attribute("base_addr");
		outfile << " + " << child->Attribute("addr_size") << ",\n";
		outfile << "\t\t.flags = IORESOURCE_MEM,\n";
		outfile << "\t},\n};\n\n";
	}
	return 0;
}
int DriverGenerator::generatePlatformData()
{
	XMLElement *drv, *child, *elem;
	int i;
	string plat_struct, childName;
	string drivername;

	if (_ng == false) {

	for (lelem it = drvList.begin (); it != drvList.end (); ++it){
		drv = *it;
		drivername = drv->Attribute("name");
		elem = driverhandler->getNodeWithAttributeValue("driver", "filename", drivername);
		if (!elem) {
			printError(drivername + " not found in " + driverhandler->getFileName());
			return -1;
		}
		plat_struct = elem->Attribute("plat");
		child = drv->FirstChildElement("board_driver");
		for (i=0; child; i++) {
			childName = child->Attribute("name");
			outfile << "static struct "+plat_struct; 
			outfile << " plat_" + childName + "_data = {\n";
			outfile << "\t.name\t\t= \"" + childName + "\",\n";
			outfile << "\t.num\t\t= " << i << ",\n";
			outfile << "\t.idnum\t\t= " << i << ",\n";
			outfile << "};\n";
			child = child->NextSiblingElement(); // iteration 
		}
	}
	outfile << endl;
	} else {
		for (lelem it = drvList.begin (); it != drvList.end (); ++it){
			drv = *it;
			drivername = drv->Attribute("name");
			elem = driverhandler->getNodeWithAttributeValue("driver", "filename", drivername);
			if (!elem) {
				printError(drivername + " not found in " + driverhandler->getFileName());
				return -1;
			}
			plat_struct = elem->Attribute("plat");
			child = drv->FirstChildElement("board_driver");
			for (i=0; child; i++) {
				childName = child->Attribute("name");
				//cout << childName << endl;
				outfile << rootName << "_defglob(";
				outfile << childName << ", ";
				outfile << child->Attribute("base_addr") << ", ";
				outfile << child->Attribute("addr_size") << ", ";
				outfile << plat_struct << ", ";
				outfile << drivername << ", ";
				outfile << i << ");\n";
				child = child->NextSiblingElement(); // iteration 
			}
		}
		outfile << endl;
	}
	return 0;
}

int DriverGenerator::generatePlatformDevice()
{
	XMLElement *drv, *child, *elem;
	int i;
	string driverName, childName;

    string releaseFunc = "plat_" + rootName + "_release";
	for (lelem it = drvList.begin (); it != drvList.end (); ++it){
		drv = *it;
        //driverName = drv->Attribute("name");
		child = drv->FirstChildElement("board_driver");
		elem = driverhandler->getNodeWithAttributeValue("driver", "filename", drv->Attribute("name"));
		driverName = elem->Attribute("name");
		for (i=0; child; child = child->NextSiblingElement(), i++) {
            childName = child->Attribute("name");
            outfile << "static struct platform_device ";
            outfile << "plat_" + childName + "_device = {\n";
            outfile << "\t.name = \""+ driverName + "\",\n";
            outfile << "\t.id\t= " << i << ",\n";
            outfile << "\t.dev\t= {\n";
            outfile << "\t\t.release\t= " + releaseFunc + ",\n";
            outfile << "\t\t.platform_data\t= &plat_" + childName + "_data,\n";
            outfile << "\t},\n";
            outfile << "\t.num_resources\t\t= ARRAY_SIZE(";
			outfile << childName +"_resources),\n";
            outfile << "\t.resource\t\t= "+childName + "_resources,\n";
            outfile << "};\n";
		}
	}
    outfile << "\n";
	return 0;
}
int DriverGenerator::generateInitExit(string authorName)
{
	string childName;
	outfile << "static int __init board_" << rootName << "_init(void)\n";
    outfile << "{\n\tint ret;\n";

	for (lelem it = boardDrv.begin (); it != boardDrv.end (); ++it){
		childName = (*it)->Attribute("name");
        outfile << "\tret = platform_device_register(&plat_" << childName;
		outfile << "_device);\n";
        outfile << "\tif (ret < 0)\n\t\treturn ret;\n";
	}

    outfile << "\n\treturn ret;\n}\n";

    outfile << "static void __exit board_" << rootName << "_exit(void)\n{\n";
	for (lelem it = boardDrv.begin (); it != boardDrv.end (); ++it){
		childName = (*it)->Attribute("name");
        outfile << "\tplatform_device_unregister(&plat_" << childName << "_device);\n";
	}
    outfile << "}\n\n";
    outfile << "module_init(board_" << rootName << "_init);\n";
    outfile << "module_exit(board_" << rootName << "_exit);\n";

    outfile << "MODULE_AUTHOR(\"" << authorName << "\");\n";
    outfile << "MODULE_DESCRIPTION(\"Board specific " << rootName << "\");\n";
    outfile << "MODULE_LICENSE(\"GPL\");\n";
	return 0;

}

int DriverGenerator::generateBoardDriver(string outfilename, string authorName)
{
	int ret = 0;

	outfile.open(outfilename.c_str());
	if (0 > generateInclude()) {
		ret = -1;
		goto end;
	}

	outfile << "void plat_" << rootName;
	outfile << "_release(struct device *dev)\n";
	outfile << "{\n";
	outfile << "\tdev_dbg(dev, \"released\\n\");\n";
	outfile << "}\n\n";

	if (_ng == true) {
		generateMacro();
		generatePlatformData();
		/*XMLElement *child;

		for (lelem it = boardDrv.begin (); it != boardDrv.end (); ++it){
			child = *it;
			cout << child->Attribute("name") << endl;
			outfile << rootName << "_defglob(";
			outfile << child->Attribute("name") << ", ";
			outfile << child->Attribute("base_addr") << ", ";
			outfile << child->Attribute("addr_size") << ", ";
			//platname
			//drvname
			//id
		}*/

	} else {
		if (generateResource() < 0) {
			ret = -2;
			goto end;
		}
		cout << "toto" << endl;
		if (generatePlatformData() < 0) {
			ret = -3;
			goto end;
		}
		cout << "toto2" << endl;
		if (generatePlatformDevice() < 0) {
			ret = -4;
			goto end;
		}
	}
	cout << "toto" << endl;
	if (generateInitExit(authorName) < 0) {
		ret = -5;
		goto end;
	}
	cout << "toto" << endl;
end:
	outfile.close();
	return ret;
}

int DriverGenerator::generateMakefile(string outfilename, string installDir)
{
	cout << "hello" << endl;
	outfile.open(outfilename.c_str());
	outfile << "obj-m +=" << "board_" << rootName << ".o" << endl;
	outfile << "EXTRA_CFLAGS+='-save-temps'\n";
	//if (installDir != "")
	//	outfile << INSTALL_DIR << " ?= " << installDir << endl;
	//	outfile << INSTALL_DIR << " := $(" << INSTALL_DIR << ")/" << rootName << endl;
	outfile << "BASE_NAME = " << rootName << endl;
	outfile << "include $(" << DRIVER_DIR << ")/Makefile.include" << endl;
	outfile.close();
	cout << "bye" << endl;
	return 0;
}
