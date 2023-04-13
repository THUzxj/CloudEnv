# Cloud Environment

An all-in-one cloud environment for experiments.

## Host preparation

```bash
cp common.sh.sample common.sh
source common.sh
```

## Troubleshooting

### Docker internet problem in China

#### docker daemon

```bash
vi etc/systemd/system/docker.service.d/http-proxy.conf 
```

#### docker build

```bash
vi ~/.docker/config.json
```

# Known problems


