
import logging
import threading
import time


def thread_function(name):

    logging.info(f"thread {name} started")

    time.sleep(2)

    logging.info(f"thread {name} finished")


if __name__ == "__main__":

    format = "%(asctime)s.%(msecs)03d %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(format=format, level=logging.INFO, datefmt=datefmt)

    logging.info("main create threads")

    # create threads
    threads = []

    for i in range(10):

        threads.append(threading.Thread(target=thread_function, args=(i,)))

    logging.info("main start threads")

    # start all threads
    [t.start() for t in threads]

    logging.info("main wait for threads")

    # wait for all threads
    [t.join() for t in threads]

    logging.info("main end")
