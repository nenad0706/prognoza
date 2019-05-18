# prognoza
Unix terminal weather forecast (bash, python, bs4)

Data from https://www.accuweather.com/sr/rs/belgrade/298198/hourly-weather-forecast/298198

![prognoza](https://user-images.githubusercontent.com/31278778/57962938-d10fd900-791d-11e9-996a-084f6495edd4.png)

## Configuration

1. Create (if not exists) directory */home/USER/bin*:
``` 
mkdir /home/USER/bin && cd "$"
```
2. Copy *prognoza* into that dir:
```
cp PATH_TO_FILE/prognoza .
```
3. Add execute privileges:
```
chmod 755 prognoza
```
4. Export path so it is loaded every time terminal is opened:
```
echo "export PATH=\"$HOME/bin:$PATH\"" >> ~/.bashrc
```

**Now you can run it just by typing "prognoza"**
