package metrocar.carUnit;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Vector;
import java.util.logging.Logger;

import metrocar.carUnit.connection.ConnectionManager;
import metrocar.carUnit.protocol.ProtocolParser;
import metrocar.carUnit.protocol.ProtocolParser.Response;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;

import android.app.Activity;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.TextView;

public class MetrocarCarUnitAndroidActivity extends Activity implements LocationListener {
	static final String tag = "Metrocar"; // for Log
	
	TextView txtInfo;
	LocationManager lm;
	StringBuilder sb;
	int noOfFixes = 0;
	
	final int userID = 2; // We will get this based on the key card/ app unlock
	
	Vector<Location> locations = new Vector<Location>(100);
	
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        
        lm = (LocationManager) getSystemService(LOCATION_SERVICE);
        txtInfo = (TextView) findViewById(R.id.textView1);
    }
    
    @Override
    protected void onResume() {
    	super.onResume();
    	ProtocolParser parser = ProtocolParser.getInstance();
    	
    	String xmlSettingsRequest = parser.parseRequestToXML(Core.authKey, Core.PROTOCOL_SETTINGS);
    	Response response;
    	try {
			//response =  ConnectionManager.getInstance().requestSettings();
	    	//Settings.updateSettings(parser.getSettings(response));
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

    	lm.requestLocationUpdates(LocationManager.GPS_PROVIDER, Settings.SYSTEM_TASK_GPSREAD_PERIOD, 10f, this);
    	// TODO init timers   	
    	
    	
    }
    
    @Override
    protected void onPause() {
    	lm.removeUpdates(this);
    	super.onPause();
    }

    

    public void sendData(View view) throws Exception {
    	//postData();
    }
    
    
    public String postData(String xml) throws Exception {
    	// Testing url
    	String url = "http://192.168.56.101:8000/comm/xml/";   	
    	
    	// Dummy message
    	//String msg = "<?xml version=\"1.0\" encoding=\"utf-8\"?><r><a>test</a><m>123123123</m><v><i>2</i><s>09-12-21 14:20</s><p><b>51.000</b><c>33.000</c></p><q><d>0.04</d><e>2.01</e></q><q><d>0.4</d><e>3.2</e></q><l>4000</l><t>09-12-21 15:40</t></v><z><x>RESERVATIONS</x><x>SETTINGS</x></z></r>";
    	
    	
        // Create a new HttpClient and Post Header
        HttpClient httpclient = new DefaultHttpClient();
        HttpPost httppost = new HttpPost(url);
        Log.v(tag, "Creating HTTP POST to URL: "+url);
        
            // Add your data
            httppost.setEntity(new StringEntity(xml));
            Log.v(tag, "Sending message: " + xml);

            // Execute HTTP Post Request
            HttpResponse response = httpclient.execute(httppost);
            
            String line = "";
            StringBuilder total = new StringBuilder();
            
            // Wrap a BufferedReader around the InputStream
            BufferedReader rd = new BufferedReader(new InputStreamReader(response.getEntity().getContent()));

            // Read response until the end
            while ((line = rd.readLine()) != null) { 
                total.append(line); 
            }
            
            //TextView output = (TextView) findViewById(R.id.textView1);
            //output.setText(response.getStatusLine().toString());
            //output.setText(total);
            
            
            return total.toString();
            
        
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
		
		Log.v(tag, "Registering new location: "+location.toString());
		locations.add(location);
		
		Log.v(tag, "((locations.size()+1) % 5): "+((locations.size()+1) % 5));
		if (((locations.size()+1) % 5) == 0) {
			
			if (ConnectionManager.getInstance().sendGPSdata(locations)) {
                locations.removeAllElements();
                Log.v(tag, "SENDING GPS DATA SUCCESSFULL");
            } else {
                Log.e(tag, "ERROR SENDING GPS DATA");
            }
		}
		
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