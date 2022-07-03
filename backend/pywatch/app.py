import json
import os
import threading
from flask import Flask, Response, jsonify
from file_watchdog import get_watcher

#  the directory to monitor
# dir_to_watch = os.environ.get("DIR_TO_WATCH", "/home/aditya/aditya_kuchekar/watchdog")
dir_to_watch = "/datavol"
#  queue used to store events pushed by watchdog. Objects from this queue are streamed to the server as SSE
queue = []
#  flag indicating connection should be kept alive or closed
keep_alive = False

watcher_thread = threading.Thread(target=get_watcher, args=(dir_to_watch, queue,))
watcher_thread.start()
watcher_thread.join()

app = Flask(__name__)


def add_cors_header(r):
    """
    adds cors headers to the response object
    :param r: response object
    :return: response object
    """
    r.headers.add_header("Access-Control-Allow-Origin", "*")
    r.headers.add_header("Access-Control-Allow-Headers", "*")
    r.headers.add_header("Access-Control-Allow-Methods", "*")
    return r


@app.route("/file-list", methods=["GET"])
def get_files():
    """
    SSE: Server Sent Events
    fetches initial list of files from directory to watch. makes keep alive true and returns files
    :return: return a list of files present in the directory to watch
    """
    global keep_alive
    keep_alive = True
    curr_dir_list = [f for f in os.listdir(dir_to_watch)]
    r = jsonify(curr_dir_list)
    r = add_cors_header(r)
    return r


@app.route("/close", methods=["GET"])
def close_connection():
    """
    Closes the current connection
    :return: returns a message saying connection closed
    """
    global keep_alive
    keep_alive = False
    r = jsonify({"message": "Conenction Closed"})
    r = add_cors_header(r)
    return r


@app.route("/events")
def stream():
    """
    This is a generator pattern. Events are streamed to the client using eventStream function
    :return: returns a event as response to client. this event is polled from the queue (file creation/deletion)
    """
    def eventStream():
        while keep_alive:
            # Poll data from watcher queue which has the directory change events
            while queue:
                event = queue.pop(0)
                data = json.dumps(event)
                yield f"data: {data}\n\n"

        res = json.dumps({"message": "Conenction Closed"})
        yield f"data: {res}\n\n"

    r = Response(eventStream(), mimetype="text/event-stream")
    r = add_cors_header(r)
    return r


if __name__ == "__main__":
    watcher_thread = threading.Thread(target=get_watcher, args=(dir_to_watch, queue,))
    watcher_thread.start()
    app.run(debug=True)
    watcher_thread.join()



