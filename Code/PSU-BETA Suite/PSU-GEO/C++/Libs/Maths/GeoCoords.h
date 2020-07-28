#pragma once
//#include <GeoTransformation.h>

#include <string>

using namespace std;
class GeoCoords
{

public:
	double x;
	double y;
	double z;

public:
	GeoCoords(double, double, double);
	GeoCoords();
	string info();
	// Operator overloads	
	GeoCoords operator + (GeoCoords const& obj);

};

