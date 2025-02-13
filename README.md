# `persona-manager`

This utility allows administrators and system builders to interact with the creation and
limited control of OpenAI Assistant threads. This utility requires a connection to an API
server as described in `[whorl-server](https://github.com/hellowhorl/whorl-server)`.

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

* --thread_id`: ID of thread to delete
