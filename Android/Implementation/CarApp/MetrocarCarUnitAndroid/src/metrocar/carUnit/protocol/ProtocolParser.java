package metrocar.carUnit.protocol;

import java.util.Date;
import java.util.Hashtable;
import java.util.Vector;
import java.util.Calendar;


import android.location.Location;
import android.util.Log;

import com.exploringxml.xml.*;

import metrocar.carUnit.*;

/**
 * Class that parses raw data to/from protocol-defined XML.
 * @author Lubos Krcal
 */
public class ProtocolParser {
	private static final String tag = "ProtocolParser";

    private static ProtocolParser instance = null;

    private ProtocolParser(){
    }

    public static ProtocolParser getInstance(){
        if (instance == null){
            instance = new ProtocolParser();
        }
        return instance;
    }

    public class Response {
        private int type;
        private Hashtable<String, String> settings;
        private Vector<String> reservations;
    }

    /**
     * Constructs a XML protocol-valid request to server. This request contains
     * GPS data. Optionally it contains since and till date. It is possible to
     * send both since and till dates in one request (according to protocol).
     *
     * This method check for all combinations of Core.PROTOCOL_*.
     *
     * User any of convenience parsing methods for simpler interface. This method
     * constructs the most complex XML requests.
     *
     * @param authkey = pure string only, no XML injection! :)
     * @param userId
     * @param data
     * @param since
     * @param till
     * @return
     */
    public String parseAllToXML(String authkey, int REQUEST_TYPE, int userId,
            Vector<Location> data, Date since, Date till){

        // no auth key
        if (authkey == null) return null;
        
        // request to settings and reservations in the same time not supported
        if ((REQUEST_TYPE & (Core.PROTOCOL_SETTINGS | Core.PROTOCOL_RESERVATIONS)) > 0)
            return null;
        // no user ID when there is one required
        if ((REQUEST_TYPE & (Core.PROTOCOL_DATA | Core.PROTOCOL_SINCE | Core.PROTOCOL_TILL)) > 0
             && userId <= 0)
            return null;
        if ((REQUEST_TYPE & Core.PROTOCOL_SINCE) > 0 && since == null)
            return null;
        if ((REQUEST_TYPE & Core.PROTOCOL_TILL) > 0 && till == null)
            return null;
        if ((REQUEST_TYPE & Core.PROTOCOL_DATA) > 0 &&
                (data == null || data.isEmpty()))
            return null;

        String xml = new String();
        String xmlAuth = new String();
        String xmlSince = new String();
        String xmlTill = new String();
        String xmlRequest = new String();
        String xmlUser = new String();
        StringBuffer xmlPositions = new StringBuffer();
        String xmlData = new String();

        // construct since and date tags
        if ((REQUEST_TYPE & Core.PROTOCOL_SINCE) > 0){
            Calendar c = Calendar.getInstance();
            c.setTime(since);
            xmlSince = "<s>"+calendarToString(c)+"</s>";
        }
        if ((REQUEST_TYPE & Core.PROTOCOL_TILL) > 0){
            Calendar c = Calendar.getInstance();
            c.setTime(till);
            xmlTill = "<t>"+calendarToString(c)+"</t>";
        }
        // construct requests
        if ((REQUEST_TYPE & Core.PROTOCOL_SETTINGS) > 0){
            xmlRequest.concat("<x>SETTINGS</x>");
        }
        if ((REQUEST_TYPE & Core.PROTOCOL_RESERVATIONS) > 0){
            xmlRequest.concat("<x>RESERVATIONS</x>");
        }
        if (xmlRequest.length() > 0){
            xmlRequest = "<z>"+xmlRequest+"</z>";
        }
        // construct authorisation
        xmlAuth = "<a>"+authkey+"</a>";
        // construct positions
        if ((REQUEST_TYPE & Core.PROTOCOL_DATA) > 0){
            xmlPositions.append("<p>");
            for (int i = 0; i < data.size(); i++) {
                Location loc = (Location) data.elementAt(i);
                String strloc =
                    "<b>"+loc.getLatitude()+"</b>"+
                    "<c>"+loc.getLongitude()+"</c>";
                xmlPositions.append(strloc);
            }
            xmlPositions.append("</p>");
        }
        if (xmlSince.length() > 0 || xmlPositions.length() > 0
                || xmlTill.length() > 0){
            xmlData = "<v>"+xmlSince+xmlPositions.toString()+xmlTill+"</v>";
        }
        xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"+
                "<r>"+xmlAuth+xmlData+xmlRequest+"</r>";
        return xml;
    }

    /**
     * Convenience method for sending just settings or reservations request.
     *
     * Contructs a XML protocol-valid request to server. This request can
     * ask for settings or reservations. No GPS data can be send with this
     * request.
     *
     * This parse method only checks for exclusive Core.PROTOCOL_SETTINGS and
     * Core.PROTOCOL_RESERVATIONS types.
     *
     * @param authKey - car unit authentification key
     * @param REQUEST_TYPE - enum: one of Core.PROTOCOL_*
     * @return
     */
    public String parseRequestToXML(String authKey, int REQUEST_TYPE){
        if (REQUEST_TYPE == Core.PROTOCOL_SETTINGS ||
            REQUEST_TYPE == Core.PROTOCOL_RESERVATIONS){
            return parseAllToXML(authKey, REQUEST_TYPE, 0, null, null, null);
        }
        return null;
    }

