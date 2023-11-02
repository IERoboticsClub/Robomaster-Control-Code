import sys
import socket
import time

host = "192.168.2.1"
port = 40923

VX = 0.5
VY = 0.5
VZ = 100

def sleepCommand(direction, movement):
        """
        calculates the number of seconds for the command to run and sleeps
        """
        velocity = 0
        movement = abs(movement)
        if direction == "x":
                velocity = VX
        elif direction == "y":
                velocity = VY
        elif direction == "z":
                velocity = VZ
        time_to_sleep = movement / velocity
        if direction == "z":
                time_to_sleep += 5

        time_to_sleep+=1
        print(time_to_sleep)
        time.sleep(time_to_sleep)



def main():
    address = (host, int(port))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Connecting...")
        s.connect(address)
        print("Connected!")

        with open('star', 'r') as f:
            script = f.read()

        s.send("command;".encode('utf-8'))
        #pIN: chassis speed x <speed_x> y <speed_y> z <speed_z>
        time.sleep(2)

        for line in script.splitlines():
            print("Running")
            # x 0.5 -- ex
            distance = float(line.split()[1])
            direction = line.split()[0]

            line = f"chassis move {line};"
            print(line)
            s.send(line.encode('utf-8'))
            time.sleep(2)  # Adding a delay of 2 seconds between commands

            sleepCommand(direction, distance)
            try:
                buf = s.recv(1024)
                print(buf.decode('utf-8'))

            except socket.error as e:
                print("Error receiving :", e)
                sys.exit(1)

        s.shutdown(socket.SHUT_WR)
        s.close()

if __name__ == '__main__':
    main()
