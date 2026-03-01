{ inputs, version, ... }:
let
  project = inputs.pyproject-nix.lib.project.loadPyproject {
    projectRoot = ../../lib;
  };
in
{
  perSystem =
    { pkgs, self', ... }:
    let
      python = pkgs.python3;
    in
    {
      packages.lib = python.pkgs.buildPythonPackage (
        (project.renderers.buildPythonPackage {
          inherit python;
        })
        // {
          inherit version;
          buildInputs = with pkgs; [
            mapnik
            mapnik.buildInputs
          ];
          nativeBuildInputs = with pkgs; [ pkg-config ];
          carto_dir = "${self'.packages.carto}";
        }
      );
    };
}
