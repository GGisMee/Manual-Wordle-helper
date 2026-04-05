{ pkgs ? import <nixpkgs> {} }:
let
  python-env = pkgs.python313.withPackages (ps: with ps; [
    numpy
    scipy
    matplotlib
    tkinter
    debugpy
  ]);
in
pkgs.mkShell {
  buildInputs = [
    python-env
    pkgs.tcl
    pkgs.tk
    pkgs.libGL
    pkgs.libxkbcommon
    pkgs.wayland
    pkgs.stdenv.cc.cc.lib
  ];

  shellHook = ''
    export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath [ pkgs.libGL pkgs.libxkbcommon pkgs.wayland pkgs.stdenv.cc.cc.lib ]}"
    export TCL_LIBRARY="${pkgs.tcl}/lib/tcl8.6"
    export TK_LIBRARY="${pkgs.tk}/lib/tk8.6"
  '';
}
