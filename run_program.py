import sys
import socket

host = "192.168.2.1"
port = 40923


def main():

        address = (host, int(port))

        # Establish a TCP connection with the control command port of the robot.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:



            print("Connecting...")

            s.connect(address)

            print("Connected!")

            # read script from file
            with open('star', 'r') as f:
                script = f.read()

            # send command
            s.send("command;".encode('utf-8'))

            # Send control commands to the robot.
            for line in script.splitlines():
                line = f"chassis move {line};"
                print(line)
                s.send(line.encode('utf-8'))
                try:
                    # Wait for the robot to return the execution result.
                    buf = s.recv(1024)
                    print(buf.decode('utf-8'))
                    # wait for command to finish
                    if line.startswith("chassis move"):
                        while True:
                            buf = s.recv(1024)
                            print(buf.decode('utf-8'))
                            if buf.decode('utf-8').startswith("OK"):
                                break
                except socket.error as e:
                    print("Error receiving :", e)
                    sys.exit(1)
                if not len(buf):
                        break

            # Disconnect the port connection.
            s.shutdown(socket.SHUT_WR)
            s.close()

if __name__ == '__main__':
        main()
