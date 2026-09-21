import asyncio
import time

import httpx

from .statistics import Statistics


MAX_USERS = 50
MAX_RPS = 100
MAX_DURATION = 60
MAX_TIMEOUT = 10


class LoadTester:
    def __init__(
        self,
        url,
        users,
        rps,
        duration,
        timeout,
    ):
        self.url = url
        self.users = min(users, MAX_USERS)
        self.rps = min(rps, MAX_RPS)
        self.duration = min(duration, MAX_DURATION)
        self.timeout = min(timeout, MAX_TIMEOUT)

        self.stats = Statistics()

        self.stop_event = asyncio.Event()

    async def send_request(self, client):
        start = time.perf_counter()

        try:
            response = await client.get(self.url)

            elapsed = time.perf_counter() - start

            if 200 <= response.status_code < 400:
                self.stats.add_success(elapsed)
            else:
                self.stats.add_failure(elapsed)

        except Exception:
            elapsed = time.perf_counter() - start
            self.stats.add_failure(elapsed)

    async def worker(self, client):
        while not self.stop_event.is_set():
            await self.send_request(client)

            if self.rps > 0:
                await asyncio.sleep(1 / self.rps)

    async def run(self):
        self.stats.start()

        timeout = httpx.Timeout(self.timeout)

        limits = httpx.Limits(
            max_connections=self.users,
            max_keepalive_connections=self.users,
        )

        async with httpx.AsyncClient(
            timeout=timeout,
            limits=limits,
            follow_redirects=True,
        ) as client:

            workers = [
                asyncio.create_task(self.worker(client))
                for _ in range(self.users)
            ]

            try:
                await asyncio.sleep(self.duration)

            finally:
                self.stop_event.set()

                await asyncio.gather(
                    *workers,
                    return_exceptions=True,
                )

        self.stats.finish()

        return self.stats.get_report()
