FROM python:3.9.6

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY main.py ./
COPY extensions/ ./extensions

COPY --from=1password/op:2 /usr/local/bin/op /usr/local/bin/op

ARG OP_VAULT

ENV DISCORD_TOKEN="op://${OP_VAULT}/DISCORD_TOKEN/password"
ENV DB_URI="op://${OP_VAULT}/DB_URI/password"
ENV GUILD_ID="op://${OP_VAULT}/GUILD_ID/password"
ENV CHANNEL_ID="op://${OP_VAULT}/CHANNEL_ID/password"

CMD op run -- python ./main.py