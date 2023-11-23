# infra

[![Build Status](https://jenkins.sudo.is/buildStatus/icon?job=infra%2Fb&style=flat-square)](https://jenkins.sudo.is/job/infra/)
[![Version](https://jenkins.sudo.is/buildStatus/icon?job=infra%2Fb&style=flat-square&status=${description}&subject=version&build=lastStable&color=blue)](https://git.sudo.is/ben/infra/packages)
[![BSD-3-Clause-No-Military-License](docs/img/shields/license-BSD-blue.svg)](LICENSE)
[![git](https://www.sudo.is/readmes/git.sudo.is-ben-infra.svg)](https://git.sudo.is/ben/infra)
[![github](https://www.sudo.is/readmes/github-benediktkr.svg)](https://github.com/benediktkr/infra)
[![Matrix](https://www.sudo.is/readmes/matrix-ben-sudo.is.svg)](https://matrix.to/#/@ben:sudo.is)


the ansible repo for the [sudo.is](https://www.sudo.is) infrastructure.

![logo](docs/img/logo.png)

## related projects

theres a lot of useful (and not so useful) scripts in this repo, that
are too short/simple to be their own "project", and they're sometimes
Jinja2-templated for convenience (though i usually prefer to template
configs and not code).

this repo also deploys/orchestrates a bunch of "projects":

 * [`zflux`](https://git.sudo.is/ben/zflux): a zeromq queue in front of
   influxdb to be resillient against network errors
 * [`notflixbot`](https://git.sudo.is/ben/notflixbot): a "custom" matrix
   bot written with nio (async python matrix library) and has
   webhooks.
 * [`matrix-smtp-webhook`](https://git.sudo.is/ben/matrix-smtp-webhook):
   a dead simple python daemon to read SMTP messages and forward to
   the notflix http webhook, great for cron mail.
 * [`archives`](https://git.sudo.is/ben/archives): file listing with
   proxy auth
 * [`shared-jenkins-pipelines`](https://git.sudo.is/ben/shared-jenkins-pipelines)

and various `.deb` builds and docker images that needed some customizing:


 * [`build-owntone`](https://git.sudo.is/ben/build-owntone): building
   [OwnTone](https://owntone.github.io/owntone-server/).
 * [`build-nginx`](https://git.sudo.is/ben/build-nginx): building
   nginx from source with all modules (the useful ones anyway) and
   packaging as `.deb`
 * [`build-jellyfin-web`](https://git.sudo.is/ben/build-jellyfin-web)
 * [`emacs-docker`](https://git.sudo.is/ben/emacs-docker): building
   emacs from upstream git in docker on jenkins and packaging a `.deb`
   published at https://apt.sudo.is
 * [`hydrogen-docker`](https://git.sudo.is/ben/hydrogen-docker)
 * [`jenkins-docker`](https://git.sudo.is/ben/jenkins-docker)
 * [`mergerfs-docker`](https://git.sudo.is/ben/mergerfs-docker)
 * [`openldap-docker`](https://git.sudo.is/ben/openldap-docker)
 * [`poetry-docker`](https://git.sudo.is/ben/poetry-docker)
 * [`socat-dns-docker`](https://git.sudo.is/ben/socat-dns-docker):
   forwarding the dns server of a docker bridged network.
 * [`synapse-admin-docker`](https://git.sudo.is/ben/synapse-admin-docker)
 * [`xmrig-docker`](https://git.sudo.is/ben/xmrig-docker)


## mirrors

 * upstream :gitea: : [`git.sudo.is/ben/infra`](https://git.sudo.is/ben/infra)
 * github :github: mirror: [`benediktkr/infra`](https://github.com/benediktkr/infra)
 * bitbucket mirror (private): [`benedikt/infra`](https://bitbucket.org/benedikt/infra)
