# Perdido

Hi, I'm Perdido. I'm a seedbox, streaming server, and more! I'm really talented.

Here is a list of services I host:

- **For torrenting** I run [rTorrent](https://github.com/rakshasa/rtorrent). That's just a backend, but you can connect to it using [Transdrone](https://play.google.com/store/apps/details?id=org.transdroid.lite&hl=en&gl=US) and similar apps via SCGI to manage it. Just use the endpoint `/RPC2`.
- **My built-in torrent frontend** is [ruTorrent](https://github.com/Novik/ruTorrent). Sure, it's a bit vintage and rough around the edges, but it's pretty stable and functional.
- **For auto-sorting downloads** I use my [sweeper](https://github.com/GregRos/sweeper), which is a custom python script. That script uses [filebot](https://www.filebot.net/) behind the scenes in most cases.
- **For video streaming,** I run [Jellyfin](https://github.com/jellyfin/jellyfin). Jellyfin is super special awesome and is much better than other programs like [Emby](https://emby.media/) and way better than [Plex](https://www.plex.tv/). I hate that thing.
- **For file transfer,** I support SCP, SFTP, and FTP (TLS only). If none of that works for you, you can use my trusty [filebrowser](https://filebrowser.org/) instead.

To tie this all together I use [nginx](https://nginx.org/), acting as a reverse proxy. Neat, right? I'd show you, but I only show my internal services to my trusted friends who know the secret handshake.

Sadly, ever since I moved in to my neighborhood and started torrenting, I've been getting all kinds of nasty callers. Just look at this page from my journal:

![a log containing multiple failed login attempts](docs/unpleasant-callers.png)

I don't know any of these kiddies! They all just ring my SSH, say `root`, and then run away! A few of them even tried to convince me to use SHA1. How horrid.

More importantly, though - the racket! I could barely sleep. At least, not until I installed [fail2ban](https://www.fail2ban.org/wiki/index.php/Main_Page). And it worked like a charm, just like the testimonials said it would. It really helps keeping the more rambunctious ones at bay. Let's see who's on my naughty list right now:

```
[{'sshd': ['61.177.173.37', '61.177.172.108', '61.177.173.50', '61.177.173.35', '218.92.0.204']}, {'vsftpd': []}]
```

Oh, look! That's `218.92.0.204` from earlier! I hope they've learned their lesson.

I couldn't stop just with that, though. Sure, `fail2ban` protects by FTP and SSH, but I wanted to be sure my nginx is safe too. So I compiled [ModSecurity](https://github.com/SpiderLabs/ModSecurity) and even got some [rules](https://owasp.org/www-project-modsecurity-core-rule-set/) for it. I hooked that all up and got it purring like a kitten. No nasty HTTP traffic is going to be bothering my nginx.

Actually, though, my nginx is well-protected as it is. Call me old-fashioned, but I just use basic HTTP authentication. Sure, it has its limitations, but my cousin told me that it has a "small attack surface" or something, and I usually just do whatever he tells me.

After all that was done I went out and got an official [LetsEncrypt](https://letsencrypt.org/) certificate. From now on, if someone offers me some unencrypted traffic - I just say no!

Well, I say "Please use the other door."

# Explanation

1. Perdido is not a shrinkwrapped product. It's moved a few environments but by its nature as a bundle of scripts it's not set-it-and-forget-it. It comes with no documentation and you can submit no bug reports.
2. Perdido is not containerized. I don't know what would happen if you ran it in a container, but it probably won't work. It expects to run in a VM or physical machine.

This repo contains the code needed to set Perdido services up a new machine. The setup scripts are in `setup.d`, in the order they should run. Each script does something specific, but it's also idempotent. If the script has already executed running it again won't change anything.

All the scripts have `set -ex`, which means you'll see every line being executed and the script will stop on error.

Some scripts symlink configuration files, so that pulling will automatically update the config file. In some cases you can't do that, and you have to create a real file instead. In that case the config file is copied. You should run the `setup` tool to rerun things just in case.

You can run the scripts manually, but I wrote a handy Python runner for executing them. It's just `./setup`. It has a few nifty features. For example, the script's output will be decorated with its name and number so you know what's running right now.

Plus, you can run specific scripts or a subset. Here is an example:

```
./setup run 2,50,nginx,51- rtorrent
```

This will run the scripts:

1. `02.env.bash`
2. `23.nginx.bash`
3. `31.rtorrent.bash`
4. `50.ftp.bash`
5. All scripts with `id > 51` (that's the `51-` parameter)

# Installation

Requires Debian 11 and Python 3.9. All other requirements are installed by the script.

```bash
git clone git@github.com:GregRos/perdido.git /opt/perdido
cd /opt/perdido
./setup install
```

Perdido includes a handy CLI for running some of the stages separately. For example:

```
./install run 3,50,docker,51- rtorrent
```

The above would only run the scripts:

- `03.docker.bash`
- `31.rtorrent.bash`
- `50.ftp.bash`
- Scripts with ID `51+`.

It will still run them in ascending order, not in the specified order.

**Perdido is not containerized and expects to run on a VM or physical machine.**

# Configuration

Some services still need to be configured manually after the installation:

1. Jellyfin
2. Filebrowser
3. Maybe other stuff.

Perdido is not a shrinkwrapped application, it's a cobbled-together bundle of code. Maybe one day it'll all be k8s pods or something.

> asdadasdsa
> dfsdfsdfdsf
