{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.11";
    flake-parts.url = "github:hercules-ci/flake-parts";
    import-tree.url = "github:vic/import-tree";
    treefmt-nix.url = "github:numtide/treefmt-nix";
    treefmt-nix.inputs.nixpkgs.follows = "nixpkgs";
    pyproject-nix.url = "github:pyproject-nix/pyproject.nix";
    pyproject-nix.inputs.nixpkgs.follows = "nixpkgs";
    openstreetmap-carto.url = "github:openstreetmap-carto/openstreetmap-carto";
    openstreetmap-carto.flake = false;
    poland-osm-pbf.url = "https://download.geofabrik.de/europe/poland-260101.osm.pbf";
    poland-osm-pbf.flake = false;
  };
  outputs = inputs: inputs.flake-parts.lib.mkFlake { inherit inputs; } (inputs.import-tree ./flake);
}
