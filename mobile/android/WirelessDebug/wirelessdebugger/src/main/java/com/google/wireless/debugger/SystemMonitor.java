package com.google.wireless.debugger;

import android.util.Log;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

class SystemMonitor {

    private static final String TAG = "System Monitor";

    private int[] mPreviousCpuStats = new int[2];

    public SystemMonitor() {
        ArrayList<String> cpuStatLines = getFileLines("/proc/stat");
        if (!cpuStatLines.isEmpty()) {
            String firstLine = getFileLines("/proc/stat").get(0);
            mPreviousCpuStats = parseCpuLine(firstLine);
        }
    }

    private ArrayList<String> getFileLines(String path) {
        ArrayList<String> fileLines = new ArrayList<>();

        try {
            BufferedReader reader = new BufferedReader(new FileReader(path));

            String line;
            while ((line = reader.readLine()) != null) {
                fileLines.add(line);
            }

        } catch (IOException e) {
            Log.e(TAG, e.toString());
        }

        return fileLines;
    }

    public double getCpuUsage() {

        ArrayList<String> cpuStatLines = getFileLines("/proc/stat");

        if (cpuStatLines.isEmpty()) {
            Log.d(TAG, "cpuStatLines is Empty");
            return 0.0;
        }

        int[] currentCpuStats = parseCpuLine(cpuStatLines.get(0));

        double cpuUsagePercent = (double) (currentCpuStats[0] - mPreviousCpuStats[0]) /
                (double) (currentCpuStats[1] - mPreviousCpuStats[1]);

        Log.d(TAG, "0: " + Integer.toString(currentCpuStats[0]) + " 1: "
                + Integer.toString(currentCpuStats[1]) );

        Log.d(TAG, "0: " + Integer.toString(mPreviousCpuStats[0]) + " 1: "
                + Integer.toString(mPreviousCpuStats[1]) );

        mPreviousCpuStats = currentCpuStats;

        return cpuUsagePercent;
    }

    private int[] parseCpuLine(String line) {
        String[] lineParts = line.split("\\s+");
        Log.d(TAG, line);
        int[] times = new int[2];

        int timeUser = Integer.parseInt(lineParts[1]);
        int timeNice = Integer.parseInt(lineParts[2]);
        int timeSystem = Integer.parseInt(lineParts[3]);
        int timeIdle = Integer.parseInt(lineParts[4]);
        int timeIoWait = Integer.parseInt(lineParts[5]);
        int timeIrq = Integer.parseInt(lineParts[6]);
        int timeSoftIrq = Integer.parseInt(lineParts[7]);
        int timeSteal = Integer.parseInt(lineParts[8]);
        int timeGuest = Integer.parseInt(lineParts[9]);
        int timeGuestNice = Integer.parseInt(lineParts[10]);

        int totalIdleTime = timeIdle + timeIoWait;
        int totalTime = totalIdleTime + timeIrq + timeSoftIrq + timeSystem + timeSteal +
                timeGuest + timeGuestNice;

        times[0] = timeUser + timeNice + timeSystem;
        times[1] = times[0] + totalIdleTime;

        return times;
    }

    /* proc/stat
    proc/net/dev
    proc/meminfoq
 */

}