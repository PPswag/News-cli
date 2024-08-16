# news-cli

pythonic news getter and aggregator

## Development instructions

`news-cli` uses [Nix](https://nixos.org) for managing dependencies to guarantee
reproducible builds. You should install Nix using your preferred method. We
recommend the
[Determine Nix Installer](https://github.com/DeterminateSystems/nix-installer).

Once you have Nix installed, simply enter `cd` into this directory and run:

```bash
nix develop
```

This may take a while, as `nix` will recompile all of the dependencies from
source on your machine. Grab a coffee.

Once the command completes, you will be placed into a development environment in
which you have access to the correct version of `python` with all of the project
dependencies available.

We do not use any Python virtualenvs. All development and build environments are
managed by `nix`, which is vastly superior to Pythonic virtualenv techniques.

Please note that you should NOT use the `poetry` tool directly to install any
dependencies. The `pyproject.toml` and `poetry.lock` are read by `poetry2nix` so
that `nix` can fetch the proper dependencies.

To add new dependencies, run the following command:

```bash
nix run nixpkgs#poetry -- add dependency-name --lock
```

Poetry will automatically resolve dependencies and update `pyproject.toml` and
`poetry.lock`. Then simply execute `nix develop` again to enter a development
shell with the new dependencies.
