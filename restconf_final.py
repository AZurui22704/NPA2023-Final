import json
import requests
requests.packages.urllib3.disable_warnings()

# Router IP Address is 10.0.15.189
api_url = "https://10.0.15.189/restconf/data/ietf-interfaces:interfaces/interface=loopback{}"

# the RESTCONF HTTP headers, including the Accept and Content-Type
headers = {"Accept": "application/yang-data+json", "Content-Type": "application/yang-data+json"}
basicauth = ("admin", "cisco")


def create():
    student_id = "65070206"  # example student ID
    loopback_id = student_id[-3:]  # last 3 digits of student ID
    ip_address = f"172.30.{loopback_id}.1"
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": f"loopback{student_id}",
            "description": "Created via RESTCONF",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [{"ip": ip_address, "netmask": "255.255.255.0"}]
            }
        }
    }

    resp = requests.put(
        api_url.format(student_id),
        data=json.dumps(yangConfig),
        auth=basicauth,
        headers=headers,
        verify=False
    )

    if resp.status_code == 201:
        return f"Interface loopback {student_id} is created successfully"
    elif resp.status_code == 409:
        return f"Cannot create: Interface loopback {student_id} already exists"
    else:
        return f"Error: {resp.status_code}"


def delete():
    student_id = "65070206"
    resp = requests.delete(
        api_url.format(student_id),
        auth=basicauth,
        headers=headers,
        verify=False
    )

    if resp.status_code == 204:
        return f"Interface loopback {student_id} is deleted successfully"
    elif resp.status_code == 404:
        return f"Cannot delete: Interface loopback {student_id} does not exist"
    else:
        return f"Error: {resp.status_code}"


def enable():
    student_id = "65070206"
    yangConfig = {
        "ietf-interfaces:interface": {
            "enabled": True
        }
    }

    resp = requests.patch(
        api_url.format(student_id),
        data=json.dumps(yangConfig),
        auth=basicauth,
        headers=headers,
        verify=False
    )

    if resp.status_code == 204:
        return f"Interface loopback {student_id} is enabled successfully"
    elif resp.status_code == 404:
        return f"Cannot enable: Interface loopback {student_id} does not exist"
    else:
        return f"Error: {resp.status_code}"


def disable():
    student_id = "65070206"
    yangConfig = {
        "ietf-interfaces:interface": {
            "enabled": False
        }
    }

    resp = requests.patch(
        api_url.format(student_id),
        data=json.dumps(yangConfig),
        auth=basicauth,
        headers=headers,
        verify=False
    )

    if resp.status_code == 204:
        return f"Interface loopback {student_id} is shutdowned successfully"
    elif resp.status_code == 404:
        return f"Cannot shutdown: Interface loopback {student_id} does not exist"
    else:
        return f"Error: {resp.status_code}"


def status():
    student_id = "65070206"
    api_url_status = api_url.format(student_id)

    resp = requests.get(
        api_url_status,
        auth=basicauth,
        headers=headers,
        verify=False
    )

    if resp.status_code == 200:
        response_json = resp.json()
        admin_status = response_json["ietf-interfaces:interface"]["enabled"]
        if admin_status:
            return f"Interface loopback {student_id} is enabled"
        else:
            return f"Interface loopback {student_id} is disabled"
    elif resp.status_code == 404:
        return f"No Interface loopback {student_id}"
    else:
        return f"Error: {resp.status_code}"