## Web Server Installation (webclient)
- Go to webclient folder
```
cd webclient
```

- Install dependencies
```
go mod vendor
```

- Build & Run Project (Linux & Unix)
```
make go_run_web
```

- Build & Run Project (Windows or without **make** command)
```
go build -o bin/webclient main.go && go run main.go
```

- Or you want to run it as a Docker Container
```
bash start.sh
```