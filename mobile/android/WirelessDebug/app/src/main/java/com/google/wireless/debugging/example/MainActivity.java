package com.google.wireless.debugging.example;

import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import com.google.wireless.debugger.WirelessDebugger;
import com.google.wireless.debugging.R;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        WirelessDebugger.start("NA", 500, getApplicationContext());

        setContentView(R.layout.activity_fragment);

        FragmentManager fm = getSupportFragmentManager();
        Fragment fragment = fm.findFragmentById(R.id.fragment_container);

        if (fragment == null){
            fragment = new MainFragment();
            fm.beginTransaction().add(R.id.fragment_container, fragment).commit();
        }

    }
}
