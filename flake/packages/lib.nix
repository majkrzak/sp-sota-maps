{
  lib,
  inputs,
  version,
  ...
}:
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
      carto-data = pkgs.stdenv.mkDerivation {
        name = "openstreetmap-carto-data";
        src = inputs.openstreetmap-carto;
        nativeBuildInputs =
          with pkgs;
          [
            osm2pgsql
          ]
          ++ [ postgres ];
        configurePhase = ''
          export PGDATA="$(pwd)/pgdata";
          export PGHOST="$(pwd)";
          export PGDATABASE="gis";
          export PGUSER="gis";
        '';
        buildPhase = ''
          initdb \
            --encoding=UTF8 \
            --username=gis
          pg_ctl -o "-c listen_addresses= -c unix_socket_directories=$PGHOST" start
          createdb
          psql -c 'CREATE EXTENSION postgis; CREATE EXTENSION hstore;'
          osm2pgsql \
            --output flex \
            --style openstreetmap-carto-flex.lua \
            --input-reader=pbf "${inputs.poland-osm-pbf}"
          psql -f indexes.sql
          psql -f functions.sql
          psql -f common-values.sql
          psql -c 'VACUUM FULL FREEZE ANALYZE'
          pg_ctl stop
        '';
        installPhase = ''
          mv pgdata "$out"
        '';
      };
      carto-service = pkgs.writeText "carto.service" ''
        [Unit]
        [Service]
        RuntimeDirectory=%n
        PrivateMounts=true
        PrivateTmp=disconnected
        ProtectSystem=strict
        BindReadOnlyPaths=/nix/store
        AmbientCapabilities=CAP_SYS_ADMIN
        ExecStart=${pkgs.writeShellScript "carto-start" ''
          set -e
          cp -R "${carto-data}" /tmp/pgdata
          chmod -R u=rwX,og= /tmp/pgdata
          ${lib.getExe' postgres "postgres"} \
           -c listen_addresses= \
           -c unix_socket_directories="''${RUNTIME_DIRECTORY:?}"  \
           -D "/tmp/pgdata"
        ''}
      '';
      carto-service-name = lib.baseNameOf carto-service;
    in
    {
      packages.sota-unwrapped = python.pkgs.buildPythonPackage (
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
      packages.sota = pkgs.buildEnv {
        name = "sota-${version}";
        nativeBuildInputs = with pkgs; [ makeWrapper ];
        paths = with self'.packages; [
          sota-unwrapped
        ];
        pathsToLink = [
          "/"
          "/bin"
        ];
        postBuild = ''
          for i in $out/bin/*; do
            wrapProgram "$i" \
              --run 'systemctl --user link ${carto-service}' \
              --run 'systemctl --user start ${carto-service-name}' \
              --run 'export PGHOST="$XDG_RUNTIME_DIR/${carto-service-name}"' \
              --set CARTO_DIR ${carto-style}
          done
        '';
        meta = self'.packages.sota-unwrapped;
      };
    };
}
