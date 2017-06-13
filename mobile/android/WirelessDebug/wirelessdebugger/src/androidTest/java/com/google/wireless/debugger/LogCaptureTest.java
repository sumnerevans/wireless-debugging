package com.google.wireless.debugger;

import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnit;
import org.mockito.junit.MockitoRule;

import static org.mockito.Mockito.*;

public class LogCaptureTest {


    private Thread mLogThread;
    @Mock
    private LogReader mMockLogReader;

    @Rule public MockitoRule mockitoRule = MockitoJUnit.rule();

    @Before
    public void createThread() {
        mMockLogReader = new LogReader("localhost", "none", 200);
        mLogThread = new Thread(mMockLogReader);
    }

    @Test
    public void logStartCapture() {

    }

    @Test
    public void logEndCapture() {


    }

    @Test
    public void crashCapture() {


    }

}
