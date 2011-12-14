package metrocar.carUnit.gps;

import metrocar.carUnit.MetrocarCarUnitAndroidActivity;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

public class MetrocarGpsLocationListener implements LocationListener {
	static final String tag = "GPS"; // for Log

	TextView txtInfo;
	LocationManager lm;
	StringBuilder sb;
	int noOfFixes = 0;
	
	public MetrocarGpsLocationListener() {
		/* the location manager is the most vital part it allows access
		 * to location and GPS status services */
		//lm = (LocationManager) getSystemService(MetrocarCarUnitAndroidActivity.LOCATION_SERVICE);
	}

	@Override
	public void onLocationChanged(Location location) {
		Log.v(tag, "Location Changed");

		sb = new StringBuilder(512);

		noOfFixes++;

		/* display some of the data in the TextView */

		sb.append("No. of Fixes: ");
		sb.append(noOfFixes);
		sb.append('\n');
		sb.append('\n');

		sb.append("Londitude: ");
		sb.append(location.getLongitude());
		sb.append('\n');

		sb.append("Latitude: ");
		sb.append(location.getLatitude());
		sb.append('\n');

		sb.append("Altitiude: ");
		sb.append(location.getAltitude());
		sb.append('\n');

		sb.append("Accuracy: ");
		sb.append(location.getAccuracy());
		sb.append('\n');

		sb.append("Timestamp: ");
		sb.append(location.getTime());
		sb.append('\n');

		txtInfo.setText(sb.toString());
	}

	@Override
	public void onProviderDisabled(String provider) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onProviderEnabled(String provider) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onStatusChanged(String provider, int status, Bundle extras) {
		// TODO Auto-generated method stub
		
	}

}
