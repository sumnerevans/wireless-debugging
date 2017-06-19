package live.flume.sample;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v7.app.AppCompatActivity;
import live.flume.wireless.debugger.WirelessDebugger;


public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        /*
         * Call to start wireless debugging
         * Params:
         * String - Hostname/IP of the server to send logs to
         * String - Your Key
         * Context - context for the application
         */
        WirelessDebugger.start(R.string.wireless_debug_server, R.string.wireless_debug_api_key,
                getApplicationContext());
        setContentView(R.layout.activity_fragment);

        FragmentManager fm = getSupportFragmentManager();
        Fragment fragment = fm.findFragmentById(R.id.fragment_container);

        if (fragment == null){
            fragment = new MainFragment();
            fm.beginTransaction().add(R.id.fragment_container, fragment).commit();
        }
    }
}
