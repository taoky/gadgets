A `Dockerfile` for pwn environment using `socat`.

- Build: `docker build -t pwndocker . `
- Run: `docker run --read-only -it -p 12345:12345 pwndocker `
- Maintain (Attach): `docker exec -it xxxx /bin/bash `

---

`exe`: An x64 example pwnable executable. It executes `system("/bin/sh")` directly.

---

Remaining Problems:

- no timeout setting
- fork bomb