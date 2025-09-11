import json
import glob
import os
from collections import defaultdict

def build_ext_to_int(
    folder: str,
    internal_prefix: str = "10.",
    external_prefix: str = "100."
):
    all_internal_ips = set()
    files = glob.glob(os.path.join(folder, "tokenmap_*.json"))
    file_to_internal_set = {}

    for fp in files:
        with open(fp, "r", encoding="utf-8") as f:
            data = json.load(f)
        internals = {ip for ip in data.keys() if ip.startswith(internal_prefix)}
        all_internal_ips |= internals
        file_to_internal_set[fp] = internals

    def last_octet(ip: str) -> str:
        parts = ip.split(".")
        return parts[-1] if len(parts) == 4 else ip

    ext_to_int = {}
    for fp, internals_in_file in file_to_internal_set.items():
        filename = os.path.basename(fp)
        external_ip = filename.replace("tokenmap_", "").replace(".json", "")

        candidates = list(all_internal_ips - internals_in_file)

        chosen = None
        if len(candidates) == 1:
            chosen = candidates[0]
        else:
            host = last_octet(external_ip)
            same_host = [ip for ip in candidates if last_octet(ip) == host]
            if len(same_host) == 1:
                chosen = same_host[0]
            elif len(same_host) > 1:
                chosen = same_host[0]

        if not chosen and external_ip.startswith(external_prefix):
            guess = external_ip.replace(external_prefix, internal_prefix, 1)
            if guess in all_internal_ips:
                chosen = guess

        if not chosen:
            raise RuntimeError(f"can't find {external_ip} target internal ip, potential candidate: ({candidates})")

        ext_to_int[external_ip] = chosen

    return ext_to_int

def invert(mapping: dict) -> dict:
    # internal -> external
    return {v: k for k, v in mapping.items()}

# 示例：
if __name__ == "__main__":
    folder = "./"
    ext2int = build_ext_to_int(folder)
    print("external -> internal:", ext2int)
    print("internal -> external:", invert(ext2int))
