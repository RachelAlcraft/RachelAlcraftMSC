#include "GeoVector.h"
#include <math.h>
#include <sstream>

GeoVector::GeoVector()
{
	x = 0;
	y = 0;
	z = 0;
	
}
GeoVector::GeoVector(const GeoVector& copy)
{
	x = copy.x;
	y = copy.y;
	z = copy.z;
	//_start = copy._start;
	//_end = copy._end;

}
GeoVector::GeoVector(double X, double Y, double Z)
{
	x = X;
	y = Y;
	z = Z;
	//_start = a;
	//_end = b; 
}

GeoVector::GeoVector(GeoCoords a, GeoCoords b)
{
	//_start = a;
	//_end = b;
	x = b.x - a.x;
	y = b.y - a.y;
	z = b.z - a.z;
}

/*void GeoVector::copy(GeoVector copyvec)
{
	x = copyvec.x;
	y = copyvec.y;
	z = copyvec.z;
}*/

GeoVector GeoVector::operator+(GeoVector const& obj)
{
	x += obj.x;
	y += obj.y;
	z += obj.z;
	return GeoVector(x, y, z);
}

GeoVector GeoVector::operator-(GeoVector const& obj)
{
	x -= obj.x;
	y -= obj.y;
	z -= obj.z;
	return GeoVector(x, y, z);
}

GeoVector GeoVector::operator*(double mult)
{
	x *= mult;
	y *= mult;
	z *= mult;
	return GeoVector(x, y, z);
}

GeoVector GeoVector::operator/(double div)
{
	x /= div;
	y /= div;
	z /= div;	
	return GeoVector(x, y, z);
}

GeoVector GeoVector::operator=(GeoVector const& obj)
{
	x = obj.x;
	y = obj.y;
	z = obj.z;
	//_start = obj._start;
	//_end = obj._end;
	return GeoVector(x,y,z);
}
GeoVector GeoVector::operator+(GeoCoords const& obj)
{
	x += obj.x;
	y += obj.y;
	z += obj.z;		
	return GeoVector(x, y, z);
}
GeoCoords GeoVector::movePoint(GeoCoords p)
{
	return GeoCoords(x+p.x, y + p.y, z + p.z);
}
double GeoVector::angle(GeoVector b)
{
	//angle betwen 2 vectors in 3 dimensions on the plain formed (between outer pairs of dihedral angles)
	GeoVector a = *this;
	//dot product
	double dot = (a.x * b.x) + (a.y * b.y) + (a.z * b.z);
	//magnitude
	double ma2 = a.magnitude();
	double mb2 = b.magnitude();
	double div = ma2 * mb2;
	//cos
	double cos_theta = dot / div;
	//inverse cos
	double theta = acos(cos_theta);
	theta = (theta / PI) * 180;//convert to degrees
	//if (theta > 180)
	//	theta = theta - 180;
	//theta = round(theta);
	//ATAN2 version?	I prefer this but the decision on sign is effectively the same thing.
	return theta;
}


double GeoVector::magnitude()
{
	double mag = (x * x) + (y * y) + (z * z);
	return sqrt(mag);
}

GeoVector GeoVector::getCrossProduct(GeoVector B)
{
	GeoVector A = *this;
	double px = (A.y * B.z) - (A.z * B.y);
	double py = (A.z * B.x) - (A.x * B.z);
	double pz = (A.x * B.y) - (A.y * B.x);
	return GeoVector(px, py, pz);
}

double GeoVector::getDotProduct(GeoVector B)
{
	GeoVector A = *this;
	double dot = (A.x * B.x) + (A.y * B.y) + (A.z * B.z);
	return dot;
}

double GeoVector::getOrthogonalDistance(GeoCoords p)
{//http://mathworld.wolfram.com/Point-LineDistance3-Dimensional.html
	GeoCoords a = GeoCoords(0, 0, 0);
	GeoCoords b = GeoCoords(x, y, z);
	GeoCoords c = p;
	GeoVector ca = GeoVector(c,a);
	GeoVector cb = GeoVector(c,b);
	GeoVector ba = GeoVector(b,a);
	GeoVector caDOTcb = ca.getCrossProduct(cb);
	double mag = ba.getMagnitude();
	double distance = caDOTcb.getMagnitude();
	distance = distance / mag;
	return distance;
}

double GeoVector::getMagnitude()
{
	GeoVector A = *this;
	double mag = (A.x * A.x) + (A.y * A.y) + (A.z * A.z);
	return sqrt(mag);
}

string GeoVector::info()
{
	stringstream ss;
	ss << "(" << x << "," << y << "," << z << ")";
	return ss.str();
}
