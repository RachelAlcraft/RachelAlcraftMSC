#pragma once
#include <GeoCoords.h>
class GeoVector
{
	//get angle given another vector
	//apply vector to a point
	//some shifts around turns??
public://lazy public interface
	double x;
	double y;
	double z;
	const double PI = 3.141592653589793238463;
	//GeoCoords _start;
	//GeoCoords _end; //lazy extra info for perpendiculars
public:
	GeoVector();
	GeoVector(const GeoVector& copy);
	GeoVector(double, double, double);
	GeoVector(GeoCoords a, GeoCoords b);
	// Operator overloads	
	GeoVector operator + (GeoVector const& obj);
	GeoVector operator - (GeoVector const& obj);
	GeoVector operator * (double);
	GeoVector operator / (double);
	GeoVector operator = (GeoVector const& obj);
	// Operator overloads	
	GeoVector operator + (GeoCoords const& obj);
	GeoCoords movePoint(GeoCoords p);

	
	double angle(GeoVector);//the angle this vector makes with another vector (can start anywhere)
	double magnitude();
	GeoVector getCrossProduct(GeoVector);
	double getDotProduct(GeoVector);
	double getOrthogonalDistance(GeoCoords p);//shortest distance from p to the vector
	double getMagnitude();
	string info();


};

