FROM python:3.9.6

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY main.py ./

COPY --from=1password/op:2 /usr/local/bin/op /usr/local/bin/op

ARG OP_VAULT

ENV DISCORD_TOKEN="op://${OP_VAULT}/DISCORD_TOKEN/password"
ENV APP_ID="op://${OP_VAULT}/APP_ID/password"
ENV PUBLIC_KEY="op://${OP_VAULT}/PUBLIC_KEY/password"
ENV GUILD_ID="op://${OP_VAULT}/GUILD_ID/password"
ENV CHANNEL_ID="op://${OP_VAULT}/CHANNEL_ID/password"
ENV INTENTS="op://${OP_VAULT}/INTENTS/password"
ENV CHANNEL_CATEGORY="op://${OP_VAULT}/CHANNEL_CATEGORY/password"

CMD op run -- python ./main.py