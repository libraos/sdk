"""The round trip against a running service.py: what you send, what leaves, what comes back. All the data is made up.

    python demo.py [--url http://127.0.0.1:8931/v1] [--model your-model]
"""
import argparse, json, urllib.error, urllib.request

TICKET = ("Customer ticket: Margaret Holloway (DOB 14 March 1979) of Brightwater Logistics Inc. wrote from "
          "margaret.holloway@brightwater-logistics.example, phone +1 415 555 0173. Her card is 4111 1111 1111 1111. "
          "She asks for a refund of $1,240 by 1 March 2027.\n\n"
          "Write a one-sentence reply that names the customer and her company.")


def post(url, body):
    req = urllib.request.Request(url, json.dumps(body).encode(), {"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"{url}: HTTP {e.code} {e.read().decode()}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://127.0.0.1:8931/v1")
    ap.add_argument("--model")
    a = ap.parse_args()
    request = {"messages": [{"role": "user", "content": TICKET}], "max_tokens": 2000}
    if a.model:
        request["model"] = a.model

    print("1. You send:\n\n" + TICKET + "\n")
    preview = post(a.url + "/preview", request)
    print(f"2. What leaves the machine ({preview['masked']} values masked):\n\n" + preview["would_send"]["messages"][0]["content"] + "\n")
    print("3. What you get back, restored:\n\n" + post(a.url + "/ask", request)["text"])


if __name__ == "__main__":
    main()
