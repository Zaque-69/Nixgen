{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    python311Packages.tkinter
    python311Packages.customtkinter
    python311Packages.pexpect
  ];

  shellHook = ''
    echo Shell prepared!
  '';
}