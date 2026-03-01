{ lib, inputs, ... }:
{
  perSystem =
    { pkgs, system, ... }:
    {
      packages.carto = derivation {
        inherit system;
        name = "openstreetmap-carto";
        src = inputs.openstreetmap-carto;
        builder = lib.getExe (
          pkgs.writeShellApplication {
            name = "builder";
            runtimeInputs = with pkgs; [
              coreutils
              osm2pgsql
              carto
              (postgresql.withPackages (p: with p; [ postgis ]))
            ];
            text = ''
              export PGDATA="''${TMP:?}/pgdata"
              export PGHOST="''${TMP:?}"
              export PGDATABASE="gis"

              initdb --encoding=UTF8
              pg_ctl -o "-c listen_addresses= -c unix_socket_directories=$PGHOST" start

              createdb
              psql -c 'CREATE EXTENSION postgis; CREATE EXTENSION hstore;'

              osm2pgsql \
                --output flex \
                --style "''${src:?}/openstreetmap-carto-flex.lua" \
                --input-reader=pbf "${inputs.poland-osm-pbf}"

              psql -c 'ALTER SYSTEM SET jit=off;' -c 'SELECT pg_reload_conf();'
              psql -f "''${src:?}/indexes.sql"
              psql -f "''${src:?}/functions.sql"
              psql -f "''${src:?}/common-values.sql"

              pg_ctl stop

              mkdir "''${out:?}"
              cp -r "''${src:?}/patterns" "''${out}"
              cp -r "''${src:?}/symbols" "''${out}"
              cp -r "$TMP/pgdata" "''${out}"
              cp -r "${pkgs.noto-fonts}/share/fonts/noto" "''${out}/fonts"
              carto "''${src:?}/project.mml" > "''${out:?}/carto.xml"
            '';
          }
        );
      };
    };
}
