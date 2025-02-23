# `persona-manager`

This utility allows administrators and system builders to interact with the creation and
limited control of OpenAI Assistant threads. This utility requires a connection to an API
server as described in `[whorl-server](https://github.com/hellowhorl/whorl-server)`.

## Installing

To install `pmgr`, use the following `pip` command:
```bash
python -m pip install git+https://github.com/hellowhorl/persona-manager
```

## Commands

Invoke each of the following commands using the `pmgr` CLI command:
```pmgr <command> <flags>```

### `create`

`create` adds a `persona` assistant to the OpenAI platform and `whorl-server` Postgres DB.
This command features two required and one optional flag:

* `--name`: template name of the Assistant
* `--prompt`: path to a text file containing the text of a prompt for an assistant
* `--file`: path to a Python file to attach to the Assistant

### `cancel`

* `--thread_id`: ID of thread to cancel run

### `delete`

* `--thread_id`: ID of thread to delete

### `inventory`

The `inventory` command allows managers to look at and add to inventories of any user, agent (persona)
or not. This command elaborates the CLI command structure:
```pmgr inventory <method> <flags>```
The various methods are listed below

#### `--listing`

Requires:

* `--name`: name of user to look up inventory for

#### `--add`

* `--name`: name of user for which to alter inventory
* `--item`: name of item file (in current working directory) to add

