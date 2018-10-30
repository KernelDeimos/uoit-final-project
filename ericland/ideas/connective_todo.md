## TODO List for HA/Connective

- [done] elconn_list_from_json
  elconn_list_from_phsh
- elconn_make_interpreter() operation
- elconn_call(operation, list) list
- elconn_serve_remote(port, operation)
- elconn_connect_remote(port) operation
- elconn_set_exec
- elconn_run_list
- elconn_create_operation() id

- @dir sa-clusters          // makes a function with scope api
- sa-clusters @req sensor0  // makes a request queue called sensor0

or maybe
- @ sa-clusters (dir)
- sa-clusters @ sensor0 (req)

- @ $ (copy-exec)
- ...
- $ sa-clusters @ sensor0 (maskfunc ([] get) (tmp-req))

Interface API (@)
- (link-operation name id)
- (: type name) @            // make a sub-api

- @ dir /sa-clusters
- @ link-operation name id
- :dir /sa-clusters
- :

> maybe `:` returns `Operation` and not a list
> add `&` to take any list/operation and expose it to library users as an id
