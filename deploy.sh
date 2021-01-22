#!/bin/bash
gcloud functions deploy eq-translations-check \
    --entry-point check_translations --runtime python38 --trigger-http \
    --region=europe-west2
