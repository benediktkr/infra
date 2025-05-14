# `infra`

[![Build Status](https://jenkins.sudo.is/buildStatus/icon?job=infra%2Fb&style=flat-square)](https://jenkins.sudo.is/job/infra/)
[![Version](https://jenkins.sudo.is/buildStatus/icon?job=infra%2Fb&style=flat-square&status=${description}&subject=version&build=lastStable&color=blue)](https://git.sudo.is/ben/infra/packages)
[![BSD-2-Claus](https://www.sudo.is/readmes/license-BSD-blue.svg)](LICENSE)
[![git](https://www.sudo.is/readmes/git.sudo.is-ben-infra.svg)](https://git.sudo.is/ben/infra)
[![codeberg](https://www.sudo.is/readmes/codeberg.svg)](https://codeberg.org/benk/infra)
[![github](https://www.sudo.is/readmes/github-benediktkr.svg)](https://github.com/benediktkr/infra)
[![Matrix](https://www.sudo.is/readmes/matrix-ben-sudo.is.svg)](https://matrix.to/#/@ben:sudo.is)

![logo](docs/img/logo.png)

## Overview

This is the ansible repo for the [`sudo.is` infrastructure](https://www.sudo.is/docs/infra/).

There are a lot of useful (and not so useful) scripts in this repo that
are too short/simple to be their own "project", and they're sometimes
Jinja2-templated for convenience (though I usually prefer to template
configs and not code).

## Related projects

This repo also deploys/orchestrates a bunch of "projects":

- [`zflux`](https://git.sudo.is/ben/zflux): A ZeroMQ queue in front of
  InfluxDB to be resillient against network errors.
- [`notflixbot`](https://git.sudo.is/ben/notflixbot): A "custom" Matrix
  bot written with nio (async python matrix library) and has
  webhooks.
- [`matrix-smtp-webhook`](https://git.sudo.is/ben/matrix-smtp-webhook):
  A dead simple python daemon to read SMTP messages and forward to
  the Notflix HTTP webhook, great for cron mail.
- [`archives`](https://git.sudo.is/ben/archives): file listing with
  proxy authl
- [`shared-jenkins-pipelines`](https://git.sudo.is/ben/shared-jenkins-pipelines)

And various `.deb` builds and docker images that needed some customizing:

- [`build-owntone`](https://git.sudo.is/ben/build-owntone): Building [OwnTone](https://owntone.github.io/owntone-server/).
- [`build-jellyfin-web`](https://git.sudo.is/ben/build-jellyfin-web)
- [`emacs-docker`](https://git.sudo.is/ben/emacs-docker) (not maintained):
  Built Emacs from upstream Git in Docker on Jenkins and packages a `.deb`
  published at [`apt.sudo.is`](https://apt.sudo.is).
- [`jenkins-docker`](https://git.sudo.is/ben/jenkins-docker)
- [`openldap-docker`](https://git.sudo.is/ben/openldap-docker)
- [`socat-dns-docker`](https://git.sudo.is/ben/socat-dns-docker):
  Forwarding the DNS server of a Docker bridged network.
- [`synapse-admin-docker`](https://git.sudo.is/ben/synapse-admin-docker)
- [`xmrig-docker`](https://git.sudo.is/ben/xmrig-docker)

## Git mirrors

- :gitea: : [`git.sudo.is/ben/infra`](https://git.sudo.is/ben/infra)
- GitHub :github: mirror: [`benediktkr/infra`](https://github.com/benediktkr/infra)
- Codeberg :codeberg: [`benk/infra`](https://codeberg.org/benk/Infra)
- Bitbucket mirror (private): [`benedikt/infra`](https://bitbucket.org/benedikt/infra)
