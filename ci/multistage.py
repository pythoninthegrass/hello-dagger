#!/usr/bin/env python

import anyio
import dagger
import random
import sys

node_image = "node:16-slim"
nginx_image = "nginx:1.23-alpine"


async def main():
    config = dagger.Config(log_output=sys.stdout)

    async with dagger.Connection(config) as client:
        source = (
            client.container()
            .from_(node_image)
            .with_directory(
                "/src",
                client.host().directory("."),
                exclude=["node_modules/", "ci/"]
            )
        )

        runner = source.with_workdir("/src").with_exec(["npm", "install"])

        test = runner.with_exec(["npm",
                                 "test",
                                 "--",
                                 "--watchAll=false"])

        # first stage
        build_dir = test.with_exec(["npm",
                                    "run",
                                    "build"]).directory("./build")

        # second stage
        image_ref = await (
            client.container()
            .from_(nginx_image)
            .with_directory("/usr/share/nginx/html", build_dir)
            .publish(f"ttl.sh/hello-dagger-{random.randint(0, 10000000)}")
        )

    print(f"Published image to: {image_ref}")


anyio.run(main)
