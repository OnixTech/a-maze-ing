{
  description = "Nix flake for fly-in";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];

      perSystem = { pkgs, ... }:
        let
          x11Libs = with pkgs; [ libX11 libXrandr libXi libXcursor libXinerama libXext libxcb ];
          glLibs  = with pkgs; [ mesa libGL libGLU glfw ];
          fontLibs = with pkgs; [ freetype fontconfig ];
        in {
          devShells.default = pkgs.mkShell {
            packages = with pkgs; [ python313 uv ruff python313Packages.flake8 python313Packages.mypy ] ++ glLibs ++ x11Libs ++ fontLibs;
            env = {
              LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath (
                [ pkgs.stdenv.cc.cc.lib ] ++ glLibs ++ x11Libs ++ fontLibs
              );
              UV_PYTHON_DOWNLOADS = "never";
              UV_PYTHON = "${pkgs.python313}/bin/python3.13";
            };
          };
        };
    };
}
