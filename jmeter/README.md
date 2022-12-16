
open GUI:

```bash
./bin/jmeter
```

test:

```bash
~/apache-jmeter-5.5/bin/jmeter -n -t testplan/sock.jmx -l testresult/sock_round50_result.txt -e -o testresult/round50
```