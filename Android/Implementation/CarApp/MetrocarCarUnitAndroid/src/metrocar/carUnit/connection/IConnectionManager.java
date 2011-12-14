package metrocar.carUnit.connection;

import java.util.Date;
import java.util.Hashtable;
import java.util.Vector;

import android.location.Location;

public interface IConnectionManager {

    Date getDate();

    Vector<String> requestReservations();

    Hashtable<String, String> requestSettings();

    boolean sendGPSdata(Vector<Location> locations);

    boolean sendGPSdata(Vector<Location> locations, Date since, Date till);

    boolean sendGPSdataFirst(Vector<Location> locations, Date since);

    boolean sendGPSdataLast(Vector<Location> locations, Date till);

    void testConnection(String url);

}