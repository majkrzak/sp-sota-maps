{ inputs, ... }:
{
  perSystem =
    { pkgs, ... }:
    {
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
          initdb --encoding=UTF8
          pg_ctl -o "-c listen_addresses= -c unix_socket_directories=$PGHOST" start
          createdb
          psql -c 'CREATE EXTENSION postgis; CREATE EXTENSION hstore;'
        '';
        buildPhase = ''
          osm2pgsql \
            --output flex \
            --style openstreetmap-carto-flex.lua \
            --input-reader=pbf "${inputs.poland-osm-pbf}"
          psql -f indexes.sql
          psql -f functions.sql
          psql -f common-values.sql
        '';
        installPhase = ''
          pg_dump -Fc > $out
        '';
        fixupPhase = ''
          pg_ctl stop
        '';
      };
    };
}
