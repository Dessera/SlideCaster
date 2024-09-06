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
              python312
              poetry
              black

              nil
              nixpkgs-fmt
            ] ++ (with pkgs.python312Packages; [
              pip
              venvShellHook
            ]);

            # envs for mediapipe
            LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib:${pkgs.libGL}/lib:${pkgs.glib.out}/lib";
          };
        };
    };
}
