{ inputs, ... }:
{
  imports = [
    inputs.treefmt-nix.flakeModule
  ];
  perSystem =
    { ... }:
    {
      treefmt.programs.nixfmt.enable = true;
      treefmt.programs.black.enable = true;
      treefmt.programs.isort.enable = true;
      treefmt.programs.clang-format.enable = true;
      treefmt.programs.rumdl-format.enable = true;
      treefmt.programs.taplo.enable = true;
    };
}
