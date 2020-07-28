#pragma once
#include <GeoShape.h>
#include <GeoCoords.h>
#include <vector>

using namespace std;

class GeoCloud
{
private:
	vector<GeoCoords> _coords;
	//pair<GeoCoords, GeoCoords> _furthestPoints1;
	//GeoCoords _furthestPoint2;

	vector<double> _farDistance;
	vector<pair<GeoCoords, GeoCoords >> _farCoords;
	vector<vector<double>> _perpDistance;
	vector < vector<GeoCoords>> _perpCoords;

	
public:
	GeoCloud();
	void addCoords(GeoCoords coord);
	void makeTripod(GeoTripod& geo, unsigned int best1, unsigned int best2); //the bests params control whether it is the first best or second best etc to allow iteration through the possibilities
	void createDistances();
};

