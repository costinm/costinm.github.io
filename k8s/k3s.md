
Notes on using K3S for dev, tests and small installs.

# Install as root

- Shell script creates a systemd unit, start by default
- systemctl stop k3s, disable k3s

- kubeconfig generated as:  /etc/rancher/k3s/k3s.yaml
- /etc/systemd/system/k3s.service
- /etc/systemd/system/k3s.service.env

```shell script

cat /etc/systemd/system/k3s.service.env 
K3S_KUBECONFIG_MODE=666


journalctl -u k3s

```

Files under: /var/lib/rancher

Custom flannel config, if kernel doesn't support vxlan:

```json
{
        "Network": "10.42.0.0/16",
        "SubnetLen": 20,
        "SubnetMin": "10.42.0.0",
        "SubnetMax": "10.42.64.0",
        "Backend": {
                "Type": "host-gw",
                "Port": 7890
        }
}
```

Start agent with:

```shell
./k3s agent --server https://x.x.x.x:6443 --token $TOKEN --flannel-conf flannel.conf  
```

Also:
- if you have an external IP: --node-external-ip=10.1.10.1 
- multiple interfaces: --flannel-iface=br-lan

By default agent uses built-in 'runc'
