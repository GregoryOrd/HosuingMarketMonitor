#!/usr/bin/python

from prospects import Prospect
from email_sender import sendEmail
from db_access import DbAccess
import remax
import os
from remax_config import ConfigData

def diff_prospects_list(old_prospects, new_prospects):
    to_delete = []
    to_add = []
    price_changes = []

    # Since a price change entry is in both lists,
    # we only need to check for it in one of the loops
    for old in old_prospects:
        try:
            index = new_prospects.index(old)
            if old.price != new_prospects[index].price:
                price_change.append((old, new))
        except ValueError:
            to_delete.append(old)

    for new in new_prospects:
        if new not in old_prospects:
            to_add.append(new)

    return to_delete, to_add, price_changes

def update_prospects(config_data):
    if config_data is None:
        print("Configuration Data Not Set.")
        return

    db_access = DbAccess()
    db_access.start()

    old_prospects = db_access.query()

    new_prospects = remax.query_remax(config_data)

    to_delete, to_add, price_changes = diff_prospects_list(old_prospects, new_prospects)

    for p in to_add:
        db_access.insert_prospect(p)

    for p in to_delete:
        db_access.delete_prospect(p)

    if len(to_add) > 0 or len(to_delete) > 0 or len(price_changes) > 0:
        print(f"{len(price_changes)} price changes, {len(to_add)} additions, {len(to_delete)} deletions")
        to_add = sorted(to_add, key=lambda p: p.price)
        to_delete = sorted(to_delete, key=lambda p: p.price)
        sendEmail(to_delete, to_add, price_changes, config_data.min_price, config_data.max_price)
    else:
        print("No changes.")

    db_access.close()

update_prospects(ConfigData.fromConfigFile(os.path.expanduser("~/retriever_config.yaml")))