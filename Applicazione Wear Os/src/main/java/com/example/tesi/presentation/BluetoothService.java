package com.example.tesi.presentation;

import android.annotation.SuppressLint;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.Service;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.Intent;
import android.os.Binder;
import android.os.IBinder;

import androidx.core.app.NotificationCompat;

import com.example.tesi.R;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.UUID;

public class BluetoothService extends Service {

    private final IBinder binder = new BluetoothBinder();
    private BluetoothSocket bluetoothSocket;

    // Crea classe interna
    public class BluetoothBinder extends Binder {
        BluetoothService getService() {
            return BluetoothService.this;
        }
    }

    // Combina Activity e Service
    @Override
    public IBinder onBind(Intent intent) {
        return binder;
    }

    // Crea il canale di notifica per lo scambio di dati
    private void createNotificationChannel() {
        NotificationChannel channel = new NotificationChannel(
                "1",
                "Bluetooth Notifications",
                NotificationManager.IMPORTANCE_HIGH
        );
        NotificationManager manager = getSystemService(NotificationManager.class);
        manager.createNotificationChannel(channel);
    }

    // Crea la struttura della notifica
    private Notification buildNotification(String message) {
        return new NotificationCompat.Builder(this, "1")
                .setContentTitle("Bluetooth Service")
                .setContentText(message)
                .setSmallIcon(R.drawable.splash_icon)
                .build();
    }

    // Funzione che svolge l'applicazione quando avviata
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        createNotificationChannel();
        startForeground(1, buildNotification("Ricezione notifiche da bluetooth attiva"));

        String bluetooth_interface = "5C:F3:70:60:E2:A1";
        BluetoothDevice device = BluetoothAdapter.getDefaultAdapter().getRemoteDevice(bluetooth_interface);

        connectToDevice(device);

        return START_STICKY;
    }


    // Connessione al Raspberry
    @SuppressLint("MissingPermission")
    private void connectToDevice(BluetoothDevice device) {
        UUID uuid = UUID.fromString("0000111e-0000-1000-8000-00805f9b34fb");
        try {
            bluetoothSocket = device.createRfcommSocketToServiceRecord(uuid);
            bluetoothSocket.connect();

            receiveNotifications();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Permette di ricevere i dati e leggerli
    private void receiveNotifications() {
        try {
            InputStream inputStream = bluetoothSocket.getInputStream();
            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));

            while (true) {
                String receivedNotification = bufferedReader.readLine();
                if (receivedNotification != null) {
                    showNotification(receivedNotification);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Permette di mostrare la notifica a schermo
    private void showNotification(String message) {
        Notification notification = buildNotification(message);
        NotificationManager notificationManager = getSystemService(NotificationManager.class);
        notificationManager.notify(1, notification);
    }

    // Distrugge il componente Service e interrompe la connessione
    @Override
    public void onDestroy() {
        super.onDestroy();
        try {
            if (bluetoothSocket != null) {
                bluetoothSocket.close();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}