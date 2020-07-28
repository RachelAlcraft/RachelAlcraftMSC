#pragma once

#include <GeoCoords.h>
#include <GeoVector.h>


class GeoPlane
{
public:
	GeoVector A;
	GeoVector B;
public:
	GeoPlane() {}
	GeoPlane(GeoVector, GeoVector);
	void create(GeoVector, GeoVector);
	GeoVector getPerpendicular(); // a plane can be defined by its perpendicular
	GeoVector getUnitPerpendicular(); // a plane can be defined by its perpendicular
	//double getOrthogonalDistance(GeoCoords p);//shortest distance from p to the plane (via the orthogonal vector)
};

