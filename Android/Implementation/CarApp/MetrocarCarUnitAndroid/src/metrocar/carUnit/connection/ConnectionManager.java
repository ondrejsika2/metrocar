package metrocar.carUnit.connection;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.util.Date;
import java.util.Hashtable;
import java.util.Vector;

import org.apache.http.HttpConnection;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;

import metrocar.carUnit.Core;
import metrocar.carUnit.Settings;
import metrocar.carUnit.protocol.ProtocolParser;

import android.location.Location;
import android.util.Log;

public class ConnectionManager implements IConnectionManager {

	private final String tag = "ConnectionManager";

	/** Authentification key */
	private String authKey;
	/** Secret key to combine with IMEI */
	private String secretKey = "metrocar";

	private static ConnectionManager instance = null;

	private ConnectionManager() {

	}

	public static ConnectionManager getInstance() {
		if (instance == null) {
			instance = new ConnectionManager();
		}
		return instance;
	}

	public Date getDate() {
		return getDateFromGoogle();
	}

	protected Date getDateFromGoogle() {
		/*String strUrl = "http://www.google.com" + ";"
				+ Settings.GPRS_URL_PARAMS;
		Log.v(tag, "Connecting to: " + "http://www.google.com");

		HttpConnection connection = null;
		Date googleDate = null;

		try {
			connection = (HttpConnection) Connector.open(strUrl,
					Connector.READ_WRITE);
			connection.setRequestMethod(HttpConnection.GET);

			googleDate = new Date(connection.getDate());
			Log.v(tag, "Google time: " + googleDate.toString());

			if (HttpConnection.HTTP_OK == connection.getResponseCode()) {
				Log.v(tag, "Http connection to " + strUrl + " OK: 200");
			} else {
				Log.v(tag, "Http connection to " + strUrl + " FAIL: "
						+ connection.getResponseCode(), Core.LOG_WARNING);
			}
		} catch (IOException e) {
			Log.v(tag, "#IOException");
			Log.v(tag, e.getMessage());
		} catch (IllegalArgumentException e) {
			Log.v(tag, "#IllegalArgumentException");
		} finally {
			try {
				connection.close();
			} catch (IOException e) {
				Log.v(tag,
						"#IOException closing connection/input/output buffers",
						Core.LOG_ERROR);
			}
		}//*/
		return null;
	}

	public void testConnection(String url) {
		/*String strUrl = url + ";" + Settings.GPRS_URL_PARAMS;
		Log.v(tag, "#Connecting to: " + url);

		HttpConnection connection = null;
		InputStream is = null;
		OutputStream os = null;
		StringBuffer sb = new StringBuffer();

		try {
			connection = (HttpConnection) Connector.open(strUrl,
					Connector.READ_WRITE);
			connection.setRequestMethod(HttpConnection.GET);

			Date d = new Date(connection.getDate());
			Log.v(tag, "#" + url + " server time: " + d.toString());

			XTConnectionManager.logConnectionPREInformation(connection);

			// Log.println("#Opening OutputStream");
			// DataOutputStream ostream = connection.openDataOutputStream();
//*/
			/*
			 * Log.println("#Opening InputStream"); is =
			 * connection.openInputStream(); // transition to connected! int ch
			 * = 0; for(int ccnt=0; ccnt < 150; ccnt++) { // get the title. ch =
			 * is.read(); if (ch == -1){ break; } sb.append((char)ch); }
			 */
/*
			if (HttpConnection.HTTP_OK == connection.getResponseCode()) {
				Log.v(tag, "#Http connection to " + strUrl + " OK: 200");
			} else {
				Log.v(tag, "#Http connection to " + strUrl + " FAIL: "
						+ connection.getResponseCode());
			}

			Log.v(tag, "#Connection successful.");
			// Log.println("<-- "+sb.toString());

		} catch (ConnectionNotFoundException e) {
			Log.v(tag, "#ConnectionNotFoundException");
		} catch (IOException e) {
			System.err.println("SYSERR: Error creating HTTP connection");
			Log.v(tag, "#IOException");
			Log.v(tag, e.getMessage());
		} catch (IllegalArgumentException e) {
			Log.v(tag, "#IllegalArgumentException");
		} finally {
			try {
				connection.close();
				if (is != null)
					is.close();
				if (os != null)
					os.close();
			} catch (IOException e) {
				Log.v(tag,
						"#IOException closing connection/input/output buffers");

			}
		}//*/
	}

	public void testConnection() {
		testConnection(Settings.TESTSERVER_URL);
	}

	public boolean sendGPSdata(Vector<Location> locations) {
		return sendGPSdata(locations, null, null);
	}

	public boolean sendGPSdataFirst(Vector<Location> locations, Date since) {
		return sendGPSdata(locations, since, null);
	}

	public boolean sendGPSdataLast(Vector<Location> locations, Date till) {
		return sendGPSdata(locations, null, till);
	}

