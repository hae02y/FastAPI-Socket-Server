def parse_packet(data: bytes):

    dport = int.from_bytes(data[:2], 'little')
    actual_data = data[2:]

    if not actual_data.startswith(b'djHS'):
        return None

    header = actual_data[:10]
    usm_list = actual_data[10:]

    # \x00 값을 제외한 유효한 USM 바이트 리스트
    usm_filtered = bytes(b for b in usm_list if b != 0x00)

    scm_num = header[7]

    # 상태별 분류
    status_map = {
        0x80: "공차",
        0x81: "만차",
        0x82: "만차1",
        0x83: "만차2",
        0x84: "만차3"
    }

    dport_ccm = {
        7891:1,
        7892:2,
        7893:3
    }

    status_list = []
    for i, b in enumerate(usm_filtered):
        status = status_map.get(b, "알 수 없음")
        status_list.append({
            "index": i + 1,
            "hex": f"{b:#04x}",
            "status": status
        })

    return {
        "header": header.hex(),
        "ccm_num": dport_ccm.get(dport, -1),
        "scm_num": scm_num,
        # "usm_list_length": len(usm_list),
        "usm_length": len(usm_filtered),
        "status_details": status_list
    }