FROM python:3.9.6

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY main.py ./

COPY --from=1password/op:2 /usr/local/bin/op /usr/local/bin/op

ENV DISCORD_TOKEN="op://Personal Dev Vault/DISCORD_TOKEN/password"
ENV APP_ID="op://Personal Dev Vault/APP_ID/password"
ENV PUBLIC_KEY="op://Personal Dev Vault/PUBLIC_KEY/password"
ENV GUILD_ID="op://Personal Dev Vault/GUILD_ID/password"
ENV CHANNEL_ID="op://Personal Dev Vault/CHANNEL_ID/password"
ENV INTENTS="op://Personal Dev Vault/INTENTS/password"
ENV CHANNEL_CATEGORY="op://Personal Dev Vault/CHANNEL_CATEGORY/password"

CMD op run -- python ./main.py