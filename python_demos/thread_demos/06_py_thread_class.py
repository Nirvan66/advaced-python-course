import threading

class DoItThread(threading.Thread):

    def __init__(self, msg: str):
        threading.Thread.__init__(self)
        self.msg = msg
    
    def run(self) -> None:
        print(dir(self))
        print(self._kwargs)
        print(f"{self.msg} {threading.get_native_id()}")

print(f"main thread id:{threading.get_native_id()}")
some_thread = DoItThread("Message of ")
some_thread.start()
some_thread.join()
