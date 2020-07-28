#include "GeoCloud.h"
#include <GeoCoords.h>
#include <GeoVector.h>
#include <set>
#include <map>
#include <LogFile.h>

/*
TODO
CENTRE OF GEOMETRY
I'm not convinved that a centre of geometry (which I've since discovered is the usual way) (average of all x y and z) is any better.
For a centre of geometry I would then want to find the furtherst point for an axis, and then the furthest next othogonal
for another, it seems it would come roughly to the same thing and since the centre of geometry has no topological meaning
doesn't seem intrinsically better. I will experiment with this method and see what I get before deciding.

INSIDE OUTSIDE
For the problem of deciding what is inside and what is outside - there is no way of doing it without the bonds so the GeoCloud would have to become a connected cloud.
Then it would involve finding no particles in certain directons away from bonds. Surface particles could be labelled with a value, and the distance from the surface 
could be recorded for each particle. Or a density could be recorded for all points in space of surrounding particles, or surrounding bonds. Closer to the surface would have a lower density. 
But inside a curve would have high density. Needs to be bonds.

But in fact what actually does mark the inside and outside?
*/

GeoCloud::GeoCloud()
{
}

void GeoCloud::addCoords(GeoCoords coord)
{
	_coords.push_back(coord);
}

void GeoCloud::createDistances()
{
	//First we need to do a distance map and find the furthest points
	LogFile::getInstance()->writeMessage("Creating GeoCloud distance map");
	_farDistance.clear();
	_farCoords.clear();
	_perpDistance.clear();
	_perpCoords.clear();

	for (unsigned int i = 0; i < _coords.size(); ++i)
	{
		for (unsigned int j = i + 1; j < _coords.size(); ++j)
		{
			GeoVector gv(_coords[i], _coords[j]);
			double mag = gv.getMagnitude();			
			bool inserted = false;
			for (unsigned int k = 0; k < _farDistance.size(); ++k)
			{
				double dd = _farDistance[k];
				if (mag > dd && !inserted)
				{//biggest at the front					
					_farDistance.insert(_farDistance.begin() + k, mag);
					_farCoords.insert(_farCoords.begin() + k, pair<GeoCoords, GeoCoords>(_coords[i], _coords[j]));
					inserted = true;
				}
			}
			if (!inserted)
			{
				_farDistance.push_back(mag);
				_farCoords.push_back(pair<GeoCoords, GeoCoords>(_coords[i], _coords[j]));
			}			
		}
	}
	
	//Then we need to find the furtherst points on a distance orthogonal at some rotation
	for (unsigned int i = 0; i < _farCoords.size(); ++i)
	{
		GeoVector ortho1(_farCoords[i].first, _farCoords[i].second);

		vector<double> vDistance;
		vector<GeoCoords> vCoords;

		//we go through all the points and find the one that is furtherst from this vector to make the next orthoginal vector		
		double furthest2 = 0;
		for (unsigned int i = 0; i < _coords.size(); ++i)
		{
			double distance = ortho1.getOrthogonalDistance(_coords[i]);
			bool inserted = false;
			for (unsigned int j = 0; j < vDistance.size(); ++j)
			{
				double dd = vDistance[j];
				if (distance > dd && !inserted)
				{//biggest at the front
					vDistance.insert(vDistance.begin() + j, distance);
					vCoords.insert(vCoords.begin() + j, _coords[i]);
					inserted = true;
				}
			}
			if (!inserted)
			{
				vDistance.push_back(distance);
				vCoords.push_back(_coords[i]);
			}		
		}
		_perpCoords.push_back(vCoords);
		_perpDistance.push_back(vDistance);
	}		
}

void GeoCloud::makeTripod(GeoTripod& geo, unsigned int best1, unsigned int best2)
{
	if (_farCoords.size() >= best1 && _perpCoords.size() >= best2)
	{
		geo.A = _farCoords[best1].first;
		geo.B = _farCoords[best1].second;
		geo.C = _perpCoords[best1][best2];
		geo.Init = true;
	}
	else
	{
		geo.Init = false;
	}
}

/*void GeoCloud::makeTripod(GeoTripod& geo, unsigned int best1, unsigned int best2)
{
	//First we need to do a distance map and find the furthest points :-(
	vector<double> farmag;
	vector<pair<GeoCoords, GeoCoords >> farcoords;
	
	for (unsigned int i = 0; i < _coords.size(); ++i)
	{
		for (unsigned int j = i+1; j < _coords.size(); ++j)
		{
			GeoVector gv(_coords[i], _coords[j]);
			double mag = gv.getMagnitude();
			bool inserted = false;
			for (unsigned int k = 0; k < farmag.size(); ++k)
			{
				double dd = farmag[k];
				if (mag > dd && !inserted)
				{//biggest at the front					
					farmag.insert(farmag.begin() + k, mag);
					farcoords.insert(farcoords.begin() + k, pair<GeoCoords, GeoCoords>(_coords[i], _coords[j]));
					inserted = true;
				}
			}
			if (!inserted && farmag.size() < best1)
			{
				farmag.push_back(mag);
				farcoords.push_back(pair<GeoCoords, GeoCoords>(_coords[i], _coords[j]));
			}
			if (farmag.size() > best1)
			{
				farmag.pop_back();
				farcoords.pop_back();
			}									
		}
	}

	if (farmag.size() >= best1)
	{		
		_furthestPoints1.first = farcoords[best1-1].first;
		_furthestPoints1.second = farcoords[best1-1].second;
	}

	//Then we need to find the furtherst piunts on a distance orthogonal at some rotation
	GeoVector ortho1(_furthestPoints1.first, _furthestPoints1.second);
	//we go through all the points and find the one that is furtherst from this vector to make the next orthoginal vector
	vector<double> farmag2;
	vector<GeoCoords> farcoord2;
	double furthest2 = 0;
	for (unsigned int i = 0; i < _coords.size(); ++i)
	{
		double distance = ortho1.getOrthogonalDistance(_coords[i]);
		bool inserted = false;
		for (unsigned int j = 0; j < farmag2.size(); ++j)
		{
			double dd = farmag2[j];
			if (distance > dd && !inserted)
			{//biggest at the front
				farmag2.insert(farmag2.begin() + j, distance);
				farcoord2.insert(farcoord2.begin() + j, _coords[i]);
				inserted = true;
			}
		}
		if (!inserted && farmag2.size() < best2)
		{
			farmag2.push_back(distance);
			farcoord2.push_back(_coords[i]);
		}
		if (farmag2.size() > best2)
		{
			farmag2.pop_back();
			farcoord2.pop_back();
		}		
	}
	if (farcoord2.size() >= best2)
		_furthestPoint2 = farcoord2[best2-1];
	//This should fully define what we need for a transformation for this cloud. We have an axis along the furthyest 2 pointsd
	// Orthogonal to that we have the next furthest point
	// Our transformations of clouds will match anchor points along the axis and then rotate to the plane
	geo.A = _furthestPoints1.first;
	geo.B = _furthestPoints1.second;
	geo.C = _furthestPoint2;
}*/
