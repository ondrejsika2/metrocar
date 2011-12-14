package metrocar.carUnit.gps;

import java.util.TimerTask;
import java.util.Vector;

/**
 * This task sends all GPS data to server in defined intervals. It takes all
 * data 'to send' from system, sends those to server, and if successful, deletes
 * those data from 'to send' list.
 * @author Lubos Krcal
 */
public class SendGPSTask extends TimerTask{

    public SendGPSTask(){

    }

    public void run() {
    }

}
