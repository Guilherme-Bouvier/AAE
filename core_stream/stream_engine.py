import time
import threading


class StreamEngine:

    def __init__(self, scraper, callback, interval=2):

        self.scraper = scraper
        self.callback = callback
        self.interval = interval
        self.running = False

    def _run(self):

        while self.running:

            try:
                value = self.scraper.get_latest()

                if value:
                    self.callback(value)

            except Exception as e:
                print("Erro stream:", e)

            time.sleep(self.interval)

    def start(self):

        self.running = True
        thread = threading.Thread(target=self._run)
        thread.daemon = True
        thread.start()

    def stop(self):

        self.running = False