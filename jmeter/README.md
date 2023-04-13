
open GUI:

```bash
./bin/jmeter
```

test:

```bash
~/apache-jmeter-5.5/bin/jmeter -n -t testplan/sock.jmx -l testresult/sock_round50_result.txt -e -o testresult/round50
~/apache-jmeter-5.5/bin/jmeter -n -t testplan/infinite.jmx -l testresult/infinite_result.txt -e -o testresult/infinite
```

# Timer shaping

[](https://www.blazemeter.com/blog/jmeters-shaping-timer-plugin)

[](https://stackoverflow.com/questions/68448606/how-to-increase-dynamically-load-on-jmeter)
