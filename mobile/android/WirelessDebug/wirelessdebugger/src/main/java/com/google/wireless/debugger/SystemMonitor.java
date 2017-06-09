package com.google.wireless.debugger;

import android.util.Log;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

/**
 * System Monitor compiles CPU usage, Memory usage, and Network usage by reading from /proc.
 */
class SystemMonitor {

    private static final String TAG = "System Monitor";
    private static final String PROC_ROOT = "/proc/";
    private static final String PROC_STAT = PROC_ROOT + "stat";
    private static final String PROC_MEMINFO = PROC_ROOT + "meminfo";
    private static final String PROC_NET_DEV = PROC_ROOT + "net/dev";
    private static final String REGEX_WHITESPACE = "\\s+";
    private static final int TOTAL_SYSTEM_TIME = 0;
    private static final int TOTAL_TIME = 1;
    private static final int NETWORK_BYTES_SENT_COLUMN = 9;
    private static final int NETWORK_BYTES_RECEIVED_COLUMN = 1;
    private static final int MEMORY_TOTAL_LINE = 0;
    private static final int MEMORY_USED_LINE = 5;

    private int[] mPreviousCpuStats = new int[2];
    private long mLastBytesSentTime;
    private long mLastBytesReceivedTime;
    private int mPreviousBytesSent;
    private int mPreviousBytesReceived;

    /**
     * Creates a new System Monitor and reads initial system state
     */
    public SystemMonitor() {
        ArrayList<String> cpuStatLines = getFileLines(PROC_STAT);
        if (!cpuStatLines.isEmpty()) {
            String firstLine = cpuStatLines.get(0);
            mPreviousCpuStats = parseCpuLine(firstLine);
        }
        mPreviousBytesSent = getSentBytes();
        mLastBytesSentTime = System.currentTimeMillis();
        mPreviousBytesReceived = getReceivedBytes();
        mLastBytesReceivedTime = System.currentTimeMillis();
    }

    /**
     * Reads the specified file and returns its lines as an array list of Strings.
     * @param path Full path to the file.
     * @return Array List of Strings, each entry is one line in the file.
     */
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

    /**
     * Returns the CPU Usage as a decimal.
     * @return CPU usage as decimal (must multiply by 100 to get it as a percentage).
     */
    public double getCpuUsage() {
        ArrayList<String> cpuStatLines = getFileLines(PROC_STAT);
        if (cpuStatLines.isEmpty()) {
            Log.d(TAG, "cpuStatLines is Empty");
            return 0.0;
        }

        int[] currentCpuStats = parseCpuLine(cpuStatLines.get(0));

        int systemUsage = currentCpuStats[TOTAL_SYSTEM_TIME] - mPreviousCpuStats[TOTAL_SYSTEM_TIME];
        int totalUsage = currentCpuStats[TOTAL_TIME] - mPreviousCpuStats[TOTAL_TIME];
        // Clamped value taken because sometimes the the file is read from the past (what!)
        double cpuUsagePercent = Math.abs(systemUsage / (double) totalUsage);
        cpuUsagePercent = Math.max(0, Math.min(1, cpuUsagePercent));
        mPreviousCpuStats = currentCpuStats;

        return cpuUsagePercent;
    }

    /**
     * Returns the amount of memory (in kilobytes used/active).
     * @return Memory used in kilobytes.
     */
    public int getMemoryUsage() {
        return getMemoryUsageStatFromLine(MEMORY_USED_LINE);
    }

    /**
     * Returns the total amount of memory available on the system.
     * @return Total system memory in kilobytes.
     */
    public int getTotalMemory() {
        return getMemoryUsageStatFromLine(MEMORY_TOTAL_LINE);
    }

