#!/usr/bin/env python

import anyio
import dagger
import sys

docker_image = "python:3.11-slim"


async def main():
    config = dagger.Config(log_output=sys.stdout)

    # initialize dagger client
    async with dagger.Connection(config) as client:
        # get version
        python = (
            client.container()
            .from_(docker_image)
            .with_exec(
                ["python", "-V"]
            )
        )

        # execute
        version = await python.stdout()

    # print output
    print(f"Hello from Dagger and {version}")


anyio.run(main)
