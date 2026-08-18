# sse
This project is to demonstrate SSE(server sent event). 

# local env setup

Run docker compose to execute
```bash
docker compose up -d
```

Check logs
```bash
docker compose logs -f
```

Run curl command disabling caching for result using -N flag -
```
curl -N http://localhost/api/server-stats
```

Try from browser
![alt text](docs/images/image.png)
