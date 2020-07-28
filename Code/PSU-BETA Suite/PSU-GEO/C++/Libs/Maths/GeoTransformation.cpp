#include "GeoTransformation.h"
#include <math.h>
#include <sstream>
#include <LogFile.h>

/*
I realise this should be done using eigen vectors
but for now it works with simple vector transformation enabling the object to be moved in space
*/

GeoTransformations::GeoTransformations()
{
	

}
GeoTransformations::~GeoTransformations()
{	
	for (unsigned int i = 0; i < transformations.size(); ++i)
	{
		if (transformations[i])
			delete transformations[i];
	}
	transformations.clear();
}
GeoTransformations::GeoTransformations(GeoCoords A, GeoCoords B, GeoCoords C)
{
	//This is the constructor to create a transformation that maps the 3 given points 
	//onto the origin and flat against the plane xz.
	MapA = A;
	MapB = B;
	MapC = C;
	TranslateRelativeToOrigin* t1 = new TranslateRelativeToOrigin(A);
	A = t1->applyTransformation(A);
	B = t1->applyTransformation(B);
	C = t1->applyTransformation(C);
	transformations.push_back(t1);

	RotationAboutOrigin* t2 = new RotationAboutOrigin(B,"XY");
	B = t2->applyTransformation(B);
	C = t2->applyTransformation(C);
	transformations.push_back(t2);

	RotationAboutOrigin* t3 = new RotationAboutOrigin(B,"YZ");
	B = t3->applyTransformation(B);
	C = t3->applyTransformation(C);
	transformations.push_back(t3);

	RotationAboutOrigin* t4 = new RotationAboutOrigin(C,"XZ");
	C = t4->applyTransformation(C);
	transformations.push_back(t4);	
}

GeoCoords GeoTransformations::applyTransformation(GeoCoords point)
{
	GeoCoords movedPoint = point;
	for (unsigned int i = 0; i < transformations.size(); ++i)
	{
		point = transformations[i]->applyTransformation(point);
	}
	return point;
}

string GeoTransformations::info()
{
	stringstream ss;	
	for (unsigned int i = 0; i < transformations.size(); ++i)
	{
		ss << transformations[i]->info() << "\n";
	}	
	return ss.str();
}

//TRANSLATION///////////////////////////////////////////////////////////////////////////////////////////////////////////////
TranslateRelativeToOrigin::TranslateRelativeToOrigin(GeoCoords A):GeoTransform()
{
	//This finds the vector that translates a fixed boddy relative to tge origin for the reference point p
	V = GeoVector(A, GeoCoords(0, 0, 0));
	//Log this
	stringstream ss;
	//ss << "Rotate to origin x=" << A.x << " y=" << A.y << " z=" << A.z;
	//LogFile::getInstance()->writeMessage(ss.str());
}
GeoCoords TranslateRelativeToOrigin::applyTransformation(GeoCoords point)
{	
	return V.movePoint(point);
}
string TranslateRelativeToOrigin::info()
{
	stringstream ss;
	ss << "Translate:" << V.info();
	return ss.str();
}
//ROTATION ABOUT THE ORIGIN////////////////////////////////////////////////////////////////////////////////////////////////////////////
RotationAboutOrigin::RotationAboutOrigin(GeoCoords A, string flatPlane) :GeoTransform()
{
	_flatPlane = flatPlane;	
	if (_flatPlane == "XY")
		_thetaDeg = findFlatRotation(A.x, A.y);
	else if (_flatPlane == "YZ")
		_thetaDeg = findFlatRotation(A.y, A.z);
	else if (_flatPlane == "ZX")
		_thetaDeg = findFlatRotation(A.z, A.x);
			
}
GeoCoords RotationAboutOrigin::applyTransformation(GeoCoords point)
{
	GeoCoords pointRotated = point;	
	if (_flatPlane == "XY")
		rotateFlatAboutOrigin(pointRotated.x, pointRotated.y, _thetaDeg);
	else if (_flatPlane == "YZ")
		rotateFlatAboutOrigin(pointRotated.y, pointRotated.z, _thetaDeg);
	else if (_flatPlane == "ZX")
		rotateFlatAboutOrigin(pointRotated.z, pointRotated.x, _thetaDeg);
		
	return pointRotated;	
}
string RotationAboutOrigin::info()
{
	stringstream ss;
	ss << "Rotate " << _flatPlane <<  ":" << _thetaDeg;
	return ss.str();
}