    /**
     * Returns the average number of bytes sent over the network per second.
     * @return Bytes per second sent.
     */
    public double getSentBytesPerSecond() {
        int currentBytesSent = getSentBytes();
        long currentTime = System.currentTimeMillis();
        long elapsedMilliseconds = System.currentTimeMillis() - mLastBytesSentTime;
        mLastBytesSentTime = currentTime;
        double bytesPerMillisecond  = (currentBytesSent - mPreviousBytesSent) /
                (double) elapsedMilliseconds;

        mPreviousBytesSent = currentBytesSent;

        return bytesPerMillisecond * (1000 / elapsedMilliseconds );
    }

    /**
     * Returns the average number of bytes received over the network per second.
     * @return Bytes per second received.
     */
    public double getReceivedBytesPerSecond() {
        int currentBytesReceived = getReceivedBytes();
        long currentTime = System.currentTimeMillis();
        long elapsedMilliseconds = System.currentTimeMillis() - mLastBytesReceivedTime;
        mLastBytesReceivedTime = currentTime;
        double bytesPerMillisecond  = (currentBytesReceived - mPreviousBytesReceived) /
                (double) elapsedMilliseconds;

        mPreviousBytesReceived = currentBytesReceived;

        return bytesPerMillisecond * (1000 / elapsedMilliseconds );
    }

    /**
     * Returns the total number of bytes sent.
     * @return Bytes sent.
     */
    private int getSentBytes() {
        return sumNetworkUsageColumn(NETWORK_BYTES_SENT_COLUMN);
    }

    /**
     * Returns the total number of bytes received.
     * @return Bytes received.
     */
    private int getReceivedBytes() {
        return sumNetworkUsageColumn(NETWORK_BYTES_RECEIVED_COLUMN);
    }

    /**
     * Parses line to get total time and total system time from the CPU.
     * @param line Line of cpu information to be parsed.
     * @return Returns int[2], with the first value being total system time and second being
     * total time.
     */
    private int[] parseCpuLine(String line) {
        String[] lineParts = line.split(REGEX_WHITESPACE);
        int[] times = new int[2];

        int timeUser = Integer.parseInt(lineParts[1]);
        int timeNice = Integer.parseInt(lineParts[2]);
        int timeSystem = Integer.parseInt(lineParts[3]);
        int timeIdle = Integer.parseInt(lineParts[4]);
        int timeIoWait = Integer.parseInt(lineParts[5]);
        int timeIrq = Integer.parseInt(lineParts[6]);
        int timeSoftIrq = Integer.parseInt(lineParts[7]);
        int timeSteal = Integer.parseInt(lineParts[8]);

        int totalIdleTime = timeIdle + timeIoWait;
        int totalTime = totalIdleTime + timeIrq + timeSoftIrq + timeSystem + timeSteal + timeUser
                + timeNice;

        times[TOTAL_SYSTEM_TIME] = totalTime - totalIdleTime;
        times[TOTAL_TIME] = totalTime;
        return times;
    }

    /**
     * Returns the memory usage number from a line of text.
     * @param line Line containing memory information.
     * @return Number of kilobytes used in memory.
     */
    private int getMemoryUsageStatFromLine(int line) {
        ArrayList<String> memInfoLines = getFileLines(PROC_MEMINFO);
        if (memInfoLines.isEmpty()){
            return 0;
        }

        String[] firstLineParts = memInfoLines.get(line).split(REGEX_WHITESPACE);
        return Integer.parseInt(firstLineParts[1]);
    }

    /**
     * Sums the amount of bytes across a column.  Used to get total bytes sent/received across
     * the network from every networking adapter.
     * @param column Column to sum across.
     * @return Total number of bytes in the column.
     */
    private int sumNetworkUsageColumn(int column){
        ArrayList<String> networkFileLines = getFileLines(PROC_NET_DEV);
        int totalBytes = 0;

        // Remove first two lines from the /proc/net/dev file
        networkFileLines.remove(0);
        networkFileLines.remove(0);

        for (String networkLine : networkFileLines) {
            networkLine = networkLine.substring(networkLine.indexOf(":"));
            String[] networkStats = networkLine.split(REGEX_WHITESPACE);
            totalBytes += Integer.parseInt(networkStats[column]);
        }

        return totalBytes;
    }
}
