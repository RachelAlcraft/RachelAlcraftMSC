#include "GeoShape.h"
#include <sstream>

GeoTripod::GeoTripod(GeoCoords anchor, GeoCoords axisFar, GeoCoords perpFar)
{
	anchor = anchor;
	axisFar = axisFar;
	perpFar = perpFar;
	Init = true;
}

GeoTransformations* GeoTripod::getTransformation(GeoTripod tri/*, int orientation*/)
{
	/*
	TODO
	I ought to be getting variious different orientations of the transformations
	For now they are all the same
	*/
	
	return new GeoTransformations(tri.A, tri.B, tri.C);	
}

GeoTripod GeoTripod::operator=(GeoTripod const& obj)
{
	A = obj.A;
	B = obj.B;
	C = obj.C;
	return (GeoTripod(A, B, C));
}

string GeoTripod::info()
{
	stringstream ss;
	ss << "A=" << A.info() << " B=" << B.info() << " C=" << C.info();
	return ss.str();;
}
