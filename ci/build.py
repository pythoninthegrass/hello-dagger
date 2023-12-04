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
                exclude=["node_modules/", "ci/"]
            )
        )

        runner = source.with_workdir("/src").with_exec(["npm", "install"])

        test = runner.with_exec(["npm", "test", "--", "--watchAll=false"])

        build_dir = (
            test.with_exec(["npm", "run", "build"])
            .directory("./build")
        )

        await build_dir.export("./build")

        e = await build_dir.entries()
        print(f"build dir contents:\n{e}")


anyio.run(main)
