package metrocar.carUnit;

import java.util.Hashtable;

/**
 * Class for storing settings
 * @author JPEXS
 */
public class Settings {

    // --- GPS
    /** Requested accurancy of GPS receiver in meters */
    public static double GPSAccurancy = 30.0;

    // --- SYSTEM
    /** Interval between attempts to get GPS time. In miliseconds.*/
    public static long SYSTEM_TASK_GPSTIME_PERIOD = 10000;
    /** Interval between checking GPS for location. In miliseconds */
    public static long SYSTEM_TASK_GPSREAD_PERIOD = 3000;

    /** Minimal distance for saving location to the list in meters */
    public static float minDistanceLocation = 2.0F; //2 meters
    /** Time interval for saving location to the list in milliseconds */
    public static long minTimeLocation = 5 * 1000; //5 seconds
    /** Interval between sending locations to the server in miliseconds */
    public static long locationSendInterval = 30 * 1000; //30 seconds
    
     /** Distance method : calculate distance between locations in the list ONLY */
    public static final int DM_ONLYSTORED = 0;
    /** Distance method : calculate distance between all location even if it is not stored*/
    public static final int DM_ALL = 1;
    /** Method for calculating distance (see DM_* constants) */
    public static int distanceMethod = DM_ALL; //DM_ONLYSTORED;

    // --- LOGGING
    /** Use logging features */
    public static boolean LOGGER_USE_STDLOG = true;
    /** Use GPS logging features */
    public static boolean LOGGER_USE_GPSLOG = true;
    /** Log up to note/warning/error
     * OR connected: means that ( LOG_WARNING | LOG_ERROR | LOG_FATAL)
     * all but most common notes are logged */
    public static int LOGGER_LEVEL =
            (Core.LOG_NOTE | Core.LOG_WARNING | Core.LOG_ERROR | Core.LOG_FATAL);
    /** Path for logging */
    public static String LOGGER_STDLOG_PATH = "a:/log/";
    public static String LOGGER_GPSLOG_PATH = "a:/gps/";
    /** Log to file in FFS */
    public static boolean LOGGER_LOG_TO_FILE = true;
    /** Log via System.out.println too */
    public static boolean LOGGER_LOG_TO_STDOUT = true;
    /** Log special location flags */
    public static boolean LOGGER_LOG_GPSLOG_FLAGS = false;
    /** Maximal size of the log file - new file created when this exceeds */
    public static long LOGGER_MAX_STDLOG_SIZE = 20 * 1024;
    public static long LOGGER_MAX_LOCLOG_SIZE = 20 * 1024;


    // --- SERVER
    /** Server address to send requests to*/
    //public static String serverURL = "http://metrocar.cz/metrocar/server";
    //public static String SERVER_URL = "http://admin.metrocar.dev.vlasta.fragaria.cz/comm";
    public static String SERVER_URL = "http://admin.autonapul.cz/com/xml/";
    //public static String testServerURL = "http://88.208.119.18:80/carsharing/test.php";
    public static String TESTSERVER_URL = "http://147.32.83.48:8080/comm/";
    public static String TESTSERVER_HTTPHOST = "admin.koala.felk.cvut.cz";

    /** Time zone of dates */
    public static String timeZone = "GMT";
    /** GPRS parameters to connect to internet */
    public static String GPRS_URL_PARAMS = "bearer_type=gprs;access_point=internet";


    // ------- CURRENTLY USUSED --------
    /** Retry interval - UNUSED */
    public static long retrySendInterval = 10 * 1000;  //10 seconds;
    /** Echo interval - UNUSED*/
    public static long echoInterval = 50 * 1000; //50 seconds;
    /** Interval between sending usage */
    public static long usageSendInterval = 1000;

    /**
     * Get specified setting or default value (long)
     * @param settingList
     * @param setting Setting idenfificator
     * @param defaultValue Default value to be retrieved when setting does not exist
     * @return setting value or defaultValue if setting is not set
     */
    private static long getSettingLongDef(Hashtable<String, String> settingList, String setting, long defaultValue) {
        if (settingList == null) {
            return defaultValue;
        }
        try {
            return Long.parseLong((String) settingList.get(setting));
        } catch (Exception ex) {
            return defaultValue;
        }
    }

    /**
     * Get specified setting or default value (float)
     * @param settingList List of settings
     * @param setting Setting idenfificator
     * @param defaultValue Default value to be retrieved when setting does not exist
     * @return setting value or defaultValue if setting is not set
     */
    private static float getSettingFloatDef(Hashtable<String, String> settingList, String setting, float defaultValue) {
        try {
            return Float.parseFloat((String) settingList.get(setting));
        } catch (Exception ex) {
            return defaultValue;
        }
    }

    /**
     * Get specified setting or default value (boolean)
     * @param settingList List of settings
     * @param setting Setting idenfificator
     * @param defaultValue Default value to be retrieved when setting does not exist
     * @return setting value or defaultValue if setting is not set
     */
    private static boolean getSettingBooleanDef(Hashtable<String, String> settingList, String setting, boolean defaultValue) {
        if (settingList == null) {
            return defaultValue;
        }
        Object o = settingList.get(setting);
        if (o == null) {
            return defaultValue;
        }
        if (o instanceof String) {
            String s = (String) o;
            if (s.toUpperCase().equals("TRUE")) {
                return true;
            }
            if (s.toUpperCase().equals("FALSE")) {
                return false;
            }
            if (s.equals("1")) {
                return true;
            }
            if (s.equals("0")) {
                return false;
            }
        }
        return defaultValue;
    }

    /**
     * Update current settings from HashTable of settings received from server
     * @param settings HashTable of settings
     */
    public static void updateSettings(Hashtable<String, String> settings) {
        //Tested settings:
        //1) minDistanceLocation=10.5 m , minTimeLocation=5s, GPSCheckInterval=0.5s, locationSendInterval=20s
        //2) minDistanceLocation=100 m , minTimeLocation=30s, GPSCheckInterval=0.5s, locationSendInterval=60s
        minDistanceLocation = getSettingFloatDef(settings, "minDistanceLocation", 100F);
        minTimeLocation = getSettingLongDef(settings, "minTimeLocation", 30 * 1000);
        SYSTEM_TASK_GPSREAD_PERIOD = getSettingLongDef(settings, "GPSCheckInterval", 5 * 100);
        locationSendInterval = getSettingLongDef(settings, "locationSendInterval", 60 * 1000);
        retrySendInterval = getSettingLongDef(settings, "retrySendInterval", 10 * 10000);
        echoInterval = getSettingLongDef(settings, "echoInterval", 50 * 10000);
        usageSendInterval = getSettingLongDef(settings, "usageSendInterval", 1000);
        GPSAccurancy = getSettingFloatDef(settings, "GPSAccurancy", 10.0F);
        LOGGER_USE_STDLOG = getSettingBooleanDef(settings, "useLog", true);
        LOGGER_USE_GPSLOG = getSettingBooleanDef(settings, "useGPSLog", false);
        distanceMethod = (int) getSettingLongDef(settings, "distanceMethod", DM_ALL);

    }
}
