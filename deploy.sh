rsync -av -e ssh --exclude-from='.gitignore' * <user>@<server>:<path> &&
ssh <user>@<server> << EOF
sudo chown apps:apps <path> -R
sudo -u apps -i
cd mani
make build
docker compose -f docker/docker-compose.yml up -d
EOF
