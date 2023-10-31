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

            # tell me more about the connection
            print(s)

            while True:

                # Wait for the user to enter control commands.
                msg = input(">>> please input SDK cmd: ")

                # When the user enters Q or q, exit the current program.
                if msg.upper() == 'Q':
                        break

                # Add the ending character.
                msg += ';'

                # Send control commands to the robot.
                r=s.send(msg.encode('utf-8'))
                print(r)

                try:
                    # Wait for the robot to return the execution result.
                    buf = s.recv(1024)

                    print(buf.decode('utf-8'))
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
