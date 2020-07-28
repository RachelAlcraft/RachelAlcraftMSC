#pragma once
#include <GeoTransformation.h>
#include <GeoCoords.h>

using namespace std;


class GeoCuboid
{
	public:
		
};

class GeoTripod
{
public://lazy public interface TODO
	GeoCoords A;
	GeoCoords B;
	GeoCoords C;
	bool Init;
public:
	GeoTripod() { Init = false; }
	GeoTripod(GeoCoords a, GeoCoords b, GeoCoords c);
	GeoTransformations* getTransformation(GeoTripod tri/*, int orientation*/);
	GeoTripod operator = (GeoTripod const& obj);
	string info();

};
