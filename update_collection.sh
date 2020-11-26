#!/bin/bash

read -p "Samlingen blir slettet og gjenopprettet. Sikker på at du vil fortsette? " -n 1 -r
echo -e    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1 # handle exits from shell or function but don't exit interactive shell
fi

start=$SECONDS

cd conversion

echo -e "\033[1;96mDeleting old collection\033[0m"
task_start=$SECONDS
#poetry run python -m scripts.delete_alma_collection
echo -e "\033[1;32m ✅ Collection deleted in $(( SECONDS - task_start )) secs\033[0m"

echo -e "\033[1;96mUploading new collection\033[0m"
task_start=$SECONDS
#poetry run python -m scripts.push_to_alma
echo -e "\033[1;32m ✅ Collection uploaded in $(( SECONDS - task_start )) secs\033[0m"

echo -e "\033[1;32mWaiting 240 seconds for collection to be ingested in Alma\033[0m"
#sleep 240

echo -e "\033[1;96mFetching new identifiers\033[0m"
task_start=$SECONDS
poetry run python -m scripts.fetch_ids
echo -e "\033[1;32m ✅ Identifiers fetched in $(( SECONDS - task_start )) secs\033[0m"

echo -e "\033[1;96mGenerating map data\033[0m"
task_start=$SECONDS
poetry run python -m scripts.make_map_data
echo -e "\033[1;32m ✅ Map data generated in $(( SECONDS - task_start )) secs\033[0m"

echo -e "\033[1;96mGenerating map tiles\033[0m"
task_start=$SECONDS
poetry run python -m scripts.make_tiles
echo -e "\033[1;32m ✅ Map tiles generated in $(( SECONDS - task_start )) secs\033[0m"

echo -e "\033[1;96mGenerating thumbnails\033[0m"
task_start=$SECONDS
poetry run python -m scripts.make_thumbs
echo -e "\033[1;32m ✅ Thumbnails generated in $(( SECONDS - task_start )) secs\033[0m"

cd ..

cd popcorn-viewer
npm run build
cd ..

echo -e "\033[1;32mCompleted in $duration secs\033[0m"
