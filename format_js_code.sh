#!/bin/sh
yarn run prettier --write ${@:-src/**/*.js src/**/*.vue src/**/*.json}
