import javax.net.ssl.SSLSocket;
import javax.net.ssl.SSLSocketFactory;
import java.io.IOException;
import java.net.InetAddress;
import java.net.Socket;

public class SSLClient {

    public static Socket connect(String host, int port) {
        Socket socket = null;
        try {
            SSLSocketFactory factory = (SSLSocketFactory) SSLSocketFactory.getDefault();
            socket = factory.createSocket(host, port);
            ((SSLSocket) socket).startHandshake();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return socket;
    }
}