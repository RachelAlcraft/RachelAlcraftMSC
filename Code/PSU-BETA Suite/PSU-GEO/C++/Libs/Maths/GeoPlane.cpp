#include "GeoPlane.h"

/*double GeoPlane::getOrthogonalDistance(GeoCoords p)
{
	GeoVector perp = getPerpendicular();
	double distance = perp.getOrthogonalDistance(p);
	return distance;
}*/
GeoPlane::GeoPlane(GeoVector a, GeoVector b)
{
	//The plane can be uniqely defined by 2 vectors
	A = a;
	B = b;
}

void GeoPlane::create(GeoVector a, GeoVector b)
{
	A = a;
	B = b;
}

GeoVector GeoPlane::getPerpendicular()
{
	//the plane is uniquely defined by the vector that is perpendicular to it
	// which is the cross product of any 2 vectors lying on the plane
	return A.getCrossProduct(B);
}

GeoVector GeoPlane::getUnitPerpendicular()
{
	//the plane is uniquely defined by the vector that is perpendicular to it
	// which is the cross product of any 2 vectors lying on the plane
	GeoVector p = A.getCrossProduct(B);
	double mag = p.getMagnitude();
	return p / mag;
}
