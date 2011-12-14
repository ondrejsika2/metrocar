package metrocar.carUnit.gps;

import java.util.Date;

/**
 * Base class for saving GPS location. This class holds Latitude, Longitude, Speed,
 * Course, Horizontal accuracy, Vertical accuracy and Timestamp data.
 *
 * This implementation is platform-independent.
 * 
 * @author Lubos Krcal
 */
public class Position {

    private double latitude;
    private double longitude;
    private double speed;
    private double course;
    private double haccuracy;
    private double vaccuracy;
    private long timestamp;

    protected Position(){};

    public Position(double latitude, double longitude, double speed,
            double course, double haccuracy, double vaccuracy, long timestamp){
        this.latitude = latitude;
        this.longitude = longitude;
        this.haccuracy = haccuracy;
        this.vaccuracy = vaccuracy;
        this.speed = speed;
        this.course = course;
        this.timestamp = timestamp;
    }

    public double getCourse() {
        return course;
    }

    public double getHorizontalAccuracy() {
        return haccuracy;
    }

    public double getLatitude() {
        return latitude;
    }

    public double getLongitude() {
        return longitude;
    }

    public double getSpeed() {
        return speed;
    }

    public long getTimestamp() {
        return timestamp;
    }

    public double getVerticalAccuracy() {
        return vaccuracy;
    }

    public Date getDate(){
        return new Date(timestamp);
    }

}