void RotationAboutOrigin::rotateFlatAboutOrigin(double& x, double& y, double Theta)
{
	double angleToApply = Theta;
	double angleLeft = Theta;
	if (angleToApply > 90)
	{
		angleToApply = 90;
		angleLeft = Theta - (90);
	}

	while (angleToApply > 0)
	{
		rotateFlatAboutOrigin1Quadrant(x, y, angleToApply);
		if (angleLeft > 0)
		{
			if (angleLeft > 90)
			{
				angleToApply = 90;
				angleLeft = angleLeft - (90);
			}
			else
			{
				angleToApply = angleLeft;
				angleLeft = 0;
			}
		}
		else
		{
			angleToApply = 0;
		}
	}
}
void RotationAboutOrigin::rotateFlatAboutOrigin1Quadrant(double& x, double& y, double thetaDeg)
{//We are guaranteed to move a maximum of 90% so no quadrant confusion
	//Convert to radians
	double Theta = radians(thetaDeg);
	//Triangle has 2 sides length a and a side length b
	GeoCoords p1(x, y, 0);
	GeoVector AO(p1, GeoCoords(0, 0, 0));
	double magAO = AO.getMagnitude();
	if (abs(magAO) > 0.0000001)//otherwise we are not moving anywhere
	{
		int Qfrom = 1;
		if (y < 0 && x > 0)
			Qfrom = 4;
		else if (y < 0 && x < 0)
			Qfrom = 3;
		else if (y > 0 && x < 0)
			Qfrom = 2;

		//This is now the hypotanuse of a right-angled triangle with the x-axis
		double sinT = abs(y) / magAO;
		double T = asin(sinT);
		//Now we can subtract theta and we have the angle with the x-axis fort the lower side of the triangle (a diagram would help!)
		double t = T - Theta;
		if (Qfrom == 2 || Qfrom == 4)
			t = T + Theta;
		//The new x and y are the points at the end of this new triangle
		//but what if we move into another quadrant? NOTE we are restricted to a 90 degree turn
		int Qto = Qfrom;
		if (Qfrom == 1)
		{
			if (Theta > T)
			{
				t = Theta - T;
				Qto = 4;
			}
		}
		else if (Qfrom == 2)
		{
			if ((T + Theta) > (PI / 2))
			{
				t = PI - (T + Theta);
				Qto = 1;

			}
		}
		else if (Qfrom == 3)
		{
			if (Theta > T)
			{
				t = Theta - T;
				Qto = 2;
			}
		}
		else//MUST BE Q4
		{
			if ((T + Theta) > (PI / 2))
			{
				t = PI - (Theta +  T);
				Qto = 3;

			}
		}		
		double newX = cos(t) * magAO;
		double newY = sin(t) * magAO;
		
		if (Qto == 2 || Qto == 3)
			newX *= -1;
		if (Qto == 3 || Qto == 4)
			newY *= -1;		

		x = newX;
		y = newY;
	}	
}

double RotationAboutOrigin::radians(double degrees)
{
	return (degrees * PI) / 180;

}
double RotationAboutOrigin::degrees(double radians)
{
	return (radians * 180) / PI;
}
double RotationAboutOrigin::findFlatRotation(double x, double y)
{
	
	GeoCoords pNoX(x, y, 0);
	//We are mapping from A to 0, then 0 to B, so we have an iscoseles triangle |AO|==|OB| and AB	
	int Qfrom = 1;
	if (y < 0 && x > 0)
		Qfrom = 4;
	else if (y < 0 && x < 0)
		Qfrom = 3;
	else if (y > 0 && x < 0)
		Qfrom = 2;

	GeoVector AO(pNoX, GeoCoords(0, 0, 0));
	double magAO = AO.getMagnitude();
	if (abs(magAO) > 0.0000001)//otherwise we are not moving anywhere
	{
		GeoVector OB(magAO, 0, 0);//moving into +ve quadrant
		GeoVector AB = OB + AO;
		double magAB = AB.getMagnitude();
		//use cosine rule
		//Find theta with the cosine rule	
		double magAO2 = pow(magAO, 2);
		double magAB2 = pow(magAB, 2);
		double costheta = ((2 * magAO2) - magAB2) / (2 * magAO2);
		double theta = acos(costheta);// in radians		
		double thetaDeg = degrees(theta);
		if (Qfrom == 4 || Qfrom == 3)
			thetaDeg = 360 - thetaDeg;
		//Log this
		//stringstream ss;
		//ss << "Rotate to " << _flatPlane << " Theta = " << thetaDeg;
		//LogFile::getInstance()->writeMessage(ss.str());
		return thetaDeg;
	}
	else
		return 0;
}


 





















