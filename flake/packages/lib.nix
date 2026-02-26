{ inputs, ... }:
let
  project = inputs.pyproject-nix.lib.project.loadPyproject {
    projectRoot = ../../lib;
  };
in
{
  perSystem =
    { pkgs, ... }:
    let
      python = pkgs.python3;
    in
    {
      packages.test = pkgs.mapnik;
      packages.lib = python.pkgs.buildPythonPackage (
        (project.renderers.buildPythonPackage {
          inherit python;
        })
        // {
          version = if (inputs.self ? rev) then inputs.self.rev else inputs.self.dirtyRev;
          buildInputs = with pkgs; [
            mapnik
            mapnik.buildInputs
          ];
          nativeBuildInputs = with pkgs; [ pkg-config ];
        }
      );
    };
}
