# IMAGE TAG API

An api to store images and tag them

## App
To run the app: 
1. Create a `.config.yaml` file with the needed values (see `config.example.yaml`)
2. Run `docker compose up`


## Database

### Apply changes to database

The project uses `alembic` as the migrations engine. Some custom features have been added so that migration steps (a.k.a. revisions) work with `.sql` files. 

Revision ids **MUST** be numbered (e.g `01_first_revision.py`). An example of a revision generation: `python -m alembic revision -m "first revision" --rev-id=01`


To generate a new migration step:
1. `python -m alembic revision -m "<step_name>" --rev-id=<step_id>`
2. Create and fill the corresponding `.sql` files at `database/schemas/`: 
   - Upgrades: `.up.sql`
   - Downgrades: `.down.sql`
3. When you run the application, it will automatically apply the pending-to-migrate revisions, based on your current revision number in the table `alembic_version` of the database.
