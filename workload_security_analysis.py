import time
import cloudpassage

# get a CloudPassage session object
def get_cloud_passage_session():
    # credentials retreived from either environment variables
    # or /etc/cloudpassage.yaml if not running in a lambda function
    apiCredentials = cloudpassage.ApiKeyManager()

    # create an API connection object
    cp_session = cloudpassage.HaloSession(apiCredentials.key_id, apiCredentials.secret_key)

    return cp_session

# checks the status of an API command
def check_status(cp_server, server_id, command_id):
    # responses come back with heartbeats so need to wait
    delay = 10

    time.sleep(delay)
    response = cloudpassage.Server.command_details(cp_server, server_id, command_id)

    return response

# monitors status of a request
def process_scan_request(cp_session, server_id, response):
    QUEUED = "queued"
    PENDING = "pending"
    FAILED = "failed"
    STARTED = "started"
    STATUS = "status"
    RESULT = "result"

    ret_val = 0

    cp_server = cloudpassage.Server(cp_session)

    # get command ID then check until command finishes
    command_id = response["id"]
    response = cloudpassage.Server.command_details(cp_server, server_id, command_id)

    while response[STATUS] == QUEUED or response[STATUS] == PENDING or response[STATUS] == STARTED:
        print 'Command status is %s... waiting for next heartbeat...' % response[STATUS]
        response = check_status(cp_server, server_id, command_id)

    if response[STATUS] == FAILED:
        errorMessage = response[RESULT]
        print "Command failed on host with %s" % errorMessage
        ret_val = 1

    return ret_val

# checks if there are any critical findings in the scan
def check_for_critical_findings(results):
    critical_findings = results["scan"]["critical_findings_count"]

    return critical_findings

# print out critical findings
def get_critical_findings(results, critical_findings_to_report):
    issue = "bad"

    for result in results["scan"]["findings"]:
        if result["status"] == issue and result["critical"] is True:
            try:
                critical_findings_to_report.append(result["package_name"])
            except:
                critical_findings_to_report.append(result["rule_name"])

    return critical_findings_to_report

def main():
    FIRST = 0
    critical_findings_to_report = ["Critical issues: "]
    scan_critical_findings = 0
    critical_findings = 0

    # get a session object
    cp_session = get_cloud_passage_session()

    # get a server object
    cp_server = cloudpassage.Server(cp_session)

    # this allows you to use the first server in the list - apply
    # a policy to the root and inherit down
    halo_servers = cp_server.list_all()

    # or choose a server and get the ID from the URL in the portal
    server_id = halo_servers[FIRST]["id"]

    cp_scan = cloudpassage.Scan(cp_session)

    # scan workload
    scan_type = "sva"
    response = cp_scan.initiate_scan(server_id, scan_type)

    process_scan_request(cp_session, server_id, response)

    # once scan is complete check for critical findings
    results = cp_scan.last_scan_results(server_id, scan_type)

    # are there critical findings and if so what are they
    scan_critical_findings = check_for_critical_findings(results)
    critical_findings_to_report = \
        get_critical_findings(results, critical_findings_to_report)

    critical_findings = scan_critical_findings

    # scan workload
    scan_type = "csm"

    response = cp_scan.initiate_scan(server_id, scan_type)

    process_scan_request(cp_session, server_id, response)

    # once scan is complete check for critical findings
    results = cp_scan.last_scan_results(server_id, scan_type)

    scan_critical_findings = check_for_critical_findings(results)
    critical_findings_to_report = \
        get_critical_findings(results, critical_findings_to_report)

    critical_findings = critical_findings + scan_critical_findings

    if critical_findings != 0:
        print "\n%s\n" % critical_findings_to_report
        raise ValueError('Scan failed with %d critical findings' % critical_findings)
    else:
        print "\nNo critical findings found.\n"

if __name__ == "__main__":
    try:
        main()
    except cloudpassage.CloudPassageGeneral as err:
        print "Error: %s" % err
        sys.exit(1)
