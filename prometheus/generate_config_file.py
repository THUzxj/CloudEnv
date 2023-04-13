import config

template = '''
global:
  scrape_interval:     15s
  evaluation_interval: 15s

rule_files:
  # - "first.rules"
  # - "second.rules"

scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets: [{}]
'''

with open("prometheus.yml", "w") as f:
  f.write(template.format(",".join(["'" + a["ip"] + ":9100'" for a in config.NODES])))
