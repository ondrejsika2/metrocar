package metrocar.carUnit;

public class Core {

    /** Common message severity. Default. */
    public static final int LOG_NOTE = 1;
    /** Uncommon state that signals possible or minor problems. */
    public static final int LOG_WARNING = 2;
    /** Error that is handled by application, so that the application recovers
     * and continues it's execution. */
    public static final int LOG_ERROR = 4;
    /** Critical error from which the application cannot recover. */
    public static final int LOG_FATAL = 8;

    /** Request/response enum element for reservations */
    public static final int PROTOCOL_RESERVATIONS = 1;
    /** Request/response enum element for settings */
    public static final int PROTOCOL_SETTINGS = 2;
    /** Send GPS data in server reuqest */
    public static final int PROTOCOL_DATA = 4;
    /** Send a journey starting date in server request */
    public static final int PROTOCOL_SINCE = 8;
    /** Send a journey end date in server request */
    public static final int PROTOCOL_TILL = 16;
    
	public static final String authKey = "test";
	public static final int imei = 123123123;


}
