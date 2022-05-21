# mainframe

## new ssl cert

set the `$NAME` var for consistency

```shell
NAME=foo.bar.com
```

request a new cert with `certbot` (configured to use dns)

```shell
sudo certbot certonly --dns-cloudflare --dns-cloudflare-credentials /home/ben/.certbot_cloudflare.ini  --preferred-challenges dns -d ${NAME}
```

at this point, the cert exists in the `certbot`-managed dir
`/etc/letsencrypt/live`, but not in the ansible managed
`/usr/local/etc/certs/`:

```shell
$ ls -d /etc/letsencrypt/live/${NAME}
/etc/letsencrypt/live/twatter.sudo.is

$ ls -d /usr/local/etc/certs/${NAME}
ls: cannot access '/usr/local/etc/certs/twatter.sudo.is': No such file or directory
```

add it to the `letsencrypt_sni` in `group_vars/letsencrypt.yml` and
roll it out:

```shell
ansible-playbook site2.yml --diff --limit letsencrypt --tags letsencrypt-scripts
```

you should see a change to `/usr/local/bin/letsencrypt.sh`, and then
run that scripts

```shell
sudo letsencrypt.sh
```

now the certs will be in `/usr/local/etc/certs`:

```shell
$ ls -d /usr/local/etc/certs/${NAME}
/usr/local/etc/certs/twatter.sudo.is
```

then the pattern is currently to add a task in the role that uses this
specific script to copy it to `/usr/local/etc/certs` on those hosts.

## remove/delete a cert

if you need to

```shell
sudo certbot delete --cert-name $NAME
```
