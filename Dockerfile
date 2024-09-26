FROM python:3.9.6

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY main.py ./

COPY --from=1password/op:2 /usr/local/bin/op /usr/local/bin/op

ARG OP_VAULT

ENV DISCORD_TOKEN="op://${OP_VAULT}/DISCORD_TOKEN/password"
ENV GUILD_ID="op://${OP_VAULT}/GUILD_ID/password"

CMD op run -- python ./main.py