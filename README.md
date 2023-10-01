# our_discord_server
A place to work with my friend group's discord server



FROM python:3.9.6

ENV DISCORD_TOKEN="op://Personal Dev Vault/DISCORD_TOKEN/password"

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .

# uses the user's specified shell
RUN sudo -s \
curl -sS https://downloads.1password.com/linux/keys/1password.asc | \
gpg --dearmor --output /usr/share/keyrings/1password-archive-keyring.gpg


# This goes and gets the public key for the apt download and converts it to gpg
# -S, --show-error
#               When used with -s, --silent, it makes curl show an error
#               message if it fails.

#               This option is global and does not need to be specified
#               for each use of --next.

#               Providing -S, --show-error multiple times has no extra
#               effect.  Disable it again with --no-show-error.

#               Example:
#                curl --show-error --silent https://example.com

#               See also --no-progress-meter.


# The gpg is an acronym for “GnuPrivacy Guard”. It encrypts your files securely so that only the specified receiver can decrypt those files. GPG is based on the concept of each user having two encryption keys. Each individual can have a pair of public and private keys.

# https://www.digitalocean.com/community/tutorials/how-to-handle-apt-key-and-add-apt-repository-deprecation-using-gpg-to-add-external-repositories-on-ubuntu-22-04

RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/1password-archive-keyring.gpg] https://downloads.1password.com/linux/debian/$(dpkg --print-architecture) stable main" | \
sudo tee /etc/apt/sources.list.d/1password.list

# Add the debsig policy

RUN sudo mkdir -p /etc/debsig/policies/AC2D62742012EA22/
RUN curl -sS https://downloads.1password.com/linux/debian/debsig/1password.pol | \
sudo tee /etc/debsig/policies/AC2D62742012EA22/1password.pol
RUN sudo mkdir -p /usr/share/debsig/keyrings/AC2D62742012EA22
RUN curl -sS https://downloads.1password.com/linux/keys/1password.asc | \
sudo gpg --dearmor --output /usr/share/debsig/keyrings/AC2D62742012EA22/debsig.gpg

# update and install the 1password-cli

RUN sudo apt update && sudo apt install 1password-cli

RUN export "DISCORD_TOKEN=op://Personal Dev Vault/DISCORD_TOKEN/password"

CMD ["op run","--env-file=./.env" python ./main.py"]