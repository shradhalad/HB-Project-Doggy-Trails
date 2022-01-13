#!/usr/bin/env bash
dropdb project
createdb project
python3 -c 'import model; db = model.connect_to_db(model.get_app()); db.create_all()'
python3 -c 'import model; model.add_fake_data()'
