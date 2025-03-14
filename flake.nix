{
  description = "Python devshell";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    system = "x86_64-linux";
    pkgs = import nixpkgs {
      inherit system;
      config = {
        allowUnfree = true;
      };
    };

    libs = [
      pkgs.stdenv.cc.cc.lib
      pkgs.zlib
    ];

    shell = pkgs.mkShell {
      packages = with pkgs; [
        python312
        uv
        just
      ];
      env = {
        CC = "${pkgs.gcc}/bin/gcc";
        LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath libs;

        UVICORN_LOG_LEVEL = "debug";
        DEBUGPY = "true";
      };
    };
  in {
    devShells.${system}.default = shell;
  };
}