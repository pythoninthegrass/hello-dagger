#!/usr/bin/env python

import anyio
import dagger
import random
import subprocess
import sys
from pathlib import Path

tld = subprocess.check_output(["git",
                               "rev-parse",
                               "--show-toplevel"]
                               ).decode().strip()
ctx = str(Path(tld).resolve())


async def main():
    config = dagger.Config(log_output=sys.stdout)

    async with dagger.Connection(config) as client:
        # set build context (default: ".")
        context_dir = client.host().directory(ctx)

        # build using Dockerfile
        image_ref = (
            await context_dir.docker_build()
            .publish(f"ttl.sh/hello-dagger-{random.randint(0, 10000000)}")
        )

    print(f"Published image to: {image_ref}")


anyio.run(main)
