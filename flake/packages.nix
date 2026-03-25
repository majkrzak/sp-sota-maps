{
  lib,
  inputs,
  version,
  ...
}:
let
  project = inputs.pyproject-nix.lib.project.loadPyproject {
    projectRoot = ../lib;
  };
in
{
  perSystem =
    { pkgs, self', ... }:
    let
      python = pkgs.python3;
      postgres = with pkgs; postgresql.withPackages (p: with p; [ postgis ]);
      carto-style = pkgs.stdenv.mkDerivation {
        name = "openstreetmap-carto-style";
        src = inputs.openstreetmap-carto;
        nativeBuildInputs = with pkgs; [
          carto
        ];
        buildPhase = ''
          carto project.mml > carto.xml
        '';
        installPhase = ''
          mkdir $out
          cp -r patterns $out
          cp -r symbols $out
          cp -r "${pkgs.noto-fonts}/share/fonts/noto" "''${out}/fonts"
          cp carto.xml $out
        '';
      };
      carto-init = pkgs.writeShellScript "carto-init" ''
        set -e
        ${lib.getExe' pkgs.osm2pgsql "osm2pgsql"} -O flex -S "${inputs.openstreetmap-carto}/openstreetmap-carto-flex.lua" --input-reader=xml -
        ${lib.getExe' postgres "psql"} -f "${inputs.openstreetmap-carto}/indexes.sql"
        ${lib.getExe' postgres "psql"} -f "${inputs.openstreetmap-carto}/functions.sql"
        ${lib.getExe' postgres "psql"} -f "${inputs.openstreetmap-carto}/common-values.sql"
        ${
          lib.getExe (
            pkgs.python3.withPackages (
              p: with p; [
                pyyaml
                requests
                psycopg2
              ]
            )
          )
        } "${inputs.openstreetmap-carto}/scripts/get-external-data.py" --config "${inputs.openstreetmap-carto}/external-data.yml" --cache --data "''${SOTA_CACHE:-./cache/}"
      '';
      carto-service = pkgs.writeText "carto.service" ''
        [Unit]
        [Service]
        Type=notify
        RuntimeDirectory=%n
        PrivateMounts=true
        PrivateTmp=true
        ProtectSystem=strict
        BindReadOnlyPaths=/nix/store
        AmbientCapabilities=CAP_SYS_ADMIN
        Environment=PGDATA="%T/pgdata"
        Environment=PGHOST="%t/%n"
        Environment=PGDATABASE="gis"
        Environment=PGUSER="gis"
        ExecStartPre=mkdir "''${PGDATA}"
        ExecStartPre=${lib.getExe' postgres "initdb"} --encoding=UTF8 --username=gis
        ExecStart=${lib.getExe' postgres "postgres"} -c listen_addresses= -c unix_socket_directories="''${PGHOST}" -D "''${PGDATA}"
        ExecStartPost=${lib.getExe' postgres "createdb"} 
        ExecStartPost=${lib.getExe' postgres "psql"} -c 'CREATE EXTENSION postgis; CREATE EXTENSION hstore;'
      '';
      carto-service-name = lib.baseNameOf carto-service;
    in
    {
      packages.sota = python.pkgs.buildPythonPackage (
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
        }
      );
      packages.python = pkgs.python3.withPackages (_: [ self'.packages.sota ]);
      packages.default = pkgs.buildEnv {
        name = "sp-sota-maps-${version}";
        nativeBuildInputs = with pkgs; [ makeWrapper ];
        paths = with self'.packages; [
          sota
        ];
        pathsToLink = [
          "/"
          "/bin"
        ];
        postBuild = ''
          wrapProgram "$out/bin/sota" \
            --run 'systemctl --user --runtime link ${carto-service}' \
            --run 'systemctl --user start ${carto-service-name}' \
            --run 'export PGHOST="$XDG_RUNTIME_DIR/${carto-service-name}"' \
            --set PGDATABASE gis \
            --set PGUSER gis \
            --set CARTO_DIR ${carto-style} \
            --set CARTO_INIT ${carto-init}
        '';
      };
    };
}
