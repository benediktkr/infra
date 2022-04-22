# infra

the ansible repo for the [sudo.is](https://www.sudo.is) infrastructure.

![](https://static.sudo.is/img/lokun-logo.png)

## related projects

theres a lot of useful (and not so useful) scripts in this repo, that
are too short/simple to be their own "project", and they're sometimes
Jinja2-templated for convenience (though i usually prefer to template
configs and not code).

this repo also deploys/orchestrates a bunch of "projects":

 * [zflux](https://git.sudo.is/ben/zflux): a zeromq queue in front of
   influxdb to be resillient against network errors

 * [notflixbot](https://git.sudo.is/ben/notflixbot): a "custom" matrix
   bot written with nio (async python matrix library) and has
   webhooks.

 * [matrix-smtp-webhook](https://git.sudo.is/ben/matrix-smtp-webhook):
   a dead simple python daemon to read SMTP messages and forward to
   the notflix http webhookk, great for cron mail.

 * [archives](https://git.sudo.is/ben/archives): file listing with
   proxy auth

 * [shared-jenkins-pipelines](https://git.sudo.is/ben/shared-jenkins-pipelines)

and some docker images that needed customizing or as a way to package `.deb`:


 * [jenkins-docker](https://git.sudo.is/ben/jenkins-docker)
 * [mergerfs-docker](https://git.sudo.is/ben/mergerfs-docker)
 * [openldap-docker](https://git.sudo.is/ben/openldap-docker)
 * [poetry-docker](https://git.sudo.is/ben/poetry-docker)
 * [xmrig-docker](https://git.sudo.is/ben/xmrig-docker)
 * [hydrogen-docker](https://git.sudo.is/ben/hydrogen-docker)
 * [emacs-docker](https://git.sudo.is/ben/emacs-docker): building
   emacs from upstream git in docker on jenkins and packaging as
   `.deb` published at https://apt.sudo.is
 * [nginx-build](https://git.sudo.is/ben/nginx-build): building nginx from
   source with all modules (the useful ones anyway) and packaging as `.deb`


## mirrors

 * upstream repo: https://git.sudo.is/ben/infra
 * github mirror: https://github.com/benediktkr/infra
 * bitbucket mirror: https://bitbucket.org/benedikt/infra
