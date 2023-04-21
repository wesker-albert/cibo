#!/bin/bash

MATCH="make: Nothing to be done for 'init'."
UP_TO_DATE="\nAll dependencies and lockfiles are already up-to-date!\nYou can use this regained time to grab a fresh cup of coffee...\n"

make init | sed "s/${MATCH}/${UP_TO_DATE}/"
