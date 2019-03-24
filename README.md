note: up-to-date source code will be found in the Capstone_Winter_Work directory.

## Setup Tutorials

Setup tutorials will use the placeholder `$REPO` to indicate the repository's
root directory. You can run `REPO=$(git rev-parse --show-toplevel)` from any
location within the repository to populate this variable.

### HA Python Console
The console allows a direct line of communication with HA/Connective, which will
be useful in debugging integration issues or bugs within Connective itself.

The following steps assume HA/Manager is running at `http://127.0.0.1:3003`.
Replace this URL with the host URL where HA/Manager is running.

#### Step 1
Download the latest version of elconn.so from
[here](https://github.com/RLiscanoUOIT/capstone-project-group-23/releases)
and place it in this location:

```
$REPO/Capstone_Winter_Work/HA/connective/connective/sharedlib/elconn.so
```

There may already be an `elconn.so` file in this directory. Please overwrite it
as the existing file may not be a recent release.

#### Step 2

To run the console, enter the following commands:
```
cd $REPO/Capstone_Winter_Work/HA/pyconsole
python3 main.py myname http://127.0.0.1:3003
```

You can replace the argument `myname` with any ID to identify the console.


#### Interesting Commands to Run in the Console

##### Using `__debug_listmethods`
HA/Connective maintains source data structures for devices in the `devices`
namespace. To see all available operations, run this command:

```
hub devices __debug_listmethods
```

Note the `hub` prefix. This tells the console to send your command to the
Manager's instance of Connective (the URL provided as an argument). Without the
prefix, a command will run in the console's own local instance of Connective.

##### Interacting with a Device

Add a device called `somedevice`:
```
hub devices add-device (json-decode-one '{}') (json-decode-one '{}') somedevice
```
Note that the first, and second parameters are: Mozilla device definition,
and user-defined meta; respectively. In production, the first parameter should
have a full JSON definition as specified by
[this document](https://iot.mozilla.org/wot/#web-thing-rest-api)

Set a property of `somedevice` using the queue:
```
hub devices registry somedevice update-queue enque (json-decode-one '{"key":123}')
```

Set a property of `somedevice` directly (generally, prefer queue method):
```
hub devices registry somedevice properties : 'key' (store (int 123))
```

Read a property of `somedevice`:
```
hub devices registry somedevice properties 'key'
```
observe that the console outputs "123".