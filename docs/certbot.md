# certbot

## make a new ssl cert

```shell
certbot certonly -d $NAME
```

at this point, the cert exists in the `certbot`-managed dir
`/etc/letsencrypt/live`:

```shell
$ ls -d /etc/letsencrypt/live/${NAME}
/etc/letsencrypt/live/${NAME}
```

## delete/revoke a cert

if you need to

```shell
sudo certbot delete --cert-name $NAME
```


```
--dns-cloudflare-propagation-seconds
```