    /**
     * Convenience method for sending just GPS data in request.
     *
     * Contructs a XML protocol-valid request to server. Contains GPS data.
     * Nothing else can be added to request using this method.
     *
     * This parse method automatically sets the request type to Core.PROTOCOL_DATA
     */
    public String parseDataToXML(String authKey, int userId, Vector<Location> data){
        return parseAllToXML(authKey, Core.PROTOCOL_DATA, userId, data, null, null);
    }

    /**
     * Convenience method for sending just since date in request.
     *
     * Contructs a XML protocol-valid request to server. Contains since date.
     * Nothing else can be added to request using this method.
     *
     * This parse method automatically sets the request type to Core.PROTOCOL_SINCE
     */
    public String parseSinceToXML(String authKey, int userUd, Date since){
        return parseAllToXML(authKey, Core.PROTOCOL_SINCE,
                userUd, null, since, null);
    }

    /**
     * Convenience method for sending just till date in request.
     *
     * Contructs a XML protocol-valid request to server. Contains till date.
     * Nothing else can be added to request using this method.
     *
     * This parse method automatically sets the request type to Core.PROTOCOL_TILL
     */
    public String parseTillToXML(String authKey, int userUd, Date till){
        return parseAllToXML(authKey, Core.PROTOCOL_TILL,
                userUd, null, null, till);
    }

    /**
     * Parser input XML string to Response class. You can only retrieve data
     * from response class using ProtocolParser's interface.
     *
     * Retrieving reservations NOT YET IMPLEMENTED.
     *
     * @param xml - String with XML response.
     * @return Response if parsing was ok, null otherwise
     */
    public Response parseResponse(String xml){
        if (xml == null)
            return null;
        Xparse parser = new Xparse();
        Node root = parser.parse(xml);
        if (root == null){
            Log.e(tag, "Parser: Error parsing root node. XML"
                    + "probably invalid.");
            return null;
        }
        // detect reponse type
        Node reservationsNode = root.find("r/u", new int [] {1,1});
        Node settingsNode = root.find("r/g", new int [] {1,1});
        int hasReservation = (reservationsNode == null) ? 0 : Core.PROTOCOL_RESERVATIONS;
        int hasSettings = (settingsNode == null) ? 0 : Core.PROTOCOL_SETTINGS;
        int type = hasReservation | hasSettings;
        if (type == Core.PROTOCOL_RESERVATIONS){
            Log.i(tag, "Parser: Detected RESERVATIONS response.");
        } else if (type == Core.PROTOCOL_SETTINGS){
        	Log.i(tag, "Parser: Detected SETTINGS response");
        } else {
        	Log.e(tag, "Parser: No or unknown response type detected."
                    + "Response is not one of RESERVATIONS or SETTINGS.");
            return null;
        }
        
        if (type == Core.PROTOCOL_RESERVATIONS){
            // TODO - NOT YET IMPLEMENTED
            return null;
        }

        Hashtable<String, String> settings = new Hashtable<String, String>();
        if(type == Core.PROTOCOL_SETTINGS){
            Node settingNode = null;
            String key = null;
            String value = null;
            int i = 1;
            while ((settingNode = settingsNode.find("j", new int [] {i++})) != null){
                Node keyNode = settingNode.find("k", new int [] {1});
                if (keyNode != null)
                    key = keyNode.getCharacters();
                Node valueNode = settingNode.find("h", new int [] {1});
                if (valueNode != null)
                    value = valueNode.getCharacters();
                if (key == null || value == null ||
                    key.length() <= 0 || value.length() <= 0){
                    key = null;
                    value = null;
                    Log.e(tag, "Parser: Error parsing settings"
                            + "element, key or value is null or empty.");
                }
                Log.d(tag, "Parser: Successfully parsed settings"
                        + "element: ("+key+","+value+").");
                settings.put(key, value);
            }
        }

        Response response = new Response();
        response.type = type;
        response.reservations = null;
        response.settings = settings;
        
        return response;
    }

    public int getResponseType(Response response){
        if (response == null) return 0;
        return response.type;
    }

    public Vector<String> getReservations(Response response){
        if (response == null) return null;
        return response.reservations;
    }

    public Hashtable<String, String> getSettings(Response response){
        if (response == null) return null;
        return response.settings;
    }

    private static String calendarToString(Calendar cal) {
        String sm = "" + (cal.get(Calendar.MONTH) + 1);
        if (sm.length() == 1) {
            sm = "0" + sm;
        }
        String sd = "" + cal.get(Calendar.DATE);
        if (sd.length() == 1) {
            sd = "0" + sd;
        }
        String sh = "" + cal.get(Calendar.HOUR_OF_DAY);
        if (sh.length() == 1) {
            sh = "0" + sh;
        }
        String smin = "" + cal.get(Calendar.MINUTE);
        if (smin.length() == 1) {
            smin = "0" + smin;
        }
        String time = "" + cal.get(Calendar.YEAR) + "-" + sm + "-" + sd + " " + sh + ":" + smin;
        return time;
    }
}
