{
  description = "A basic nix + flake + poetry example";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs";
  inputs.utils.url = "github:numtide/flake-utils";
  inputs.poetry2nix.url = "github:nix-community/poetry2nix";

  outputs = {
    nixpkgs,
    utils,
    poetry2nix,
    self,
  }:
    utils.lib.eachDefaultSystem (system: let
      pkgs =
        nixpkgs.legacyPackages.${system}.extend poetry2nix.overlays.default;
    in {
      formatter = pkgs.alejandra;

      defaultPackage =
        pkgs.poetry2nix.mkPoetryApplication {projectDir = ./.;};

      devShells.default = pkgs.mkShell {
        shellHook = "echo 'Welcome to the Python development environment! In here, you will be able to execute code with the necessary dependencies.'";
        buildInputs = with pkgs; [
          (pkgs.poetry2nix.mkPoetryEnv {
            projectDir = ./.;

            editablePackageSources = {my-app = ./src;};
          })
        ];
      };
    });
}
