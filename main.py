import asyncio

from core.tester import LoadTester


def get_positive_int(message):
    while True:
        try:
            value = int(input(message))

            if value > 0:
                return value

            print("مقدار باید بیشتر از صفر باشد.")

        except ValueError:
            print("لطفاً یک عدد صحیح وارد کنید.")


def get_url():
    while True:
        url = input("Target URL: ").strip()

        if url.startswith("http://") or url.startswith("https://"):
            return url

        print("آدرس باید با http:// یا https:// شروع شود.")


def print_report(report):
    print()
    print("=" * 45)
    print("             TEST RESULT")
    print("=" * 45)

    print(f"Requests       : {report['total_requests']}")
    print(f"Successful     : {report['successful_requests']}")
    print(f"Failed         : {report['failed_requests']}")

    print(f"Success Rate   : {report['success_rate']:.2f}%")

    print(
        f"Average        : "
        f"{report['average_response_time'] * 1000:.2f} ms"
    )

    print(
        f"Minimum        : "
        f"{report['minimum_response_time'] * 1000:.2f} ms"
    )

    print(
        f"Maximum        : "
        f"{report['maximum_response_time'] * 1000:.2f} ms"
    )

    print(f"RPS            : {report['requests_per_second']:.2f}")
    print(f"Duration       : {report['duration']:.2f} sec")

    print("=" * 45)


async def main():
    print("=" * 45)
    print("          SAFE LOAD TESTER v1.0")
    print("=" * 45)
    print()

    print("Use this tool only on systems you are")
    print("authorized to test.")
    print()

    url = get_url()

    users = get_positive_int(
        "Concurrent Users: "
    )

    rps = get_positive_int(
        "Requests Per Second: "
    )

    duration = get_positive_int(
        "Test Duration (seconds): "
    )

    timeout = get_positive_int(
        "Request Timeout (seconds): "
    )

    print()
    print("Starting test...")
    print()

    tester = LoadTester(
        url=url,
        users=users,
        rps=rps,
        duration=duration,
        timeout=timeout,
    )

    report = await tester.run()

    print_report(report)


if __name__ == "__main__":
    asyncio.run(main())
