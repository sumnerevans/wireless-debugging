package com.google.wireless.debugger;

import android.support.test.runner.AndroidJUnit4;
import junit.framework.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;


@RunWith(AndroidJUnit4.class)
public class WebSocketConnectionTest {

    private static final String TEST_IP = "IP_HERE";

    @Test
    public void testConnection(){

        WebSocketMessenger wsmNull = WebSocketMessenger
                .buildNewConnection("local host", 500);

        WebSocketMessenger wsmNotRunning = WebSocketMessenger
                .buildNewConnection(TEST_IP, 500);

        WebSocketMessenger wsmCorrect = WebSocketMessenger
                .buildNewConnection(TEST_IP, 500);

        // Sleep to give time to try to connect
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        Assert.assertNull(wsmNull);

        Assert.assertNotNull(wsmNotRunning);
        Assert.assertFalse(wsmNotRunning.isRunning());

        Assert.assertNotNull(wsmCorrect);
        Assert.assertTrue(wsmCorrect.isRunning());
    }

}
