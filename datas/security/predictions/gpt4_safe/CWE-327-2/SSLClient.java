import javax.net.ssl.SSLSocket;
import javax.net.ssl.SSLSocketFactory;
import java.io.IOException;
import java.net.InetAddress;
import java.net.Socket;

public class SSLClient {

    public static SSLSocket connect(String host, int port) {
        SSLSocket sslSocket = null;
        try {
            SSLSocketFactory sslSocketFactory = (SSLSocketFactory) SSLSocketFactory.getDefault();
            sslSocket = (SSLSocket) sslSocketFactory.createSocket(host, port);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return sslSocket;
    }
}