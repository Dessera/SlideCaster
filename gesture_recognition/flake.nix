{
  description = "SlideCaster controller driven by gesture recognition";

  inputs = {
    nixpkgs = {
      url = "github:nixos/nixpkgs?ref=nixos-unstable";
    };
    flake-parts = {
      url = "github:hercules-ci/flake-parts";
    };
  };

  outputs =
    inputs@{ self
    , nixpkgs
    , flake-parts
    }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      # dev environment only
      # actual deployment is ubuntu arm64
      systems = [ "x86_64-linux" ];

      # Development shell
      perSystem = { config, pkgs, ... }:
        {
          devShells.default = pkgs.mkShell {
              venvDir = "venv";
              packages = with pkgs; [
                python310
                poetry
                black
              ] ++ (with pkgs.python310Packages; [
                pip
                venvShellHook
              ]);
            };
        };
    };
}
