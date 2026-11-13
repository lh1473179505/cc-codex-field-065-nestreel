# 来源与落盘

`extract` 同时读 `--mbox` 和 `--tickets` 目录。tickets 里会有 zip（可能再套一层 zip）、html 和 csv。不要访问网络。

## 邮件

mbox 里有多封信，编码不一致：

- 有的正文是 UTF-8，有的是 GB2312（`Content-Type: text/plain; charset=gb2312`），有的是 quoted-printable。
- 附件可能是 csv 或 html，文件名可能是 RFC 2047 编码。
- 同一张发票会同时出现在一封邮件附件和 tickets 的压缩包里，湖里只能留一行，`sources` 数组记下两个来源（`mbox:<message-id>:<filename>` 和 `zip:<zip路径>:<内部路径>`）。

去重键：优先用附件或文件正文里的 `Invoice-No:` / `invoice_no` 字段；没有发票号时，对规范化正文（去掉连续空白、统一换行）做 sha256，作为 `content_id`。最终 `record_id` 为发票号，若无发票号则为 `sha256:` 加该哈希。

## 压缩包与隔离

tickets 下的 zip 可能嵌套。需要递归解开，但遇到下面情况时不要写入湖表，改写到 `--out/quarantine.jsonl`：

- 内部路径包含 `..` 或绝对路径（zip-slip），即使解出来也不会落盘。
- 损坏的 zip 成员（夹具里 `broken.zip` 有一个坏条目，其它完好条目仍要处理）。
- 无法解码且不是明确声明为二进制发票扫描件的条目（`.png/.jpg/.pdf` 可作为二进制记录落盘，用文件 sha256 当 content_id）。

quarantine 行：`{"source","path","reason"}`，reason 为 `zip_slip`、`corrupt` 或 `undecodable`。

## 湖表

`--out/lake.jsonl` 一行一条：`record_id`、`kind`（`invoice`/`message`/`table`/`binary`/`html`）、`invoice_no`（可空）、`title`、`text`（能解码的文本，二进制可空）、`content_sha256`、`sources`（排序后的数组）。邮件正文本身若不含发票、只是会话，按 message 落一行，不要和附件发票合并。
