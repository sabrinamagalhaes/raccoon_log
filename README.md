# Log config

Simple module to configure the logging module following a pattern.

### Usage

    from data_client import DataClient

    client  = DataClient(host=<host_to_dataserver>, port=<port_to_dataserver>, route=<correct_route>)
    #Account List
    account_list = client.get_accounts()
    Account
    account = client.get_account(<account_id>)
