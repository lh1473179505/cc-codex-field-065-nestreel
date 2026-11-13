# nestreel

把客服邮箱的 mbox 和工单里的压缩包抽到同一份湖表。跨来源去重，损坏或路径越界的条目进隔离区。

```
python -m nestreel extract --mbox fixtures/inbox.mbox --tickets fixtures/tickets --out <out> --checkpoint <ckpt>
python -m nestreel verify --out <out> --expect fixtures/expected/lake.json
```
