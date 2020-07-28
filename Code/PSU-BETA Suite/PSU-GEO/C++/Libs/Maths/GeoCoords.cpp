#include "GeoCoords.h"
#include <sstream>

GeoCoords::GeoCoords()
{
	x = 0;
	y = 0;
	z = 0;
}

string GeoCoords::info()
{
	stringstream ss;
	ss << "(" << x << "," << y << "," << z << ")";
	return ss.str();
}



GeoCoords::GeoCoords(double x_coord, double y_coord, double z_coord)
{
	x = x_coord;
	y = y_coord;
	z = z_coord;
}

GeoCoords GeoCoords::operator+(GeoCoords const& obj)
{
	x += obj.x;
	y += obj.y;
	z += obj.z;
	return GeoCoords(x, y, z);
}
