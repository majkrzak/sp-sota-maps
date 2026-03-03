{ inputs, lib, ... }:
{
  perSystem =
    { pkgs, self', ... }:
    {
      packages.carto-start = pkgs.writeShellApplication {
        name = "carto-start";
        runtimeInputs = with pkgs; [
          (postgresql.withPackages (p: with p; [ postgis ]))
        ];
        text = ''
          cp -r "${self'.packages.carto-data}" "''${PGDATA:?}"
          chmod -R u=rwX,og-rwx "''${PGDATA:?}"
          pg_ctl -o "-c listen_addresses= -c unix_socket_directories=''${PGHOST:?}" start
        '';
      };
      packages.carto-style = pkgs.stdenv.mkDerivation {
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
      packages.carto-data = pkgs.stdenv.mkDerivation {
        name = "openstreetmap-carto-data";
        src = inputs.openstreetmap-carto;
        nativeBuildInputs = with pkgs; [
          osm2pgsql
          (postgresql.withPackages (p: with p; [ postgis ]))
        ];
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
    };
}
