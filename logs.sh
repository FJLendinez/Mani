ssh <user>@<server> << EOF
docker logs --tail 1000 -f mani_app
EOF
