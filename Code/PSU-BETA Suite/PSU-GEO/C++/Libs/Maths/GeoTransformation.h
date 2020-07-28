#pragma once
#include <GeoPlane.h>
#include <GeoVector.h>
#include <GeoCoords.h>
#include <vector>




using namespace std;

/* I have failed to work with 3d transformations, so for now I am going to go via 0,0,0
and map onto the x and y axes
TODO put it into 3d space properly
*/

class GeoTransform
{
public:
	//virtual GeoCoords applyTransformation(GeoCoords point) { return GeoCoords(0, 0, 0); }; //won't let me =0 it ??? TODO
	GeoTransform() {}
	virtual GeoCoords applyTransformation(GeoCoords point) = 0;
	virtual string info() = 0;
protected:
	const double PI = 3.141592653589793238463;
protected:


};


class TranslateRelativeToOrigin :public GeoTransform
{
private:
	GeoVector V;
public:
	TranslateRelativeToOrigin(GeoCoords p);
	GeoCoords applyTransformation(GeoCoords point) override;
	string info() override;
};

class RotationAboutOrigin :public GeoTransform
{
private:
	double _thetaDeg; // in degrees#
	string _flatPlane;
protected:
	void rotateFlatAboutOrigin(double& x, double& y, double theta);
	void rotateFlatAboutOrigin1Quadrant(double& x, double& y, double theta);
	double findFlatRotation(double x, double y);
	double radians(double degrees);
	double degrees(double radians);
public:
	RotationAboutOrigin(GeoCoords p, string flatPlane);
	GeoCoords applyTransformation(GeoCoords point) override;
	string info() override;
};
/*class RotateTo_Z_Is_Zero_AboutOrigin :public GeoTransform
{
private:
	double thetaDeg; // in degrees
public:
	RotateTo_Z_Is_Zero_AboutOrigin(GeoCoords p);
	GeoCoords applyTransformation(GeoCoords point) override;
	string info() override;
};

class RotateTo_Y_Is_Zero_OverX_Axis :public GeoTransform
{
private:
	double thetaDeg; // in degrees
public:
	RotateTo_Y_Is_Zero_OverX_Axis(GeoCoords p);
	GeoCoords applyTransformation(GeoCoords point) override;
	string info() override;
};*/


class GeoTransformations
{
private:
	vector<GeoTransform*> transformations;
	GeoCoords MapA;
	GeoCoords MapB;
	GeoCoords MapC;
public:
	GeoTransformations();
	~GeoTransformations();
	GeoTransformations(GeoCoords a, GeoCoords b, GeoCoords c);
	GeoCoords applyTransformation(GeoCoords point);
	string info();
private:	
};


