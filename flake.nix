/*
 * Copyright (c) 2024 Youwen Wu
 * SPDX-License-Identifier: BSD-3-Clause
 */
{
  description = "Develoment and build environment for news-cli";

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
      # we override these dependencies so they build properly, since they fail
      # # to specify their full build closures.
      buildOverrides =
        pkgs.poetry2nix.defaultPoetryOverrides.extend
        (self: super: {
          confection =
            super.confection.overridePythonAttrs
            (
              old: {
                buildInputs = (old.buildInputs or []) ++ [super.setuptools];
              }
            );
          certifi =
            super.certifi.overridePythonAttrs
            (
              old: {
                buildInputs = (old.buildInputs or []) ++ [super.setuptools];
              }
            );
          newspaper4k =
            super.newspaper4k.overridePythonAttrs
            (
              old: {
                buildInputs = (old.buildInputs or []) ++ [super.poetry];
              }
            );
        });
    in {
      formatter = pkgs.alejandra;

      defaultPackage = pkgs.poetry2nix.mkPoetryApplication {
        projectDir = ./.;
        python = pkgs.python311;
        overrides = buildOverrides;
      };

      devShells.default = pkgs.mkShell {
        shellHook = "echo 'Welcome to the Python development environment! In here, you will be able to execute code with the necessary dependencies.'";
        buildInputs = with pkgs; [
          (pkgs.poetry2nix.mkPoetryEnv {
            projectDir = ./.;
            python = pkgs.python311;
            editablePackageSources = {news-cli = ./src;};
            overrides = buildOverrides;
          })
        ];
      };
    });
}
