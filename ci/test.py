#!/usr/bin/env python

import anyio
import dagger
import sys

docker_image = "node:16-slim"


async def main():
    config = dagger.Config(log_output=sys.stdout)

    async with dagger.Connection(config) as client:
        source = (
            client.container()
            .from_(docker_image)
            .with_directory(
                "/src",
                client.host().directory("."),
                exclude=["node_modules/", "ci/"],
            )
        )

        # workdir and install dependencies
        runner = source.with_workdir("/src").with_exec(["npm", "install"])

        # run app tests
        out = await runner.with_exec(
            ["npm",
             "test",
             "--",
             "--watchAll=false"]
        ).stderr()
        print(out)

anyio.run(main)