	public boolean sendGPSdata(Vector<Location> locations, Date since, Date till) {
		// TODO
		// String parsedRequest = Core.getProtocolParser()
		// .parseDataToXML(Core.getAccessManager().getAuthKey(), 1, locations);
		if (locations == null || locations.isEmpty())
			return false;

		String xmlRequest = ProtocolParser.getInstance().parseDataToXML(
				Core.authKey, 2, locations);

		/*
		 * StringBuffer parsedRequest = new StringBuffer();
		 * parsedRequest.append("<data>"); for (int i = 0; i < locations.size();
		 * i++) { Location l = (Location)locations.elementAt(i);
		 * parsedRequest.append("<loc>");
		 * parsedRequest.append(l.getQualifiedCoordinates().getLatitude());
		 * parsedRequest.append(";");
		 * parsedRequest.append(l.getQualifiedCoordinates().getLongitude());
		 * parsedRequest.append("</loc>"); } parsedRequest.append("</data>");//
		 */
		return sendData(xmlRequest);
	}

	public Hashtable<String, String> requestSettings() {
		// TODO
		return null;
	}

	public Vector<String> requestReservations() {
		// TODO
		return null;
	}

	private boolean sendData(String xml) {

		String strUrl = Settings.SERVER_URL;
		Log.v(tag, "Connecting to: " + Settings.SERVER_URL);

		// Create a new HttpClient and Post Header
		HttpClient httpclient = new DefaultHttpClient();
		HttpPost httppost = new HttpPost(strUrl);
		Log.v(tag, "Creating HTTP POST to URL: " + strUrl);
		boolean dataSent = false;

		// Add your data
		try {
			httppost.setEntity(new StringEntity(xml));
			Log.v(tag, "Sending message: " + xml);

			// Execute HTTP Post Request
			HttpResponse response = httpclient.execute(httppost);

			String line = "";
			StringBuilder total = new StringBuilder();

			// Wrap a BufferedReader around the InputStream
			BufferedReader rd = new BufferedReader(new InputStreamReader(
					response.getEntity().getContent()));

			// Read response until the end
			while ((line = rd.readLine()) != null) {
				total.append(line);
			}
			
			Log.d(tag, "Response:\n"+total);
		} catch (UnsupportedEncodingException e) {
			Log.e(tag, "UnsupportedEncopdingException");
		} catch (ClientProtocolException e) {
			Log.e(tag, "ClientProtocolException");
		} catch (IOException e) {
			Log.e(tag, "IOException");
		}

		/*
		 * try { connection = (HttpConnection) Connector.open(strUrl,
		 * Connector.READ_WRITE);
		 * connection.setRequestMethod(HttpConnection.POST);
		 * 
		 * connection.setRequestProperty("Content-Type", "application/xml");
		 * connection.setRequestProperty("User-Agent", "http4e/2.1.1");
		 * connection.setRequestProperty("Host", "luboskrcal.cz");
		 * 
		 * logConnectionPREInformation(connection);
		 * 
		 * os = connection.openDataOutputStream(); os.writeUTF(xml); Log.v(tag,
		 * "DOS wrote: " + xml);
		 * 
		 * // Transition to connected state
		 * 
		 * is = connection.openDataInputStream(); response = is.readUTF();
		 * 
		 * if (response != null && response.length() > 0) { // Response where
		 * there should be none Log.v(tag,
		 * "Got unexpected response from server:" + response, Core.LOG_WARNING);
		 * }
		 * 
		 * if (HttpConnection.HTTP_OK == connection.getResponseCode()) {
		 * Log.v(tag, "Http connection to " + Settings.SERVER_URL + " OK: 200");
		 * } else { Log.v(tag, "Http connection to " + Settings.SERVER_URL +
		 * " FAIL: " + connection.getResponseCode(), Core.LOG_WARNING); }
		 * 
		 * dataSent = true; } catch (ConnectionNotFoundException e) { Log.v(tag,
		 * "ConnectionNotFoundException"); } catch (IOException e) { Log.v(tag,
		 * "#IOException"); Log.v(tag, e.getMessage()); } catch
		 * (IllegalArgumentException e) { Log.v(tag,
		 * "#IllegalArgumentException"); } finally { try { os.close();
		 * is.close(); connection.close(); } catch (IOException e) { Log.v(tag,
		 * "#IOException closing connection/input/output buffers",
		 * Core.LOG_ERROR); } }//
		 */
		return dataSent;
	}

	/*private static void logConnectionPREInformation(HttpConnection hc) {

		Log.v(tag,
				"Request Method for this connection is "
						+ hc.getRequestMethod());
		Log.v(tag, "URL in this connection is " + hc.getURL());
		Log.v(tag, "Protocol for this connection is " + hc.getProtocol()); // It
																			// better
																			// be
																			// HTTP:)
		Log.v(tag, "This object is connected to " + hc.getHost() + " host");
		Log.v(tag, "HTTP Port in use is " + hc.getPort());
		Log.v(tag, "Query parameter in this request are  " + hc.getQuery());

	}//*/

}