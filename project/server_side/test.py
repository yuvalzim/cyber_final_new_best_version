import os
import subprocess
import threading


def execute_rtm_engine():
    process_rtm = subprocess.Popen(["C:\\Users\\user\\source\\repos\\Project1\\x64\\Release\\project1.exe", "downloads"], stdout=subprocess.PIPE, universal_newlines=True)

    def read_output():
        while True:
            output_line = process_rtm.stdout.readline()
            if output_line == '' and process_rtm.poll() is not None:
                break
            if output_line:
                print(output_line)

        process_rtm.stdout.close()

        # Start reading output in a separate thread

    output_reader = threading.Thread(target=read_output)
    output_reader.daemon = True  # Daemonize the thread, so it terminates when the main thread terminates
    output_reader.start()


def main():
    execute_rtm_engine()
    while True:
        pass


if __name__ == '__main__':
    main()
